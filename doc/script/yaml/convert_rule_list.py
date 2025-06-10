import pandas as pd

# 適宜変更
tsv_file = "/Users/mmatsuda/Desktop/TCGA_Portal/最終確認/clinical/clinical_processed.tsv"
df = pd.read_csv(tsv_file, sep="\t", nrows=100)

def infer_type(series):
    uniques = set(series.dropna().unique())
    if uniques.issubset({0,1}) or uniques.issubset({"0","1","TRUE","FALSE","True","False"}):
        return "to_bool"
    try:
        series.dropna().astype(int)
        return "to_int"
    except:
        pass
    try:
        series.dropna().astype(float)
        return "to_float"
    except:
        pass
    return []

rules = {}

for col in df.columns:
    conv_rule = infer_type(df[col])
    if conv_rule:
        rules[col] = [conv_rule]
    else:
        rules[col] = []

# 例：特定カラムに手動ルール追加（必要に応じて）
rules["clin_project_id"] = ['prepend("tcgap:")']
rules["clin_case_id"] = ['prepend("tcgaa:")']
rules["clin_case_id___hoge"] = ['prepend("tcgac:")']

# ファイルに書き込み（適宜変更）
with open("/Users/mmatsuda/Desktop/TCGA_Portal/yaml/rules_non_entity.txt", "w") as f:
    f.write("# 特別な変換ルールを定義\n")
    f.write("rules = {\n")
    for k, v in rules.items():
        if v:  # 空リスト（strのみ）はスキップ
            f.write(f'    "{k}": {v},\n')
    f.write("}\n")

print("rules_non_entity.txt に保存しました。")