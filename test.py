import re
import csv

asc_file = 'STEPS_network_trace_20250430_175108.asc'  # Replace with your .asc file path
output_csv = 'filtered_can_data.csv'
input_id = '18DA28F1x'   # Replace with your input CAN ID (as string, no '0x')
output_id = '18DAF128x'  # Replace with your output CAN ID

pattern = re.compile(r'^\s*(\d+\.\d+)\s+(\w+)\s+(\w+)\s+Rx\s+d\s+(\d+)\s+((?:\w+\s+)+)')

filtered_rows = []

with open(asc_file, 'r') as f:
    response_data = []
    input_data = []
    collecting_multiline = False
    multiline_data = []
    expected_length = 0
    for line in f:
        match = pattern.match(line)
        if match:
            timestamp, channel, can_id, dlc, data = match.groups()
            can_id = can_id.upper()
            data_bytes = data.strip().split()[:int(dlc)]
            if can_id == output_id.upper():
                # Check for start of multi-line (first frame, ISO-TP: 10)
                if data_bytes and data_bytes[0].upper() == '10':
                    collecting_multiline = True
                    multiline_data = data_bytes[2:]  # skip '10' and length byte
                    expected_length = int(data_bytes[1], 16)
                # Continuation frames (ISO-TP: 21, 22, ...)
                elif collecting_multiline and data_bytes and data_bytes[0].startswith('2'):
                    multiline_data.extend(data_bytes[1:])  # skip the sequence byte
                else:
                    # Not a multi-line, or end of multi-line
                    if collecting_multiline:
                        response_data = multiline_data[:expected_length]
                        collecting_multiline = False
                    else:
                        response_data = data_bytes
                filtered_rows.append([timestamp, can_id, dlc] + data_bytes)
            elif can_id == input_id.upper():
                input_data.extend(data_bytes)
                filtered_rows.append([timestamp, can_id, dlc] + data_bytes)
    # If file ends while collecting multiline
    if collecting_multiline:
        response_data = multiline_data[:expected_length]

# Print all response data in one line
if response_data:
    print('All response data in one line:')
    print(' '.join(response_data))
else:
    print('No response data found for output_id.')

# Print all input data in one line
if input_data:
    print('All input data in one line:')
    print(' '.join(input_data))
else:
    print('No input data found for input_id.')

"""
# Write to CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Timestamp', 'CAN_ID', 'DLC', 'DataBytes...'])
    writer.writerows(filtered_rows)

    """

print(f"Exported {len(filtered_rows)} rows to {output_csv}")