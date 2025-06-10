import pandas as pd

# clinical.tsv を読み込み（適宜変更）
df = pd.read_csv('./config/tcga/clin/clinical.tsv', sep='\t', dtype=str)

# カラム名の変換：エンティティ部分を除去して "clin_" を追加
df.columns = [f"clin_{col.split('.')[-1]}" for col in df.columns]

# "'--" を空文字に置換（完全一致の '--' を置換）
df = df.replace("'--", '', regex=False)

# DataFrame の断片化防止（警告回避のため）
df = df.copy()

# 変換対象列の名前を取得（元が何だったかによる）
# ここでは変換後の列名でアクセス
case_id_col = "clin_case_id"
treatment_col = "clin_treatment_type"

# 特定の treatment_type の変換マッピング
treatment_map = {
    "Pharmaceutical Therapy, NOS": "Phar",
    "Radiation Therapy, NOS": "Radi"
}

# 新しいユニークID列の作成
def create_unique_id(row):
    treatment = treatment_map.get(row[treatment_col], row[treatment_col])
    return f"{row[case_id_col]}__{treatment}"

df["clin_case_id___hoge"] = df.apply(create_unique_id, axis=1)

# 結果を保存(適宜ディレクトリを変更）
df.to_csv('./config/tcga/clinical_processed.tsv', sep='\t', index=False)
