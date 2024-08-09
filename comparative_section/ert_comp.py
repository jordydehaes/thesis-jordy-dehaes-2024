import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

crl_6 = pd.read_csv('active_revocation/interval/6_crl/active_revocation_crl.csv')
crl_18 = pd.read_csv('active_revocation/interval/18_crl/active_revocation_crl.csv')
crl_36 = pd.read_csv('active_revocation/interval/36_crl/active_revocation_crl.csv')

prl_6 = pd.read_csv('self_revocation/interval/Tv_30s_HB_6s/heartbeats.csv')
prl_18 = pd.read_csv('self_revocation/interval/Tv_90s_HB_18s/heartbeats.csv')
prl_36 = pd.read_csv('self_revocation/interval/Tv_180s_HB_36s/heartbeats.csv')

crl_6 = crl_6.dropna(subset=['CRL Message Size'])
crl_18 = crl_18.dropna(subset=['CRL Message Size'])
crl_36 = crl_36.dropna(subset=['CRL Message Size'])

crl_6['Simulation Time'] = crl_6['Simulation Time'].astype(float)
crl_18['Simulation Time'] = crl_18['Simulation Time'].astype(float)
crl_36['Simulation Time'] = crl_36['Simulation Time'].astype(float)

plt.figure(figsize=(12, 8))

plt.plot(crl_6['Simulation Time'], crl_6['CRL Message Size'], 
         label='CRL Rate: 6s (Active)', linestyle='-', linewidth=2, color='#2ca02c')
plt.plot(crl_18['Simulation Time'], crl_18['CRL Message Size'], 
         label='CRL Rate: 18s (Active)', linestyle='-', linewidth=2, color='#2ca02c')
plt.plot(crl_36['Simulation Time'], crl_36['CRL Message Size'], 
         label='CRL Rate: 36s (Active)', linestyle='-', linewidth=2, color='#2ca02c')

plt.plot(prl_6['Simulation Time'], prl_6['Message Size'], 
         label='PRL Rate: HB 6s, Tv 30s (Self)', linestyle='--', linewidth=2, color='#1f77b4')
plt.plot(prl_18['Simulation Time'], prl_18['Message Size'], 
         label='PRL Rate: HB 18s, Tv 90s (Self)', linestyle='--', linewidth=2, color='#1f77b4')
plt.plot(prl_36['Simulation Time'], prl_36['Message Size'], 
         label='PRL Rate: HB 36s, Tv 180s (Self)', linestyle='--', linewidth=2, color='#1f77b4')

plt.xlabel('Simulation Time (s)')
plt.ylabel('Message Size (Bytes)')
plt.title('CRL vs PRL Message Size Growth Over Time')
plt.legend()

#plt.savefig('crl_vs_prl_growth_comparison_styled.png', dpi=300, bbox_inches='tight')

plt.show()
