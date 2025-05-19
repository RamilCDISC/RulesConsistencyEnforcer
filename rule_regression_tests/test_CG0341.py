import subprocess
import pytest
import pandas as pd
import os
import numpy as np

RULE_JSON_FILE = "published_rules/CG0341/CG0341.json"
DATASET_PATH = "json_datasets/CG0341/converted_dataset.json"
COMMAND = "python core.py test -s sdtmig -v 3.4 -r " + RULE_JSON_FILE + " -dp " + DATASET_PATH + ""

def run_command():
    process = subprocess.run(COMMAND, shell=True, capture_output=True, text=True)
    assert process.returncode == 0, f"Command failed:\n{process.stderr}"

def find_latest_excel():
    files = [f for f in os.listdir() if f.endswith(".xlsx")]
    assert files, "No Excel file found."
    return max(files, key=os.path.getctime)

def clean_dataframe(df):
    ''' Removes timestamp values and replaces NaN with None '''
    clean_df = df.copy()
    for col in clean_df.columns:
        if "Time Stamp" in col:  
            clean_df[col] = "IGNORE_TIMESTAMP"
    return clean_df.replace({np.nan: None})

def test_excel():
    run_command()
    new_file = find_latest_excel()
    new_df_dict = pd.read_excel(new_file, sheet_name=None)

    # Clean actual test data
    new_df_dict ={sheet: clean_dataframe(df) for sheet, df in new_df_dict.items()}

    sheet_names = list(new_df_dict.keys())
    for sheet_name in sheet_names[1:]:
        new_df_dict[sheet_name] = clean_dataframe(new_df_dict[sheet_name])

    # Validate sheet: Dataset Details
    assert 'Dataset Details' in new_df_dict, "Sheet 'Dataset Details' is missing"
    expected_columns = ['Dataset', 'Label', 'Location', 'Modified Time Stamp', 'Size (kb)', 'Number of Records']
    assert list(new_df_dict['Dataset Details'].columns) == expected_columns, "Column mismatch in 'Dataset Details'"

    assert clean_dataframe(new_df_dict['Dataset Details']).iloc[0].tolist() == ['fa.xpt', 'Findings About Events or Interventions', '.', 'IGNORE_TIMESTAMP', 0, 2], "Mismatch in 'Dataset Details', row 0"

    # Validate sheet: Issue Summary
    assert 'Issue Summary' in new_df_dict, "Sheet 'Issue Summary' is missing"
    expected_columns = ['Dataset', 'Dataset Domain', 'CORE-ID', 'Message', 'Issues', 'Explanation']
    assert list(new_df_dict['Issue Summary'].columns) == expected_columns, "Column mismatch in 'Issue Summary'"

    # Validate sheet: Issue Details
    assert 'Issue Details' in new_df_dict, "Sheet 'Issue Details' is missing"
    expected_columns = ['CORE-ID', 'Message', 'Executability', 'Dataset', 'Dataset Domain', 'USUBJID', 'Record', 'Sequence', 'Variable(s)', 'Value(s)']
    assert list(new_df_dict['Issue Details'].columns) == expected_columns, "Column mismatch in 'Issue Details'"

    # Validate sheet: Rules Report
    assert 'Rules Report' in new_df_dict, "Sheet 'Rules Report' is missing"
    expected_columns = ['CORE-ID', 'Version', 'CDISC RuleID', 'FDA RuleID', 'Message', 'Status']
    assert list(new_df_dict['Rules Report'].columns) == expected_columns, "Column mismatch in 'Rules Report'"

    assert clean_dataframe(new_df_dict['Rules Report']).iloc[0].tolist() == ['CORE-000159', 1, 'CG0341, TIG0506', None, "--TESTCD is equal to 'OTHER'", 'SUCCESS'], "Mismatch in 'Rules Report', row 0"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])
