import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10

self_rev_time = [7.85, 19.83, 28.97]
self_rev_overhead = [175.15, 63.66, 32.16]
active_rev_time = [10.65, 18.59, 46.38]
active_rev_overhead = [350.45, 116.66, 56.70]
passive_rev_time = [25.92, 86.54, 165.31]
passive_rev_overhead = [3475.05, 1622.35, 594.45]

colors = {'Self': '#1f77b4', 'Active': '#ff7f0e', 'Passive': '#2ca02c'}
markers = {'Self': 'o', 'Active': 's', 'Passive': '^'}

fig, ax = plt.subplots(figsize=(10, 6))

schemes = [('Self', self_rev_time, self_rev_overhead),
           ('Active', active_rev_time, active_rev_overhead),
           ('Passive', passive_rev_time, passive_rev_overhead)]

for scheme, times, overheads in schemes:
    ax.scatter(times, overheads, label=f'{scheme} Revocation', marker=markers[scheme], s=80, color=colors[scheme], alpha=0.8)
    ax.plot(times, overheads, '--', color=colors[scheme], alpha=0.5)

    for i, (x, y) in enumerate(zip(times, overheads)):
        ax.annotate(f'({x:.2f}, {y:.2f})', (x, y), textcoords="offset points", xytext=(5,5), ha='left', va='bottom', fontsize=8)

ax.set_xlabel('Mean Effective Revocation Time (s)')
ax.set_ylabel('Total Network Overhead (KB)')
ax.set_title('Trade-off: Revocation Time vs. Network Overhead')
ax.legend(frameon=True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.set_yscale('log')

plt.tight_layout()
#plt.savefig('scatter_revoc_vs_overhead.png', dpi=300, bbox_inches='tight')
plt.show()