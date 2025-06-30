import csv

# 設定
input_tsv = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical_expanded_final.tsv"
output_yaml = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/model_yaml/clinical_model.yaml"

base_subject = "TcgaClinical"
subject_curie = "tcgac:1"
class_type = "tcgac:TcgaClinical"
namespace = "tcgac"


# 読み込み
with open(input_tsv, encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter="\t")
    headers = reader.fieldnames
    first_row = next(reader)

# YAML構造を構築
yaml_blocks = []

# クラス主体

yaml_blocks.append(f"- {base_subject} {subject_curie}:")
yaml_blocks.append(f"  - a: {class_type}")

for header in headers:
    sample_value = first_row[header]
    sample_value = sample_value if sample_value.strip() != "" else "--"
    predicate = f"{namespace}:{header}"
    block = f"  - {predicate}:\n    - {header}: {sample_value}"
    yaml_blocks.append(block)

# 出力
with open(output_yaml, "w", encoding="utf-8") as f:
    f.write("\n".join(yaml_blocks))

print(f"✅ model.yaml を生成しました → {output_yaml}")
