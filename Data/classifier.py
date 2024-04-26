import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

df = pd.read_excel('pcap_analysis.xlsx', sheet_name='Statistics')
X = df.drop('Website', axis=1)
y = df['Website']

print(y.value_counts())

try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
except ValueError:
    print("Stratified split failed due to insufficient data per class. Trying non-stratified split.")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

tree = DecisionTreeClassifier(max_depth=5, random_state=42)
tree.fit(X_train, y_train)
joblib.dump(tree, 'decision_tree_model.pkl')

loaded_tree = joblib.load('decision_tree_model.pkl')
predictions = loaded_tree.predict(X_test)
print(classification_report(y_test, predictions, zero_division=0))

