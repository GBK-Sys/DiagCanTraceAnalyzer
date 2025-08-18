import pandas as pd

def export_to_excel(inputs, responses, output_file='filtered_can_data.xlsx'):
    """
    Exports combined inputs and responses to a single Excel sheet.
    Args:
        inputs (list): List of input rows [Timestamp, CAN_ID, Type, DataLen, Data].
        responses (list): List of response rows [Timestamp, CAN_ID, Type, DataLen, Data].
        output_file (str): Output Excel file name.
    """
    combined_df = pd.DataFrame(inputs + responses, columns=['Timestamp', 'CAN_ID', 'Type', 'DataLen', 'Data'])
    combined_df.to_excel(output_file, index=False)
    print(f'Exported combined inputs and responses to {output_file}')
