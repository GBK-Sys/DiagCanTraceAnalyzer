import os
import zipfile
import io
import re
import pandas as pd
from export_utils import export_to_excel

input_id = '18DA28F1x'   # Replace with your input CAN ID (as string, no '0x')
output_id = '18DAF128x'  # Replace with your output CAN ID
pattern = re.compile(r'^\s*(\d+\.\d+)\s+(\w+)\s+(\w+)\s+Rx\s+d\s+(\d+)\s+((?:\w+\s+)+)')

zip_folder = 'Data'
output_excel = os.path.join('Output', 'all_filtered_can_data.xlsx')

# Collect all zip files in the Data folder
zip_files = [os.path.join(zip_folder, f) for f in os.listdir(zip_folder) if f.endswith('.zip')]

with pd.ExcelWriter(output_excel) as writer:
    for zip_path in zip_files:
        zip_name = os.path.splitext(os.path.basename(zip_path))[0]
        with zipfile.ZipFile(zip_path, 'r') as z:
            # Find the first .asc file in the zip
            asc_files = [name for name in z.namelist() if name.lower().endswith('.asc')]
            if not asc_files:
                print(f'No .asc file found in {zip_path}')
                continue
            asc_file = asc_files[0]
            with z.open(asc_file) as f:
                responses = []
                inputs = []
                collecting_multiline = False
                multiline_data = []
                expected_length = 0
                multiline_start_time = None
                for line in io.TextIOWrapper(f, encoding='utf-8', errors='ignore'):
                    match = pattern.match(line)
                    if match:
                        timestamp, channel, can_id, dlc, data = match.groups()
                        can_id = can_id.upper()
                        data_bytes = data.strip().split()[:int(dlc)]
                        if can_id == output_id.upper():
                            if data_bytes and data_bytes[0].upper() == '10':
                                collecting_multiline = True
                                multiline_data = data_bytes[2:]
                                expected_length = int(data_bytes[1], 16)
                                multiline_start_time = timestamp
                                responses.append([timestamp, can_id, 'MULTILINE_START', expected_length, ' '.join(data_bytes)])
                            elif collecting_multiline and data_bytes and data_bytes[0].startswith('2'):
                                multiline_data.extend(data_bytes[1:])
                                responses.append([timestamp, can_id, 'MULTILINE_CONT', expected_length, ' '.join(data_bytes)])
                            else:
                                if collecting_multiline:
                                    responses.append([multiline_start_time, can_id, 'MULTILINE_END', expected_length, ' '.join(multiline_data[:expected_length])])
                                    collecting_multiline = False
                                    multiline_data = []
                                    expected_length = 0
                                    multiline_start_time = None
                                responses.append([timestamp, can_id, 'SINGLE', len(data_bytes), ' '.join(data_bytes)])
                        elif can_id == input_id.upper():
                            inputs.append([timestamp, can_id, 'SINGLE', len(data_bytes), ' '.join(data_bytes)])
                if collecting_multiline:
                    responses.append([multiline_start_time, output_id.upper(), 'MULTILINE_END', expected_length, ' '.join(multiline_data[:expected_length])])
                # Combine and export to a sheet named after the zip file
                combined_df = pd.DataFrame(inputs + responses, columns=['Timestamp', 'CAN_ID', 'Type', 'DataLen', 'Data'])
                combined_df.to_excel(writer, sheet_name=zip_name[:31], index=False)  # Excel sheet names max 31 chars
print(f'Exported all data to {output_excel}')