import pandas as pd

revocation_file = "passive_revocation\/burst\/60\passive_times_60s.csv"
df_revocation = pd.read_csv(revocation_file)

mean_revocation_time = df_revocation['Effective_Revocation_Time'].mean()
median_revocation_time = df_revocation['Effective_Revocation_Time'].median()
max_revocation_time = df_revocation['Effective_Revocation_Time'].max()

print(f"Mean revocation time: {mean_revocation_time:.2f} seconds")
print(f"Median revocation time: {median_revocation_time:.2f} seconds")
print(f"Maximum revocation time: {max_revocation_time:.2f} seconds")

message_file = "passive_revocation\/burst\/60\passive_revocation_metrics.csv"
df_message = pd.read_csv(message_file)

total_data_bytes = df_message['Message Size'].sum()
total_data_kb = total_data_bytes / 1024  # convert to KB
avg_message_size = df_message['Message Size'].mean()
max_message_size = df_message['Message Size'].max()

print(f"Total data transmitted: {total_data_kb:.2f} KB")
print(f"Average message size: {avg_message_size:.2f} bytes")
print(f"Maximum message size: {max_message_size:.2f} bytes")
