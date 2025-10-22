import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

print("Starting model training...")

# 1. Load the dataset
# 1. Load the dataset
local_file = "diabetes.csv"  # <-- Tell pandas to read the local file
column_names = [
    'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 
    'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome'
]
# Make sure 'diabetes.csv' is in the same folder as train_model.py
data = pd.read_csv(local_file, header=0, names=column_names)

print("Dataset loaded.")

# 2. Define Features (X) and Target (y)
features = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
target = 'Outcome'
X = data[features]
y = data[target]

# 3. Create and Train the AI Model
model = DecisionTreeClassifier(random_state=42)
model.fit(X, y) # Train on all data for the web app

print("Model trained.")

# 4. Save the trained model to a file
joblib.dump(model, 'diabetes_model.pkl')

print("Model saved as diabetes_model.pkl")