import os
import cantools
import re
import pandas as pd
import numpy as np

dbc_folder = 'DBCFiles'
dbc_files = [os.path.join(dbc_folder, f) for f in os.listdir(dbc_folder) if f.endswith('.dbc')]

db_list = []
for dbc in dbc_files:
    try:
        db_list.append(cantools.database.load_file(dbc))
    except Exception as e:
        print(f"Failed to load {dbc}: {e}")

# Print all available signals from all loaded DBCs
print('Available signals:')
for db in db_list:
    for msg in db.messages:
        print(f"Message: {msg.name} (ID: {hex(msg.frame_id)})")
        for sig in msg.signals:
            print(f"  Signal: {sig.name}")

# Read the ASC file
asc_path = os.path.join('Data', '0091_RB_UNIVERSAL_01J-7_24_CheckWheelRotationDirection_D_R_tcdoc', 'STEPS_network_trace_20250430_205417.asc')
output_excel = os.path.join('Output', 'decoded_can_signals.xlsx')

# Only extract these signals (from TestInfo.txt readings)
selected_signals = [
    'VSA_RR_ROT_DIRECTION_1',
    'VSA_ABS_RL_WHEEL_SPEED_1',
    'VSA_RL_ROT_DIRECTION_1',
    'VSA_ABS_FL_WHEEL_SPEED_1',
    'VSA_FR_ROT_DIRECTION_1',
    'VSA_ABS_RR_WHEEL_SPEED_1',
    'VSA_FL_ROT_DIRECTION_1',
    'VSA_ABS_FR_WHEEL_SPEED_1',
]

# Build a set of all possible signal names (but only keep selected_signals)
all_signals = selected_signals

records = []
if not os.path.exists(asc_path):
    print(f"ASC file not found: {asc_path}")
else:
    print(f"\nReading CAN messages from: {asc_path}\n")
    # Regex to match CANalyzer ASC lines
    asc_pattern = re.compile(r"^\s*(\d+\.\d+)\s+\d+\s+([0-9A-Fa-f]+)\s+Rx\s+d\s+(\d+)\s+((?:[0-9A-Fa-f]{2} ?)+)")
    with open(asc_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            match = asc_pattern.match(line)
            if match:
                timestamp, can_id_hex, dlc, data_str = match.groups()
                can_id = int(can_id_hex, 16)
                data_bytes = bytes(int(b, 16) for b in data_str.strip().split())
                decoded = None
                for db in db_list:
                    try:
                        decoded = db.decode_message(can_id, data_bytes)
                        break
                    except Exception:
                        continue
                # Only store timestamp and selected signals
                row = {'timestamp': timestamp}
                if decoded:
                    for sig in all_signals:
                        row[sig] = decoded.get(sig, np.nan)
                else:
                    for sig in all_signals:
                        row[sig] = np.nan
                records.append(row)
    if records:
        df = pd.DataFrame(records)
        os.makedirs('Output', exist_ok=True)
        df.to_excel(output_excel, index=False)
        print(f"Full time series of selected signals saved to {output_excel}")
    else:
        print("No signals decoded.")
