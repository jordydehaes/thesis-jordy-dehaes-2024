import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14

file_paths = {
    'Active': [
        r'active_revocation\interval\6_crl\active_times_6s_crl.csv',
        r'active_revocation\interval\18_crl\active_times_18s_crl.csv',
        r'active_revocation\interval\36_crl\active_times_36s_crl.csv'
    ],
    'Passive': [
        r'passive_revocation\interval\60\passive_times_60s.csv',
        r'passive_revocation\interval\180\passive_times_180s.csv',
        r'passive_revocation\interval\360\passive_times_360s.csv'
    ],
    'Self': [
        r'self_revocation\interval\Tv_30s_HB_6s\self_times_Tv_30s_HB_6s.csv',
        r'self_revocation\interval\Tv_90s_HB_18s\self_times_Tv_90s_HB_18s.csv',
        r'self_revocation\interval\Tv_180s_HB_36s\self_times_Tv_180s_HB_36s.csv'
    ]
}

params = ['6s/30s/60s', '18s/90s/180s', '36s/180s/360s']
colors = {'Self': 'blue', 'Active': 'orange', 'Passive': 'green'}

data = []
for scheme, files in file_paths.items():
    for i, file_path in enumerate(files):
        df = pd.read_csv(file_path)
        df['Scheme'] = scheme
        df['Parameters'] = params[i]
        data.append(df)

all_data = pd.concat(data, ignore_index=True)

plt.figure(figsize=(12, 6))
sns.boxplot(x='Parameters', y='Effective_Revocation_Time', hue='Scheme', data=all_data, 
            palette=colors, whis=[5, 95], showfliers=False)

plt.xlabel('Parameters')
plt.ylabel('Revocation Time (s)')
plt.title('Distribution of Revocation Times for All Schemes and Parameters')
plt.legend(title='Scheme')
plt.tight_layout()
#plt.savefig('revocation_time_boxplot.pdf', format='pdf', dpi=300, bbox_inches='tight')
plt.show()