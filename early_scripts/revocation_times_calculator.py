import pandas as pd
from collections import defaultdict
import os

def process_simulation_log(log_file):
    revocations = {}
    last_messages = defaultdict(float)

    # Read the log file
    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            event_type = parts[0]
            timestamp = float(parts[1])
            vehicle_id = parts[2]

            if event_type == 'REVOKE':
                revocations[vehicle_id] = timestamp
            elif event_type == 'RECV':
                last_messages[vehicle_id] = max(last_messages[vehicle_id], timestamp)

    # Calculate effective revocation times
    effective_revocation_times = []
    anomalies = []  # To log any anomalies

    for vehicle_id, revoke_time in revocations.items():
        if vehicle_id in last_messages:
            last_message_time = last_messages[vehicle_id]
            effective_time = last_message_time - revoke_time
            if effective_time >= 0:
                effective_revocation_times.append((vehicle_id, effective_time))
            else:
                anomalies.append((vehicle_id, revoke_time, last_message_time, effective_time))

    # Log anomalies
    if anomalies:
        print("Anomalies detected:")
        for anomaly in anomalies:
            print(f"Vehicle ID: {anomaly[0]}, Revoke Time: {anomaly[1]}, Last Message Time: {anomaly[2]}, Effective Time: {anomaly[3]}")

    return effective_revocation_times

# Specify the path to the log file
log_file_path = 'passive_revocation\/burst\/60\passive_revocation_log.txt'

# Process the log file
effective_revocation_times = process_simulation_log(log_file_path)

# Create DataFrame with Vehicle_ID and Effective_Revocation_Time
df_revocation_times = pd.DataFrame(effective_revocation_times, columns=['Vehicle_ID', 'Effective_Revocation_Time'])

# Set the output CSV file path in the same directory as the log file
output_csv_path = os.path.join(os.path.dirname(log_file_path), 'passive_times_60s.csv')
df_revocation_times.to_csv(output_csv_path, index=False)

print(f"Revocation times saved to: {output_csv_path}")
