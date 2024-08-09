import pandas as pd
import os

def process_simulation_log(log_file):
    revocations = {}
    first_discards = {}

    with open(log_file, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            event_type = parts[0]
            timestamp = float(parts[1])
            vehicle_id = parts[2]

            if event_type == 'REVOCATION_START':
                revocations[vehicle_id] = timestamp
            elif event_type == 'MESSSAGE_DISCARDED':
                if vehicle_id not in first_discards:
                    first_discards[vehicle_id] = timestamp

    effective_revocation_times = []
    anomalies = []

    for vehicle_id, revoke_time in revocations.items():
        if vehicle_id in first_discards:
            discard_time = first_discards[vehicle_id]
            effective_time = discard_time - revoke_time
            if effective_time >= 0:
                effective_revocation_times.append((vehicle_id, effective_time))
            else:
                anomalies.append((vehicle_id, revoke_time, discard_time, effective_time))

    if anomalies:
        print("Anomalies detected:")
        for anomaly in anomalies:
            print(f"Vehicle ID: {anomaly[0]}, Revoke Time: {anomaly[1]}, Discard Time: {anomaly[2]}, Effective Time: {anomaly[3]}")

    return effective_revocation_times

log_file_path = 'active_revocation/interval/6_crl/active_revocations.txt'

effective_revocation_times = process_simulation_log(log_file_path)

df_revocation_times = pd.DataFrame(effective_revocation_times, columns=['Vehicle_ID', 'Effective_Revocation_Time'])

output_csv_path = os.path.join(os.path.dirname(log_file_path), 'active_times_6s_crl.csv')
df_revocation_times.to_csv(output_csv_path, index=False)

print(f"Revocation times saved to: {output_csv_path}")
