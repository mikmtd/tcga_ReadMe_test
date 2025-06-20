import pandas as pd
import requests

# ファイルとシート名ではなく、ファイルパスだけ指定します
file1 = "/Users/mmatsuda/Documents/rdf-config関連/rdf-config/config/tcga/clinical_small.tsv"
file2 = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical.cohort.2025-06-19/clinical.tsv"

# 出力ファイル名
output_file = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/compare column/clin_column_comparison.txt'
# === 最終結果の出力ファイル ===
output_file2 = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/compare column/gdc_additional_fields_output.txt"


# ヘッダーのみ読み込み
df1 = pd.read_csv(file1, sep="\t", nrows=0)
df2 = pd.read_csv(file2, sep="\t", nrows=0)

# df1のカラム名から 'clin_' を削除
columns1 = set(col.replace("clin_", "") for col in df1.columns)

# df2のカラム名から '.' より前の部分を削除
columns2 = set(col.split(".")[-1] for col in df2.columns)

common = columns1 & columns2
only_in_1 = columns1 - columns2
only_in_2 = columns2 - columns1


# 結果をファイルに書き出し

with open(output_file, "w") as f:

    f.write("\n❌ df1 にしかないカラム:\n")
    for col in sorted(only_in_1):
        f.write(f"- {col}\n")

    f.write("\n❌ df2 にしかないカラム:\n")
    for col in sorted(only_in_2):
        f.write(f"- {col}\n")

print(f"✅ カラム比較結果を保存しました: {output_file}")

# === 差分抽出 ===
only_in_df1 = sorted(only_in_1)
print(f"🟨 df1にしかない整形済カラム数: {len(only_in_df1)}")

# === GDC フィールド一覧の取得 ===
print("🔍 GDC フィールド取得中...")
res = requests.get("https://api.gdc.cancer.gov/cases/_mapping")

# ステータスコードでチェック
if res.status_code != 200:
    print(f"❌ GDC API エラー: {res.status_code}")
    print(f"レスポンス内容: {res.text}")
    exit(1)

gdc_field_paths = res.json()["_mapping"].keys()

print(f"✅ フィールド数: {len(gdc_field_paths)} 件取得")

# === GDCとのマッチング ===
matched_fields = []
missing_fields = []

for col in only_in_df1:
    matches = [path for path in gdc_field_paths if path.startswith("cases.") and path.endswith(f".{col}")]
    if matches:
        # "cases." を削除し、[0] を挿入して整形
        path = matches[0].replace("cases.", "")
        # 最初の一致を使用して [0] を入れる
        nested = "[0].".join(path.split("."))
        matched_fields.append(nested)
    else:
        missing_fields.append(col)

# === 出力 ===
with open(output_file2, "w") as f:
    f.write("=== ✅ GDCで見つかったフィールド ===\n")
    f.write("additional_fields = [\n")
    for field in matched_fields:
        f.write(f'    "{field}",\n')
    f.write("]\n\n")

    f.write("=== ⚠️ GDCで見つからなかったフィールド ===\n")
    f.write("missing_fields = [\n")
    for field in missing_fields:
        f.write(f'    "{field}",\n')
    f.write("]\n")

print(f"✅ GDCフィールド照合結果を保存しました: {output_file2}")
