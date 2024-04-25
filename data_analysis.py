import sys 
import os
import pandas as pd
from scapy.all import *


def analyze_pcap(pcap_file, gaurd_relay_ip):
    packets = rdpcap(pcap_file)
    data = []

    for packet in packets:
        if 'IP' in packet:
            size = len(packet)
            src = packet['IP'].src
            dst = packet['IP'].dst
            timestamp = packet.time
            direction = 'incoming' if src == gaurd_relay_ip else 'outgoing'
            data.append([timestamp, src, dst, direction, size])


            df = pd.DataFrame(data, columns=['timestamp', 'src', 'dst', 'direction', 'size'])

            stats = {
                'Mean Packet Size': df['size'].mean(),
                'Median Packet Size': df['size'].median(),
                'Std Packet Size': df['size'].std(),
                'Mean Time Interval': df['timestamp'].diff().mean(),
                'Median Time Interval': df['timestamp'].diff().median(),
                'Std deviation Time Interval': df['timestamp'].diff().std(),
                'Total Packets': len(df),
                'Total Bytes': df['size'].sum(),
            }

            return df, stats
        
def main (pcap_file, gaurd_relay_ip):
    df, stats = analyze_pcap(pcap_file, gaurd_relay_ip)
    excel_file = 'pcap_analysis.xlsx'

    if os.path.exists(excel_file):
        with pd.ExcelWriter(excel_file, mode='a') as writer:
            df.to_excel(writer, sheet_name='pcap_data', index=False)
            pd.Series(stats).to_frame('value').to_excel(writer, sheet_name='stats')
    else:
        with pd.ExcelWriter(excel_file) as writer:
            df.to_excel(writer, sheet_name='pcap_data', index=False)
            pd.Series(stats).to_frame('value').to_excel(writer, sheet_name='stats')

    print(df)
    print(stats)

    print(f"Statistics Saved to Excel: {excel_file}")
    print(pd.DataFrame([stats]))
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python data_analysis.py <pcap_file> <gaurd_relay_ip>')
        sys.exit(1)