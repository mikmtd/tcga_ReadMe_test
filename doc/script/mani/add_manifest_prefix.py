import pandas as pd

# 入力ファイル名(適宜変更)
input_file = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/Mani/gdc_manifest.2025-06-19.102027.txt'
# 出力ファイル名
output_file = '/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/Mani/gdc_manifest.2025-06-19.tsv'

# ファイルを読み込む（タブ区切りを仮定）
df = pd.read_csv(input_file, sep='\t')

# 各カラム名の先頭に 'mani_' を付ける
df.columns = ['mani_' + col for col in df.columns]

# 新しいファイルに保存（インデックスは書き込まない）
df.to_csv(output_file, sep='\t', index=False)

print(f"変換完了：{output_file} に保存されました。")
