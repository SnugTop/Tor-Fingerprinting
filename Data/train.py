import pandas as pd
from joblib import dump, load
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier

def load_and_preprocess_data(filepath):
    data = pd.read_excel(filepath, sheet_name='Statistics')
    X = data[['Mean Packet Size', 'Median Packet Size', 'Std Packet Size', 'Mean Time Interval', 'Median Time Interval', 'Std deviation Time Interval', 'Total Packets', 'Total Bytes']]
    y = data['Website']
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler


def train_knn(X, y, scaler, k=4):  
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(X, y)
    return knn, scaler  

def main():
    filepath = 'pcap_analysis.xlsx'  
    X_scaled, y, scaler = load_and_preprocess_data(filepath)
    knn_model, scaler = train_knn(X_scaled, y, scaler)  

    dump(knn_model, 'knn_model.joblib')
    dump(scaler, 'scaler.joblib')


if __name__ == '__main__':
    main()
