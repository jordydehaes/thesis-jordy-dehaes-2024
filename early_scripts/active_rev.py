import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os

ACTIVE_REVOCATION_CRL_LOG = 'active_revocation_crl.csv'
ACTIVE_REVOCATIONS_LOG = 'active_revocations.txt'
OUTPUT_DIR = 'output/'

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_active_revocations(log_file):
    revocations = {}
    first_message_discard = {}

    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if parts[0] == 'REVOCATION_START':
                revocations[parts[2]] = float(parts[1])
            elif parts[0] == 'MESSSAGE_DISCARDED':
                if parts[2] not in first_message_discard:
                    first_message_discard[parts[2]] = float(parts[1])

    effective_revocation_times = []
    for pseudo_hash, revoke_time in revocations.items():
        if pseudo_hash in first_message_discard:
            effective_time = first_message_discard[pseudo_hash] - revoke_time
            if effective_time > 0:
                effective_revocation_times.append(effective_time)

    return effective_revocation_times

def plot_active_revocation_times(times):
    if not times:
        print("No effective revocation times to plot.")
        return

    df = pd.DataFrame(times, columns=['Time'])

    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")
    
    sns.boxplot(x=df['Time'], ax=ax)
    sns.stripplot(x=df['Time'], color=".3", size=4, jitter=0.3, ax=ax)

    mean = np.mean(df['Time'])
    median = np.median(df['Time'])
    
    ax.axvline(mean, color='r', linestyle='--', label=f'Mean: {mean:.2f}s')
    ax.axvline(median, color='g', linestyle=':', label=f'Median: {median:.2f}s')
    
    ax.xaxis.grid(True, which='major', linestyle='--', color='gray', alpha=0.6)
    ax.set_axisbelow(True)

    ax.set_xlim(0, max(25, df['Time'].max() * 1.1))
    ax.set_title('Effective active revocation times', fontsize=16)
    ax.set_xlabel('Time (seconds)', fontsize=14)
    ax.legend(fontsize=12, loc='upper right')

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'effective_active_revocation_time.png'), dpi=300)
    plt.close()

    print(f"Mean active revocation time: {mean:.2f} seconds")
    print(f"Median active revocation time: {median:.2f} seconds")
    print(f"Maximum active revocation time: {df['Time'].max():.2f} seconds")

def plot_active_revocation_network_overhead(csv_file):
    try:
        df = pd.read_csv(csv_file, names=['Simulation Time', 'CRL Size', 'CRL Message Size'], skiprows=1)
    except pd.errors.EmptyDataError:
        print(f"No data found in {csv_file}.")
        return

    df['CRL Message Size'] = pd.to_numeric(df['CRL Message Size'], errors='coerce')
    df = df.dropna(subset=['CRL Message Size'])

    if df.empty:
        print("No valid data to plot in 'CRL Message Size'.")
        return

    df['Cumulative Size'] = df['CRL Message Size'].cumsum()

    plt.figure(figsize=(14, 8))
    plt.style.use('default')

    fig, ax1 = plt.subplots(figsize=(14, 8))

    ax1.plot(df['Simulation Time'], df['CRL Message Size'], linestyle='-', markersize=4, label='CRL Message Size (bytes)')
    ax1.set_xlabel('Simulation Time (seconds)', fontsize=14)
    ax1.set_ylabel('CRL Message Size (bytes)', fontsize=14)
    ax1.tick_params(axis='y', labelsize=12)

    ax2 = ax1.twinx()
    ax2.plot(df['Simulation Time'], df['Cumulative Size'], color='g', linewidth=2, linestyle='--', label='Cumulative Network Overhead (bytes)')
    ax2.set_ylabel('Cumulative Size (bytes)', fontsize=14)
    ax2.tick_params(axis='y', labelsize=12)


    plt.title('Active Revocation Network Overhead', fontsize=16)
    fig.tight_layout()

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=12, loc='lower right')

    total_data_kb = df['Cumulative Size'].iloc[-1] / 1024
    ax1.annotate(f'Total data: {total_data_kb:.2f} KB', xy=(0.05, 0.95), xycoords='axes fraction',
                 fontsize=12, color='blue', backgroundcolor='white')

    plt.savefig(os.path.join(OUTPUT_DIR, 'active_revocation_network_overhead_enhanced.png'), dpi=300)
    plt.close()

    avg_size = df['CRL Message Size'].mean()
    max_size = df['CRL Message Size'].max()

    print(f"Total data transmitted: {total_data_kb:.2f} KB")
    print(f"Average CRL message size: {avg_size:.2f} bytes")
    print(f"Maximum CRL message size: {max_size:.2f} bytes")

def main():
    active_revocation_times = process_active_revocations(ACTIVE_REVOCATIONS_LOG)
    plot_active_revocation_times(active_revocation_times)
    plot_active_revocation_network_overhead(ACTIVE_REVOCATION_CRL_LOG)

if __name__ == "__main__":
    main()
