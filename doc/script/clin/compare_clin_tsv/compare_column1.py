import pandas as pd

# ファイルパスの指定
file1 = "/Users/mmatsuda/Documents/rdf-config関連/rdf-config/config/tcga/clinical_small.tsv"
file2 = "/Users/mmatsuda/Desktop/clinical_from_Project/★merge_clin_patho_tsv/merged_output_raw.tsv"
output_file = "/Users/mmatsuda/Desktop/clinical_from_Project/★merge_clin_patho_tsv/clin_column_comparison.txt"

# ヘッダーのみ読み込み
df1 = pd.read_csv(file1, sep="\t", nrows=0)
df2 = pd.read_csv(file2, sep="\t", nrows=0)

# df1のカラム名から 'clin_' を削除
columns1 = set(col.replace("clin_", "") for col in df1.columns)

# df2のカラム名と、ドットの後ろの部分を対応付ける
df2_column_map = {col: col.split(".")[-1] for col in df2.columns}
columns2_suffixes = set(df2_column_map.values())

# 共通、片方にしかないカラムを判定
common = columns1 & columns2_suffixes
only_in_1 = columns1 - columns2_suffixes
only_in_2_suffixes = columns2_suffixes - columns1

# df2の元のカラム名で、suffixがonly_in_2_suffixesに該当するものを抽出
only_in_2_fullnames = [col for col, suffix in df2_column_map.items() if suffix in only_in_2_suffixes]

# 共通のsuffixに対応するdf2の元のカラム名を抽出
common_fullnames_in_df2 = [col for col, suffix in df2_column_map.items() if suffix in common]


# 結果をファイルに書き出し
with open(output_file, "w") as f:
    f.write("❌ df1 にしかないカラム:\n")
    for col in sorted(only_in_1):
        f.write(f"- {col}\n")

    f.write("\n❌ df2 にしかないカラム (元の列名):\n")
    for col in sorted(only_in_2_fullnames):
        f.write(f"- {col}\n")

    f.write("\n✅ 共通のカラム (df2の元の列名):\n")
    for col in sorted(common_fullnames_in_df2):
        f.write(f"- {col}\n")


print(f"✅ カラム比較結果を保存しました: {output_file}")
