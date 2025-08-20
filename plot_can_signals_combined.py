import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the decoded signals
excel_path = os.path.join('Output', 'decoded_can_signals.xlsx')
df = pd.read_excel(excel_path)

# Convert timestamp to float (seconds)
df['timestamp'] = df['timestamp'].astype(float)

# List of signals to plot
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

# Set seaborn style
sns.set(style="whitegrid")

plt.figure(figsize=(14, 7))
for sig in signals:
    plt.plot(df['timestamp'], df[sig], marker='o', label=sig)
plt.xlabel('Time (s)')
plt.ylabel('Signal Value')
plt.title('All Selected CAN Signals vs Time')
plt.legend()
plt.tight_layout()
report_path = os.path.join('Output', 'can_signals_all_in_one_plot.png')
plt.savefig(report_path)
plt.close()
print(f"Combined plot saved to {report_path}")

# Find the indices in the DataFrame that correspond to each 'read_CAN_signals' event (reading)
# We'll assume that the readings are spaced out in the DataFrame and you want to plot only those rows
# For demonstration, let's select every Nth row, where N is the number of rows between readings
# You may want to adjust this logic if you have a more precise way to identify the reading rows

# Example: If you know the indices of the readings, set them here
# For now, let's assume the first reading is at index 0, the second at index 6, the third at index 10, etc.
# You can update this list based on your actual test sequence timing
reading_indices = [0, 6, 10]  # Update this list as needed

output_dir = os.path.join('Output', 'can_signals_readings')
os.makedirs(output_dir, exist_ok=True)

for idx, row_idx in enumerate(reading_indices):
    row = df.iloc[row_idx]
    plt.figure(figsize=(10, 6))
    plt.bar(signals, [row[sig] for sig in signals], color=sns.color_palette("tab10", len(signals)))
    plt.xlabel('Signal')
    plt.ylabel('Value')
    plt.title(f'CAN Signals at Reading {idx+1} (t={row["timestamp"]:.3f}s)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plot_path = os.path.join(output_dir, f'reading_{idx+1}.png')
    plt.savefig(plot_path)
    plt.close()
print(f"Individual reading plots (bar charts) saved to {output_dir}")
