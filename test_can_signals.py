import pandas as pd
import numpy as np
import os

# Expected values for each reading (from TestInfo.txt)
expected_readings = [
    {
        'VSA_RR_ROT_DIRECTION_1': 3,
        'VSA_ABS_RL_WHEEL_SPEED_1': 0,
        'VSA_RL_ROT_DIRECTION_1': 3,
        'VSA_ABS_FL_WHEEL_SPEED_1': 0,
        'VSA_FR_ROT_DIRECTION_1': 3,
        'VSA_ABS_RR_WHEEL_SPEED_1': 0,
        'VSA_FL_ROT_DIRECTION_1': 3,
        'VSA_ABS_FR_WHEEL_SPEED_1': 0,
    },
    {
        'VSA_RR_ROT_DIRECTION_1': 1,
        'VSA_ABS_RL_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
        'VSA_RL_ROT_DIRECTION_1': 1,
        'VSA_ABS_FL_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
        'VSA_FR_ROT_DIRECTION_1': 1,
        'VSA_ABS_RR_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
        'VSA_FL_ROT_DIRECTION_1': 1,
        'VSA_ABS_FR_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
    },
    {
        'VSA_RR_ROT_DIRECTION_1': 2,
        'VSA_ABS_RL_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
        'VSA_RL_ROT_DIRECTION_1': 2,
        'VSA_ABS_FL_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
        'VSA_FR_ROT_DIRECTION_1': 2,
        'VSA_ABS_RR_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
        'VSA_FL_ROT_DIRECTION_1': 2,
        'VSA_ABS_FR_WHEEL_SPEED_1': 0,  # interval -oo < 0 < 30
    }
]

# Load the decoded signals
excel_path = os.path.join('Output', 'decoded_can_signals.xlsx')
assert os.path.exists(excel_path), f"Decoded signals file not found: {excel_path}"
df = pd.read_excel(excel_path)

# Find the rows corresponding to each reading (assuming the first 3 read_CAN_signals events)
# You may need to adjust the row indices depending on your extraction logic
# Here, we just take the first 3 rows for demonstration
for i, expected in enumerate(expected_readings):
    row = df.iloc[i]
    for sig, exp_val in expected.items():
        if 'WHEEL_SPEED' in sig:
            # For reading 2 and 3, interval check: -oo < 0 < 30 (value should be < 30)
            if i > 0:
                assert row[sig] < 30, f"{sig} at reading {i+1} is {row[sig]}, expected < 30"
            else:
                assert row[sig] == exp_val, f"{sig} at reading {i+1} is {row[sig]}, expected {exp_val}"
        else:
            assert row[sig] == exp_val, f"{sig} at reading {i+1} is {row[sig]}, expected {exp_val}"
print("All CAN signal values match expected results for the first 3 readings.")
