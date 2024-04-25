import sys 
import os
import pandas as pd
from scapy.all import rdpcap
from decimal import Decimal



def analyze_pcap(pcap_file, gaurd_relay_ip):
    packets = rdpcap(pcap_file)
    data = []

    for packet in packets:
        if 'IP' in packet:
            size = len(packet)
            src = packet['IP'].src
            dst = packet['IP'].dst
            timestamp = float(packet.time)
            direction = 'incoming' if src == gaurd_relay_ip else 'outgoing'
            data.append([timestamp, src, dst, direction, size])


    df = pd.DataFrame(data, columns=['timestamp', 'src', 'dst', 'direction', 'size'])
    df['size'] = df['size'].astype(float)
    df['Time Interval'] = df['timestamp'].diff().astype(float)

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
        with pd.ExcelWriter(excel_file, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='Packet Data', index=False, startrow=writer.sheets['Packet Data'].max_row, header=False)
            pd.DataFrame([stats]).to_excel(writer, sheet_name='Statistics', index=False, startrow=writer.sheets['Statistics'].max_row, header=False)
    else:
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Packet Data', index=False)
            pd.DataFrame([stats]).to_excel(writer, sheet_name='Statistics', index=False)

    print(df)
    print(stats)

    print(f"Statistics Saved to Excel: {excel_file}")
    print(pd.DataFrame([stats]))
        
if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python data_analysis.py <pcap_file> <gaurd_relay_ip>')
        sys.exit(1)

    pcap_file = sys.argv[1]
    guard_relay_ip = sys.argv[2]
    main(pcap_file, guard_relay_ip)