import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['6s/6s/60s', '18s/18s/180s', '36s/36s/360s']
self_rev_mean = [7.85, 19.83, 28.97]
active_rev_mean = [10.65, 18.59, 46.38]
passive_rev_mean = [25.92, 86.54, 165.31]
self_rev_median = [6.87, 13.04, 25.46]
active_rev_median = [8.78, 12.97, 30.94]
passive_rev_median = [24.50, 85.64, 172.93]

# Set up the plot style
plt.style.use('seaborn-v0_8-paper')
plt.rcParams['font.family'] = 'serif'

# Create the figure and axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Function to create bars
def create_bars(ax, data1, data2, data3, title):
    x = np.arange(len(categories))
    width = 0.25
    
    ax.bar(x - width, data1, width, label='Self-Revocation', color='#1f77b4')
    ax.bar(x, data2, width, label='Active Revocation', color='#ff7f0e')
    ax.bar(x + width, data3, width, label='Passive Revocation', color='#2ca02c')
    
    ax.set_ylabel('Revocation Time (s)')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    
    # Add value labels on top of each bar
    for i, v in enumerate(data1):
        ax.text(i - width, v, f'{v:.2f}', ha='center', va='bottom')
    for i, v in enumerate(data2):
        ax.text(i, v, f'{v:.2f}', ha='center', va='bottom')
    for i, v in enumerate(data3):
        ax.text(i + width, v, f'{v:.2f}', ha='center', va='bottom')
    
    # Add x-axis label
    ax.set_xlabel('Parameter Set')

# Create the bar plots
create_bars(ax1, self_rev_mean, active_rev_mean, passive_rev_mean, '(a) Mean Effective Revocation Time')
create_bars(ax2, self_rev_median, active_rev_median, passive_rev_median, '(b) Median Effective Revocation Time')

# Adjust layout and display
plt.tight_layout()
plt.show()