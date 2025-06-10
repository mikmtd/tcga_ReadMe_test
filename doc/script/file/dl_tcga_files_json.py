import requests
import json

# 保存先ファイル（適宜変更）
output_file = "./config/tcga/file/files.tcga.all.json"

# TCGAプロジェクトリスト（33プロジェクト）（適宜変更）
tcga_projects = [
    "TCGA-ACC", "TCGA-BLCA", "TCGA-BRCA", "TCGA-CESC", "TCGA-CHOL", "TCGA-COAD", "TCGA-DLBC",
    "TCGA-ESCA", "TCGA-GBM", "TCGA-HNSC", "TCGA-KICH", "TCGA-KIRC", "TCGA-KIRP", "TCGA-LAML",
    "TCGA-LGG", "TCGA-LIHC", "TCGA-LUAD", "TCGA-LUSC", "TCGA-MESO", "TCGA-OV", "TCGA-PAAD",
    "TCGA-PCPG", "TCGA-PRAD", "TCGA-READ", "TCGA-SARC", "TCGA-SKCM", "TCGA-STAD", "TCGA-TGCT",
    "TCGA-THCA", "TCGA-THYM", "TCGA-UCEC", "TCGA-UCS", "TCGA-UVM"
]

# GDC API エンドポイント
endpoint = "https://api.gdc.cancer.gov/files"

# フィルター設定（TCGAプロジェクトのみ）
filters = {
    "op": "in",
    "content": {
        "field": "cases.project.project_id",
        "value": tcga_projects
    }
}

# フィールドの指定
fields = [
    "file_id",
    "file_name",
    "file_size",
    "data_type",
    "data_category",
    "data_format",
    "experimental_strategy",
    "platform",
    "access",
    "cases.case_id",
    "cases.project.project_id"
]

# パラメータ設定
params = {
    "filters": json.dumps(filters),
    "format": "JSON",
    "size": 10000,
    "fields": ",".join(fields),
    "expand": "cases"
}

# 結果格納
all_results = []
offset = 0
print("🔄 Downloading all TCGA file metadata...")

while True:
    params["from"] = offset
    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code} - {response.text}")
        break

    data = response.json().get("data", {}).get("hits", [])
    if not data:
        break

    all_results.extend(data)
    offset += 10000
    print(f"✅ Fetched {offset} files...")

# 保存
with open(output_file, "w") as f:
    json.dump(all_results, f, indent=2)

print(f"\n✅ Done. Saved to: {output_file}")
