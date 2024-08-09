import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

parameters = ['6s/30s/60s', '18s/90s/180s', '36s/180s/360s']
self_rev_total = [175.15, 63.66, 32.16]
self_rev_avg = [510.97, 538.78, 577.82]
active_rev_total = [350.45, 116.66, 56.70]
active_rev_avg = [1025.30, 911.88, 967.73]
passive_rev_total = [3475.05, 1622.35, 594.45]
passive_rev_avg = [345.55, 331.66, 375.52]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

def plot_lines(ax, data1, data2, data3, ylabel):
    ax.plot(parameters, data1, marker='o', label='Self-Revocation', color='#1f77b4', linewidth=2, markersize=8)
    ax.plot(parameters, data2, marker='s', label='Active Revocation', color='#ff7f0e', linewidth=2, markersize=8)
    ax.plot(parameters, data3, marker='^', label='Passive Revocation', color='#2ca02c', linewidth=2, markersize=8)
    
    ax.set_ylabel(ylabel)
    ax.legend(loc='best', frameon=True)
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    for i, (d1, d2, d3) in enumerate(zip(data1, data2, data3)):
        ax.annotate(f'{d1:.2f}', (i, d1), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)
        ax.annotate(f'{d2:.2f}', (i, d2), textcoords="offset points", xytext=(0,-15), ha='center', fontsize=8)
        ax.annotate(f'{d3:.2f}', (i, d3), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

plot_lines(ax1, self_rev_total, active_rev_total, passive_rev_total, 'Total Network Overhead (KB)')
ax1.set_title('(a) Total Network Overhead')
ax1.set_yscale('log')

plot_lines(ax2, self_rev_avg, active_rev_avg, passive_rev_avg, 'Average Message Size (B)')
ax2.set_title('(b) Average Message Size')

plt.tight_layout()
#plt.savefig('network_overhead_comparison.png', dpi=300, bbox_inches='tight')
plt.show()