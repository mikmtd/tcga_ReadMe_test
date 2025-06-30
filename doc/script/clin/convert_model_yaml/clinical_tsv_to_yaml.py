import pandas as pd

# 入力TSV（適宜変更）
tsv_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clinical_expanded_final.tsv"

# 特別な変換ルールを定義（確定した型でコピペ）
rules = {
    "clin_project_id": ['prepend("tcgap:")'],
    "clin_case_id": ['prepend("tcgaa:")'],
    "clin_days_to_consent": ['to_int'],
    "clin_days_to_lost_to_followup": ['to_int'],
    "clin_age_at_index": ['to_int'],
    "clin_age_is_obfuscated": ['to_bool'],
    
    "clin_days_to_birth": ['to_int'],
    "clin_days_to_death": ['to_int'],
    
    
    "clin_occupation_duration_years": ['to_int'],
    
    
    "clin_weeks_gestation_at_birth": ['to_float'],
    "clin_year_of_birth": ['to_int'],
    "clin_year_of_death": ['to_int'],
    
    "clin_age_at_diagnosis": ['to_int'],
    "clin_days_to_best_overall_response": ['to_int'],
    "clin_days_to_diagnosis": ['to_int'],
    "clin_days_to_last_follow_up": ['to_float'],
    "clin_days_to_last_known_disease_status": ['to_float'],
    "clin_days_to_recurrence": ['to_float'],
    "clin_diagnosis_is_primary_disease": ['to_bool'],
    
    "clin_gleason_patterns_percent": ['to_int'],
    "clin_gleason_score": ['to_int'],
    
    "clin_diagnoses_margin_distance": ['to_float'],
    
    "clin_mitotic_count": ['to_int'],
    
    
    
    "clin_primary_disease": ['to_bool'],
    
    
    "clin_sites_of_involvement_count": ['to_int'],
    "clin_tumor_burden": ['to_float'],

    "clin_tumor_depth": ['to_float'],
    "clin_year_of_diagnosis": ['to_int'],
    
    "clin_course_number": ['to_int'],
    "clin_days_to_treatment_end": ['to_int'],
    "clin_days_to_treatment_start": ['to_int'],
    "clin_lesions_treated_number": ['to_float'],
    "clin_treatments_margin_distance": ['to_float'], 
    "clin_number_of_cycles": ['to_int'],
    "clin_number_of_fractions": ['to_float'],
    "clin_prescribed_dose": ['to_float'],

    "clin_therapeutic_level_achieved": ['to_bool'],


    "clin_treatment_dose": ['to_int'],
    "clin_treatment_dose_max": ['to_float'],
    "clin_treatment_duration": ['to_int'],
    "clin_treatment_outcome_duration": ['to_int'],
    "clin_breslow_thickness": ['to_bool'],
    "clin_circumferential_resection_margin": ['to_float'],
    "clin_greatest_tumor_dimension": ['to_float'],
    "clin_lymph_nodes_positive": ['to_int'],
    "clin_lymph_nodes_tested": ['to_int'],
    "clin_tumor_largest_dimension_diameter": ['to_float'],
    "clin_percent_tumor_invasion": ['to_float'],
    "clin_case_id___hoge": ['prepend("tcgac:")'],
}

    # _ID_の例


# TSVのカラムを取得
df = pd.read_csv(tsv_file, sep="\t", nrows=0)
fields = list(df.columns)

# 優先的に出力したいIDフィールド
id_fields = ["clin_case_id", "clin_submitter_id", "clin_project_id"]


# YAML構造構築
lines = []
lines.append("- TcgaClinical:")
lines.append("    - subject:")
lines.append(f"        - source(\"{tsv_file}\")")
lines.append("")
lines.append("    # _ID_")
lines.append("        - tsv(\"clin_case_id___hoge\")")
lines.append("        - prepend(\"tcgac:\")")
lines.append("")
lines.append("    - objects:")
lines.append("    # _ID_")


# IDフィールドを先に出力
for col in id_fields:
    if col in fields:
        lines.append(f"    - {col}:")
        lines.append(f"        - tsv(\"{col}\")")
        if col in rules:
            for rule in rules[col]:
                lines.append(f"        - {rule}")
        lines.append("") # ← ここで1行空ける

# 残りのフィールドを出力
for col in fields:
    if col not in id_fields:
        lines.append(f"    - {col}:")
        lines.append(f"        - tsv(\"{col}\")")
        if col in rules:
            for rule in rules[col]:
                lines.append(f"        - {rule}")

# 保存（適宜変更）
output_file = "/Users/mmatsuda/Desktop/clinical_from_Project/ALL最終確認/clin/clin_convert.yaml"
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ YAML を保存しました: {output_file}")
