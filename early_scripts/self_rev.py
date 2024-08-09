import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from collections import defaultdict
import os

SIMULATION_LOG = 'simulation_log.txt'
HEARTBEAT_LOG = 'heartbeats.csv'
OUTPUT_DIR = 'output/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_simulation_log(log_file):
    revocations = {}
    last_messages = defaultdict(float)

    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts[0] == 'REVOKE':
                revocations[parts[2]] = float(parts[1])
            elif parts[0] == 'RECV':
                last_messages[parts[2]] = max(last_messages[parts[2]], float(parts[1]))

    effective_revocation_times = []
    for pseudo_hash, revoke_time in revocations.items():
        if pseudo_hash in last_messages:
            effective_time = last_messages[pseudo_hash] - revoke_time
            if effective_time > 0:
                effective_revocation_times.append(effective_time)

    return effective_revocation_times

def plot_revocation_times(times, T_v):
    df = pd.DataFrame(times, columns=['Time'])
    T_eff = 2 * T_v

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [3, 1]})
    sns.set_style("whitegrid")
    
    sns.boxplot(x=df['Time'], ax=ax1)
    sns.stripplot(x=df['Time'], color=".3", size=4, jitter=0.3, ax=ax1)

    mean = np.mean(df['Time'])
    median = np.median(df['Time'])
    
    ax1.axvline(mean, color='r', linestyle='--', label=f'Mean: {mean:.2f}s')
    ax1.axvline(median, color='g', linestyle=':', label=f'Median: {median:.2f}s')
    
    ax1.xaxis.grid(True, which='major', linestyle='--', color='gray', alpha=0.6)
    ax1.set_axisbelow(True)

    ax1.set_xlim(0, max(25, df['Time'].max() * 1.1))
    ax1.set_title('Effective revocation times', fontsize=16)
    ax1.set_xlabel('Time (seconds)', fontsize=14)
    ax1.legend(fontsize=12, loc='upper right')

    ax2.axvline(T_v, color='blue', linestyle='-', label=f'T_v: {T_v:.2f}s')
    ax2.axvline(T_eff, color='purple', linestyle='-', label=f'T_eff: {T_eff:.2f}s')
    ax2.axvline(df['Time'].max(), color='orange', linestyle='-', label=f'Max observed: {df["Time"].max():.2f}s')

    ax2.set_xlim(0, T_eff * 1.1)
    ax2.set_title('Theoretical bounds and Maximum observed time', fontsize=16)
    ax2.set_xlabel('Time (seconds)', fontsize=14)
    ax2.legend(fontsize=12, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'effective_revocation_time.png'), dpi=300)
    plt.close()

    print(f"Mean revocation time: {mean:.2f} seconds")
    print(f"Median revocation time: {median:.2f} seconds")
    print(f"Maximum revocation time: {df['Time'].max():.2f} seconds")
    print(f"Theoretical upper bound (T_eff): {T_eff:.2f} seconds")

def plot_network_overhead(csv_file):
    df = pd.read_csv(csv_file, names=['Time', 'Size'], skiprows=1)
    df['Size'] = pd.to_numeric(df['Size'], errors='coerce')
    df = df.dropna()

    df['Cumulative Size'] = df['Size'].cumsum()

    plt.figure(figsize=(14, 8))
    plt.style.use('default')

    fig, ax1 = plt.subplots(figsize=(14, 8))

    ax1.plot(df['Time'], df['Size'], linestyle='-', markersize=4, label='Message size (bytes)')
    ax1.set_xlabel('Simulation time (seconds)', fontsize=14)
    ax1.set_ylabel('Message size (bytes)', fontsize=14)
    ax1.tick_params(axis='y', labelsize=12)


    ax2 = ax1.twinx()
    ax2.plot(df['Time'], df['Cumulative Size'], color='g', linewidth=2, linestyle='--', label='Cumulative network overhead (bytes)')
    ax2.set_ylabel('Cumulative size (bytes)', fontsize=14)
    ax2.tick_params(axis='y', labelsize=12)

    plt.title('Network Overhead', fontsize=16)
    fig.tight_layout()

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=12, loc='lower right')

    total_data_kb = df['Cumulative Size'].iloc[-1] / 1024
    ax1.annotate(f'Total data: {total_data_kb:.2f} KB', xy=(0.90, 0.95), xycoords='axes fraction',
                 fontsize=12, color='blue', backgroundcolor='white')

    plt.savefig(os.path.join(OUTPUT_DIR, 'network_overhead_enhanced.png'), dpi=300)
    plt.close()

    avg_size = df['Size'].mean()
    max_size = df['Size'].max()

    print(f"Total data transmitted: {total_data_kb:.2f} KB")
    print(f"Average message size: {avg_size:.2f} bytes")
    print(f"Maximum message size: {max_size:.2f} bytes")

def main():
    revocation_times = process_simulation_log(SIMULATION_LOG)
    T_v = 180
    plot_revocation_times(revocation_times, T_v)
    plot_network_overhead(HEARTBEAT_LOG)

if __name__ == "__main__":
    main()