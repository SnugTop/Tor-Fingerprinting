# Network Traffic Analysis Tool

This repository contains tools for analyzing network traffic captured in PCAP files to classify and predict web activities based on traffic patterns. These tools use Python for data extraction, analysis, and machine learning to identify characteristics of different websites visited through Tor networks.

## Components

- **data_analysis.py**: Extracts packet information from PCAP files, determines the direction of traffic based on known guard relay IPs, and stores statistical analysis in an Excel file.
- **train.py**: Trains a K-Nearest Neighbors (KNN) classifier to predict the website based on network traffic characteristics.
- **test.py**: Predicts the website from new PCAP files using the trained KNN model.

## Dependencies

- Python 3.7+
- pandas
- scapy
- joblib
- sklearn
- openpyxl

If using google cloud virtual machine you will need to run a python virtual environment to install these dependencies.

```bash
sudo apt install python3-venv
python3 -m venv myenv
source myenv/bin/activate
```

You can install these dependencies using pip:

```bash
pip install pandas scapy joblib scikit-learn openpyxl
```

# Setup and Execution

## Data Analysis

Run data_analysis.py to parse PCAP files and generate a dataset:

```bash
python data_analysis.py <directory_path_containing_pcap_files>
```

directory for pcaps to be analyze is "pcaps" in this repo, but may be whatever you name it.

This script will:

Analyze packets to determine if they are incoming or outgoing based on a list of known guard relay IPs.
Compute statistics such as mean packet size and total bytes.
Save these statistics to pcap_analysis.xlsx.

I commented out two lines of code that recored the packet data as well in the excel. It can be recorded in a sheet called "Packet Data" as sanity check to make sure the data is being recorded correctly. It slows down the process and is uneccessary so it is not needed.The "statistics" are the only data used in training the model.

For statistics I chose Mean Packet Size, Median Packet Size, Standard Dev in Packet Size, Mean Time Interval, Median Time Interval, Std Deviation Time Interval, Total Packets, and Total Bytes.

## Training

Execute train.py to train the model using the generated dataset:

```bash
python train.py
```

This will:

Load data from pcap_analysis.xlsx.

Scale features using standardization. I chose to scale the features because I did not want the difference in units to mess up the training or decision-making process.

Train a KNN classifier and save the model and scaler to disk.

## Testing

Use test.py to predict the website from new PCAP files:

```bash
python test.py <directory_path_containing_test_files>
```

The directory for pcaps used for testing is "tests" in this repo, but may be whatever you name it.

This script will:

Analyze the new PCAP files in this directory using the trained model.
Output predictions for each file to the terminal. It will run for all five files outputting the predictions.

# Why KNN and Choice of K

I chose the KNN algorithm for its effectiveness in classification problems the data sets are not big enough for other methods. I chose the number 4 for K because it gives us the best balance when making these comparisons. If I pick a number that's too high, it might include too many neighbors that aren't similar(noise). But if I pick a number that's too low, it might not get enough information to make a good decision. The number 4 seemed to work best in our tests to keep things just right.

# Decision Making

The Tor website fingerprinting program determines the visited website by analyzing .pcap files to extract key traffic features such as packet sizes and timing intervals. These features are statistically processed to identify patterns of different websites. These patters are then trained on a model and then tested. When testing with new .pcap files the program is comparing to these developed traffic patterns and using the KNN model to make a decison best matching these traffic patterns.

# Advantages Over Random Guessing

Using KNN and feature engineering (e.g., packet sizes, timing intervals) allows the system to identify patterns in traffic data in a more reliable manner compared to random guessing. By leveraging historical data and machine learning, the tool can notice subtle distinctions between different types of traffic, leading to higher accuracy and better network traffic insights.

# Sources

- https://joblib.readthedocs.io/en/stable/
- https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html
- https://pandas.pydata.org/docs/user_guide/index.html
- https://scapy.readthedocs.io/en/latest/usage.html
- https://incognitjoe.github.io/reading-pcap-with-scapy.html
