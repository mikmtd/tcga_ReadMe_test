import json
import pandas as pd

# ファイルパス設定(適宜変更)
json_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/smpl/biospecimen.cohort.2025-06-19.json"
output_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/smpl/sample.tsv"

# 欲しいフィールド一覧
FIELDS = [
    "project_id", "case_id", "case_submitter_id", "sample_id", "sample_submitter_id",
    "biospecimen_anatomic_site", "biospecimen_laterality", "catalog_reference", "composition",
    "current_weight", "days_to_collection", "days_to_sample_procurement",
    "diagnosis_pathologically_confirmed", "distance_normal_to_tumor", "distributor_reference",
    "freezing_method", "growth_rate", "initial_weight", "intermediate_dimension", "is_ffpe",
    "longest_dimension", "method_of_sample_procurement", "oct_embedded", "passage_count",
    "pathology_report_uuid", "preservation_method", "sample_ordinal", "sample_type",
    "sample_type_id", "shortest_dimension", "specimen_type", "state",
    "time_between_clamping_and_freezing", "time_between_excision_and_freezing",
    "tissue_collection_type", "tissue_type", "tumor_code", "tumor_code_id", "tumor_descriptor"
]

# JSON読み込み
with open(json_file) as f:
    data = json.load(f)

records = []

# 各症例を処理
for case in data:
    case_submitter_id = case.get("submitter_id", "")
    case_id = case.get("case_id", "")
    project_id = case.get("project", {}).get("project_id", "")

    for sample in case.get("samples", []):
        row = {
            "project_id": project_id,
            "case_id": case_id,
            "case_submitter_id": case_submitter_id,
            "sample_id": sample.get("sample_id", ""),
            "sample_submitter_id": sample.get("submitter_id", "")
        }

        # 残りのFIELDSを追加
        for field in FIELDS:
            if field in row:  # すでに追加済み
                continue
            row[field] = sample.get(field, "")
        
        records.append(row)

# DataFrameにして列名に "smpl_" を付加
df = pd.DataFrame(records, columns=FIELDS)
df.columns = [f"smpl_{col}" for col in df.columns]

# TSV出力
df.to_csv(output_file, sep="\t", index=False)

print(f"✅ Saved: {output_file}")
