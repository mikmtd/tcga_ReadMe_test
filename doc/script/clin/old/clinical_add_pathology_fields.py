import pandas as pd
import json
import re
from collections import Counter

# ファイルパス
tsv_path = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical.cohort.2025-06-19/clinical.tsv"
json_path = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical.cohort.2025-06-19.json"

output_path = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical_expanded_final.tsv"

# 追加したいフィールド
additional_fields = [
    "diagnoses[0].pathology_details[0].anaplasia_present",
    "diagnoses[0].pathology_details[0].anaplasia_present_type",
    "diagnoses[0].pathology_details[0].breslow_thickness",
    "diagnoses[0].pathology_details[0].circumferential_resection_margin",
    "diagnoses[0].pathology_details[0].greatest_tumor_dimension",
    "diagnoses[0].pathology_details[0].gross_tumor_weight",
    "diagnoses[0].pathology_details[0].largest_extrapelvic_peritoneal_focus",
    "diagnoses[0].pathology_details[0].lymph_node_involved_site",
    "diagnoses[0].pathology_details[0].lymph_nodes_positive",
    "diagnoses[0].pathology_details[0].lymph_nodes_tested",
    "diagnoses[0].pathology_details[0].lymphatic_invasion_present",
    "diagnoses[0].pathology_details[0].non_nodal_regional_disease",
    "diagnoses[0].pathology_details[0].non_nodal_tumor_deposits",
    "diagnoses[0].pathology_details[0].percent_tumor_invasion",
    "diagnoses[0].pathology_details[0].perineural_invasion_present",
    "diagnoses[0].pathology_details[0].peripancreatic_lymph_nodes_positive",
    "diagnoses[0].pathology_details[0].peripancreatic_lymph_nodes_tested",
    "diagnoses[0].pathology_details[0].transglottic_extension",
    "diagnoses[0].pathology_details[0].tumor_largest_dimension_diameter",
    "diagnoses[0].pathology_details[0].vascular_invasion_present",
    "diagnoses[0].pathology_details[0].vascular_invasion_type"
]

# --- TSV読み込み ---
df_tsv = pd.read_csv(tsv_path, sep='\t')

# 列名から 'cases.' を除去
df_tsv.columns = [col.replace("cases.", "") for col in df_tsv.columns]

# JSON読み込み
with open(json_path, 'r', encoding='utf-8') as f:
    json_data = json.load(f)


# フィールドが存在するかどうかをチェックする関数
def field_path_exists(entry, field):
    try:
        val = entry
        tokens = re.findall(r"[^\.\[\]]+", field)
        for token in tokens:
            if isinstance(val, list) and token.isdigit():
                val = val[int(token)]
            elif isinstance(val, dict):
                val = val[token] # ← .get() ではなく [] にすることで KeyError を発生させる
            else:
                return False
        return True # Noneのまま返すことで空欄になる
    except (KeyError, IndexError, TypeError, ValueError):
        return False


# 値を抽出する関数（None でもそのまま返す）   
def extract_field(entry, field):
    try:
        val = entry
        tokens = re.findall(r"[^\.\[\]]+", field)
        for token in tokens:
            if isinstance(val, list) and token.isdigit():
                val = val[int(token)]
            elif isinstance(val, dict):
                val = val.get(token)
            else:
                return None
        return val
    except (KeyError, IndexError, TypeError, ValueError):
        return None

# --- 追加対象のフィールドがJSONに実際に存在するかチェック ---
existing_fields = []
for field in additional_fields: #追加したい全フィールドに対して
    for entry in json_data: #全JSON症例に対して
        if field_path_exists(entry, field) :# そのフィールドが1回でも存在したら
            existing_fields.append(field)  # そのフィールドを出力対象に加える
            break #無駄な探索を避けて次のフィールドへ



# JSONデータを整形
json_records = [] #1レコード＝1行のシンプルな辞書に変換していくためのリスト
for entry in json_data: #JSONの各症例（患者1人分）に対して処理
    record = {"case_id": entry.get("case_id")} # 🔽 ここで case_id を追加
    for field in existing_fields: #実在するフィールド」だけを対象に値を抽出
        record[field] = extract_field(entry, field)
    json_records.append(record)

df_json = pd.DataFrame(json_records)


# --- 追加フィールド名をアルファベット順にソート ---
existing_fields_sorted = sorted(existing_fields)

# --- TSVの後ろに追加（case_id列は二重にしない） ---
cols_before = list(df_tsv.columns)
cols_after = [f for f in existing_fields_sorted if f not in cols_before]
df_merged = pd.merge(df_tsv, df_json, on="case_id", how="left")

# --- 列順を制御: 元TSVの列 + 追加したフィールドの列 ---
df_merged = df_merged[cols_before + cols_after]

# --- カラム名の変換 ---
original_columns = df_merged.columns.tolist()
simple_names = [f"clin_{col.split('.')[-1]}" for col in original_columns] # 元の列名を.で区切り、最後だけ取り出して、clin_付加
name_counts = Counter(simple_names) #簡略化した名前の重複がないか
final_names = []
for orig, simple in zip(original_columns, simple_names): 
    if name_counts[simple] > 1: # 重複があれば元の列名を_で繋げてユニーク化
        safe_name = f"clin_{orig.replace('.', '_')}"
        final_names.append(safe_name)
    else:
        final_names.append(simple) # 重複なければ簡略名のまま
df_merged.columns = final_names

# --- "'--" を空文字に置換 ---
df_merged = df_merged.replace("'--", '', regex=False)
df_merged = df_merged.copy()

# --- ユニークID列の追加 ---
case_id_col = "clin_case_id"
treatment_col = "clin_treatment_type"
treatment_map = {
    "Pharmaceutical Therapy, NOS": "Phar",
    "Radiation Therapy, NOS": "Radi"
}
def create_unique_id(row):
    treatment = treatment_map.get(row.get(treatment_col, ''), row.get(treatment_col, ''))
    return f"{row.get(case_id_col, '')}__{treatment}"
df_merged["clin_case_id___hoge"] = df_merged.apply(create_unique_id, axis=1)

# --- 出力 ---
df_merged.to_csv(output_path, sep='\t', index=False)
print(f"✅ Done. {len(cols_after)} fields added, columns renamed, '--' replaced, and unique ID column appended.")
