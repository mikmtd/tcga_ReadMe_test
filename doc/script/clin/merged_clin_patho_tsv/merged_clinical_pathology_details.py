import pandas as pd

# --- ファイルパスの設定 ---
clinical_path = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical.cohort.2025-06-19/clinical.tsv'
pathology_path = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical.cohort.2025-06-19/pathology_detail.tsv'
raw_output_path = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/merged_output_raw.tsv'
final_output_path = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/merged_output_clinial.tsv'
duplicate_fields_path = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/duplicate_output.tsv'


# --- 工程1.ファイル読み込み（すべて文字列として） ---
df1 = pd.read_csv(clinical_path, sep='\t', dtype=str, on_bad_lines='skip')
df2 = pd.read_csv(pathology_path, sep='\t', dtype=str, on_bad_lines='skip')

# --- 工程2.重複列の削除（cases.case_id 以外の共通列を df2 から削除） ---
common_cols = [col for col in df1.columns if col in df2.columns and col != 'cases.case_id']
df2 = df2.drop(columns=common_cols)

# --- 工程3.内部結合 ---
df_merged = pd.merge(df1, df2, on='cases.case_id', how='inner')

# --- 工程4.結合直後のファイルを保存 ---
df_merged.to_csv(raw_output_path, sep='\t', index=False)

# --- 工程5.重複を考慮した列名変換関数 ---
def transform_column_name(col, duplicates_map):
    if '.' in col:
        prefix, rest = col.split('.', 1)
        simple_name = f"clin_{rest}"
        if simple_name in duplicates_map:
            return f"clin_{prefix}_{rest}"  # 重複がある場合はエンティティ名を残す
        else:
            return simple_name
    else:
        return col

# --- 工程6.重複フィールド名の検出と報告用整形 ---

prefix_map = {}
for col in df_merged.columns:
    if '.' in col:
        prefix, rest = col.split('.', 1)
        transformed = f"clin_{rest}"
        report_name = f"clin_{prefix}_{rest}"
        if transformed in prefix_map:
            prefix_map[transformed].append(report_name)
        else:
            prefix_map[transformed] = [report_name]

duplicates = {k: v for k, v in prefix_map.items() if len(v) > 1}

transformed_names = [transform_column_name(col, duplicates) for col in df_merged.columns]

# --- 工程7.重複フィールド名の保存 ---
with open(duplicate_fields_path, 'w') as f:
    f.write("Fields that would be duplicated after replacing prefix with 'clin_':\n")
    for name, sources in duplicates.items():
        f.write(f"{name}: " + ", ".join(sources) + "\n")

# --- 工程8.列名の更新 ---
df_merged.columns = transformed_names

# --- 工程9. '--' や \"'--\" を空文字に置換 ---
df_merged.replace({"--": "", "'--": ""}, inplace=True)

# --- 工程10.ユニークID列の追加 ---
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

# --- 工程11.出力 ---
df_merged.to_csv(final_output_path, sep='\t', index=False)
print(f"✅ Done. {len(df_merged.columns)} fields processed, columns renamed, '--' replaced, and unique ID column appended.")
print(f"📝 Duplicate fields (after renaming) saved to: {duplicate_fields_path}")
