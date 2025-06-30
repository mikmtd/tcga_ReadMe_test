import pandas as pd

# 入力ファイル（適宜変更）
tsv_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical_expanded_final.tsv"
df = pd.read_csv(tsv_file, sep="\t", nrows=100)
# 出力ファイル
output_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/yaml/rule_list.tsv"

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
with open(output_file, "w") as f:
    f.write("# 特別な変換ルールを定義\n")
    f.write("rules = {\n")
    for k, v in rules.items():
        if v:  # 空リスト（strのみ）はスキップ
            f.write(f'    "{k}": {v},\n')
    f.write("}\n")

print("{output_file} に保存しました。")