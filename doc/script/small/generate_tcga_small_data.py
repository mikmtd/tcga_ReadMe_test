import pandas as pd

def filter_tsv_by_ids(input_file, output_file, target_column, target_ids):
    """指定したIDでTSVをフィルタリングして保存"""
    df = pd.read_csv(input_file, sep="\t", dtype=str)
    filtered_df = df[df[target_column].isin(target_ids)]
    filtered_df.to_csv(output_file, sep="\t", index=False)
    print(f"{len(filtered_df)} 件を抽出して {output_file} に保存しました。")

def main():
    # clinical_expanded_final.tsv の抽出
    filter_tsv_by_ids(
        input_file="./clin/最終的に必要なファイル/clinical_expanded_final.tsv",
        output_file="./small/small_clinical.tsv",
        target_column="clin_case_id",
        target_ids={
            "ed471051-41dc-404c-87ec-db4a281ecfb5",
            "c46971a1-cbac-425d-bac2-f4142c92522e",
            "c7162d11-4bdc-41cd-a964-46fc416829db"
        }
    )

    # file.tsv の抽出
    filter_tsv_by_ids(
        input_file="./clin/最終的に必要なファイル/file.tsv",
        output_file="./small/small_files.tsv",
        target_column="file_id",
        target_ids={
            "88edcca8-97f0-4940-951e-93b13d72fc27",
            "fbb750a7-8577-4b74-985a-bc760cf5b296",
            "ba66296a-74a2-486b-bdb6-2e40fcc75b03"
        }
    )

    # manifest の抽出
    filter_tsv_by_ids(
        input_file="./clin/最終的に必要なファイル/gdc_manifest.2025-06-19.tsv",
        output_file="./small/small_manifest.tsv",
        target_column="mani_id",
        target_ids={
            "88edcca8-97f0-4940-951e-93b13d72fc27",
            "fbb750a7-8577-4b74-985a-bc760cf5b296",
            "ba66296a-74a2-486b-bdb6-2e40fcc75b03"
        }
    )

    # sample.tsv の抽出
    filter_tsv_by_ids(
        input_file="./clin/最終的に必要なファイル/sample.tsv",
        output_file="./small/small_sample.tsv",
        target_column="smpl_case_id",
        target_ids={
            "ed471051-41dc-404c-87ec-db4a281ecfb5",
            "c46971a1-cbac-425d-bac2-f4142c92522e",
            "c7162d11-4bdc-41cd-a964-46fc416829db"
        }
    )

if __name__ == "__main__":
    main()
