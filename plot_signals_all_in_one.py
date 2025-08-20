import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the decoded signals
excel_path = os.path.join('Output', 'decoded_can_signals.xlsx')
df = pd.read_excel(excel_path)
df['timestamp'] = df['timestamp'].astype(float)

signals = [
    'VSA_RR_ROT_DIRECTION_1',
    'VSA_ABS_RL_WHEEL_SPEED_1',
    'VSA_RL_ROT_DIRECTION_1',
    'VSA_ABS_FL_WHEEL_SPEED_1',
    'VSA_FR_ROT_DIRECTION_1',
    'VSA_ABS_RR_WHEEL_SPEED_1',
    'VSA_FL_ROT_DIRECTION_1',
    'VSA_ABS_FR_WHEEL_SPEED_1',
]

# 2. All signals in one plot (for comparison)
plt.figure(figsize=(14, 7))
for sig in signals:
    plt.plot(df['timestamp'], df[sig], marker='o', label=sig)
plt.xlabel('Time (s)')
plt.ylabel('Signal Value')
plt.title('All Selected CAN Signals vs Time')
plt.legend()
plt.tight_layout()
report_path = os.path.join('Output', 'all_signals_vs_time.png')
plt.savefig(report_path)
plt.close()
print(f"All-signals-in-one plot saved to {report_path}")
