import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

file_paths = {
    'Self': [
        r'self_revocation\interval\Tv_30s_HB_6s\self_times_Tv_30s_HB_6s.csv',
        r'self_revocation\interval\Tv_90s_HB_18s\self_times_Tv_90s_HB_18s.csv',
        r'self_revocation\interval\Tv_180s_HB_36s\self_times_Tv_180s_HB_36s.csv'
    ],
    'Active': [
        r'active_revocation\interval\6_crl\active_times_6s_crl.csv',
        r'active_revocation\interval\18_crl\active_times_18s_crl.csv',
        r'active_revocation\interval\36_crl\active_times_36s_crl.csv'
    ],
    'Passive': [
        r'passive_revocation\interval\60\passive_times_60s.csv',
        r'passive_revocation\interval\180\passive_times_180s.csv',
        r'passive_revocation\interval\360\passive_times_360s.csv'
    ]
}

params = {
    'Self': ['6s', '18s', '36s'],
    'Active': ['6s', '18s', '36s'],
    'Passive': ['60s', '180s', '360s']
}
colors = {'Self': '#1f77b4', 'Active': '#ff7f0e', 'Passive': '#2ca02c'}
styles = {0: '-', 1: '--', 2: ':'}

# T_v values for self-revocation
T_v_values = [30, 90, 180]
T_eff_color = 'red'

plt.figure(figsize=(12, 6))

for scheme, files in file_paths.items():
    for i, file_path in enumerate(files):
        df = pd.read_csv(file_path)
        
        sorted_data = np.sort(df['Effective_Revocation_Time'])
        yvals = np.arange(len(sorted_data))/float(len(sorted_data)-1)
        
        plt.plot(sorted_data, yvals, color=colors[scheme], linestyle=styles[i], 
                 label=f'{scheme} - {params[scheme][i]}')

# Plot T_eff lines separately
for i, T_v in enumerate(T_v_values):
    T_eff = 2 * T_v
    plt.axvline(x=T_eff, color=T_eff_color, linestyle=styles[i], alpha=0.5,
                label=f'$T_{{eff}} = {T_eff}s$')

plt.xlabel('Revocation Time (s)')
plt.ylabel('Cumulative Probability')
plt.title('CDF of Revocation Times for All Schemes and Parameters')

plt.legend(loc='upper right')

plt.tight_layout()
#plt.savefig('cdf_revocation.png', dpi=300, bbox_inches='tight')
plt.show()
