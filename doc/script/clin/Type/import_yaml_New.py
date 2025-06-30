import pandas as pd
import yaml
import os
import glob

# ===== 設定 =====
tsv_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/merged_output_clinical.tsv"
schema_dir = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/convert_yaml/schema"
output_file = "/Users/mmatsuda/Desktop/clinical_from_Project/⭐︎merge_clin_patho_tsv/rule_list_New2.tsv"
not_found_log = "/Users/mmatsuda/Desktop/clinical_from_Project/⭐︎merge_clin_patho_tsv/⭐︎schema_type_list/not_found_fields_New2.tsv"

# ===== 型変換マップと優先順位 =====
type_map = {
    "boolean": "to_bool",
    "integer": "to_int",
    "long": "to_int",
    "float": "to_float",
    "double": "to_float",
    "number": "to_float",
    "string": "to_str",
    "array": "to_str",
    "text": "to_str",
    "keyword": "to_str"
}
type_priority = ["integer", "number", "float", "string", "boolean"]

# ===== 型抽出関数 =====
def extract_type(field_def):
    if "type" in field_def:
        t = field_def["type"]
        if isinstance(t, str):
            if t == "array":
                items = field_def.get("items", {})
                if "enum" in items or "type" in items:
                    return "array"
                return None
            return t
    for key in ["oneOf", "anyOf"]:
        if key in field_def:
            candidates = [x.get("type") for x in field_def[key] if "type" in x]
            for pref in type_priority:
                if pref in candidates:
                    return pref
    if "enum" in field_def:
        return "string"
    return None

# ===== YAML 読み込みと型抽出 =====
def load_yaml_and_extract_types(yaml_path):
    with open(yaml_path, encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    props = schema.get("properties", {})
    return {field: extract_type(defn) for field, defn in props.items() if extract_type(defn)}

# ===== TSV のカラム処理 =====
df = pd.read_csv(tsv_file, sep="\t", nrows=1)
tsv_cols = list(df.columns)
field_map = {col: col[5:] for col in tsv_cols if col.startswith("clin_")}

# ===== ステップ 3: エンティティと対応する YAML ファイルのマッピング =====
entity_yaml_map = {
    "cases": "case.yaml",
    "demographic": "demographic.yaml",
    "diagnoses": "diagnosis.yaml",
    "treatments": "treatment.yaml",
    "pathology_details": "pathology_detail.yaml"
}

# ===== ステップ 4: 変換ルールの作成 =====
schema_files = glob.glob(os.path.join(schema_dir, "*.yaml"))
rules = {}
field_to_path = {}
not_found_fields = []

for full_col, base_col in field_map.items():
    matched_entity = None
    sub_field = base_col
    for entity in entity_yaml_map:
        if base_col == entity:
            matched_entity = entity
            break
        elif base_col.startswith(entity + "_"):
            matched_entity = entity
            sub_field = base_col[len(entity) + 1:]
            break

    field_type = None
    if matched_entity:
        yaml_file = os.path.join(schema_dir, entity_yaml_map[matched_entity])
        field_types = load_yaml_and_extract_types(yaml_file)
        field_type = field_types.get(sub_field)
    else:
        for schema_path in schema_files:
            field_types = load_yaml_and_extract_types(schema_path)
            if base_col in field_types:
                field_type = field_types[base_col]
                break

    if field_type in type_map:
        rules[full_col] = [type_map[field_type]]
        field_to_path[full_col] = base_col
    else:
        not_found_fields.append(full_col)


# ===== ステップ 5: 手動ルール追加 =====
rules["clin_project_id"] = ['prepend("tcgap:")']
rules["clin_case_id"] = ['prepend("tcgaa:")']
rules["clin_case_id___hoge"] = ['prepend("tcgac:")']

# ===== 変換ルール出力 =====
with open(output_file, "w", encoding="utf-8") as f:
    f.write("# GDC Mapping API に基づく変換ルール\n")
    f.write("rules = {\n")
    for k, v in sorted(rules.items()):
        if v != ["to_str"]:
            comment = f"  # {field_to_path.get(k, '')}"
            f.write(f'    "{k}": {v},{comment}\n')
    for k, v in sorted(rules.items()):
        if v == ["to_str"]:
            comment = f"  # {field_to_path.get(k, '')}"
            f.write(f'    "{k}": {v},{comment}\n')
    f.write("}\n")
print(f"✅ 変換ルールを {output_file} に出力しました。")

# ===== 見つからなかったフィールド出力 =====
if not_found_fields:
    with open(not_found_log, "w", encoding="utf-8") as f:
        f.write("型情報が見つからなかったフィールド一覧:\n")
        for field in sorted(not_found_fields):
            f.write(f"- {field}\n")
    print(f"⚠️ 一部のフィールド型が見つかりませんでした → {not_found_log}")
