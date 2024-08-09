import pandas as pd
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 10

crl_6 = pd.read_csv('active_revocation/interval/6_crl/active_revocation_crl.csv')
crl_18 = pd.read_csv('active_revocation/interval/18_crl/active_revocation_crl.csv')
crl_36 = pd.read_csv('active_revocation/interval/36_crl/active_revocation_crl.csv')

hb_6 = pd.read_csv('self_revocation/interval/Tv_30s_HB_6s/heartbeats.csv')
hb_18 = pd.read_csv('self_revocation/interval/Tv_90s_HB_18s/heartbeats.csv')
hb_36 = pd.read_csv('self_revocation/interval/Tv_180s_HB_36s/heartbeats.csv')

crl_6 = crl_6.dropna(subset=['CRL Message Size'])
crl_18 = crl_18.dropna(subset=['CRL Message Size'])
crl_36 = crl_36.dropna(subset=['CRL Message Size'])

crl_6['Simulation Time'] = crl_6['Simulation Time'].astype(float)
crl_18['Simulation Time'] = crl_18['Simulation Time'].astype(float)
crl_36['Simulation Time'] = crl_36['Simulation Time'].astype(float)

plt.figure(figsize=(12, 8))

plt.plot(crl_6['Simulation Time'], crl_6['CRL Message Size'], 
         label='CRL Rate: 6s (Active)', linestyle='-', linewidth=2, color='#ff7f0e')
plt.plot(crl_18['Simulation Time'], crl_18['CRL Message Size'], 
         label='CRL Rate: 18s (Active)', linestyle='--', linewidth=2, color='#ff7f0e')
plt.plot(crl_36['Simulation Time'], crl_36['CRL Message Size'], 
         label='CRL Rate: 36s (Active)', linestyle=':', linewidth=2, color='#ff7f0e')

plt.plot(hb_6['Simulation Time'], hb_6['Message Size'], 
         label='HB Rate: 6s, Tv 30s (Self)', linestyle='-', linewidth=2, color='#1f77b4')
plt.plot(hb_18['Simulation Time'], hb_18['Message Size'], 
         label='HB Rate: 18s, Tv 90s (Self)', linestyle='--', linewidth=2, color='#1f77b4')
plt.plot(hb_36['Simulation Time'], hb_36['Message Size'], 
         label='HB Rate: 36s, Tv 180s (Self)', linestyle=':', linewidth=2, color='#1f77b4')

plt.xlabel('Simulation Time (s)')
plt.ylabel('Message Size (Bytes)')
plt.title('CRL vs HB Message Size Growth Over Time')
plt.legend()

#plt.savefig('crl_vs_hb_growth_comparison_styled.png', dpi=300, bbox_inches='tight')

plt.show()
