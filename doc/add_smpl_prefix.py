import pandas as pd

input_file = 'sample.tsv'
output_file = 'sample_processed.tsv'

df = pd.read_csv(input_file, sep='\t')
df.columns = ['smpl_' + col for col in df.columns]
df.to_csv(output_file, sep='\t', index=False)

print(f"変換完了：{output_file} に保存されました。")
