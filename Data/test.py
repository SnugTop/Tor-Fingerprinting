import os
import pandas as pd
from scapy.all import rdpcap
import joblib

def analyze_pcap(pcap_file, guard_relay_ip):
    packets = rdpcap(pcap_file)
    data = []

    for packet in packets:
        if 'IP' in packet:
            size = len(packet)
            src = packet['IP'].src
            dst = packet['IP'].dst
            timestamp = float(packet.time)
            direction = 'incoming' if src == guard_relay_ip else 'outgoing'
            data.append([timestamp, src, dst, direction, size])

    df = pd.DataFrame(data, columns=['timestamp', 'src', 'dst', 'direction', 'size'])
    df['size'] = df['size'].astype(float)
    df['Time Interval'] = df['timestamp'].diff().astype(float)

    stats = {
        'Mean Packet Size': df['size'].mean(),
        'Median Packet Size': df['size'].median(),
        'Std Packet Size': df['size'].std(),
        'Mean Time Interval': df['Time Interval'].mean(),
        'Median Time Interval': df['Time Interval'].median(),
        'Std deviation Time Interval': df['Time Interval'].std(),
        'Total Packets': len(df),
        'Total Bytes': df['size'].sum(),
    }

    return pd.DataFrame([stats]) 

def load_model_and_scaler(model_path, scaler_path):
    knn_model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    return knn_model, scaler

def main(directory_path):
    guard_relay_ip = '85.208.144.164' 
    model_path = 'knn_model.joblib'
    scaler_path = 'scaler.joblib'
    knn_model, scaler = load_model_and_scaler(model_path, scaler_path)

    for filename in os.listdir(directory_path):
        if filename.endswith('.pcap'):
            full_path = os.path.join(directory_path, filename)
            pcap_stats = analyze_pcap(full_path, guard_relay_ip)
            pcap_stats_scaled = scaler.transform(pcap_stats)
            prediction = knn_model.predict(pcap_stats_scaled)
            print(f"{filename}: Prediction - {prediction}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('Usage: python test.py <directory_path>')
        sys.exit(1)

    directory_path = sys.argv[1]
    main(directory_path)
