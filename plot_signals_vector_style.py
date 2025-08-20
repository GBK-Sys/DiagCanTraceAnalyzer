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

# 1. One plot per signal (like Vector tool)
output_dir = os.path.join('Output', 'vector_style_signals')
os.makedirs(output_dir, exist_ok=True)
for sig in signals:
    plt.figure(figsize=(12, 4))
    plt.plot(df['timestamp'], df[sig], marker='o', label=sig)
    plt.xlabel('Time (s)')
    plt.ylabel(sig)
    plt.title(f'{sig} vs Time')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{sig}_vs_time.png'))
    plt.close()
print(f"Vector-style signal plots saved to {output_dir}")
