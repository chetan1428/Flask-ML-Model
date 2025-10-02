from flask import Flask, request, jsonify
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

app = Flask(__name__)

MODEL_PATH = "models/model.pkl"
model = None
FEATURE_COLS = [
    'type', 
    'Air temperature [K]', 
    'Process temperature [K]',
    'Rotational speed [rpm]', 
    'Torque [Nm]', 
    'Tool wear [min]'
]

def preprocess(df, is_train=True):
   
    for col in ['Product ID', 'UDI','Target']:
        if col in df.columns:
            df.drop(col, axis=1, inplace=True)    

    
    if 'Type' in df.columns:
        df['type'] = df['Type'].map({'M': 0, 'L': 1, 'H': 2})
        df.drop('Type', axis=1, inplace=True)

    
    if is_train and 'Failure Type' in df.columns:
        y = df['Failure Type']
        X = df.drop('Failure Type', axis=1)

       
        X = X.select_dtypes(include=['number'])
        return X, y
    else:
        
        df = df.select_dtypes(include=['number'])
        return df


@app.route('/train', methods=['POST'])
def train():
    global model

    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"File read error: {str(e)}"}), 400

    X_train, y_train = preprocess(df, is_train=True)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    os.makedirs("models", exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    preview = df.head().to_dict(orient="records")

    return jsonify({
        "status": "Model trained successfully",
        "preview": preview
    })


@app.route('/test', methods=['POST'])
def test():
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            return jsonify({'error': 'Model not trained yet'}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    df = pd.read_csv(file)

    X_test, y_true = preprocess(df, is_train=True)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_true, y_pred)

    return jsonify({'accuracy_score': float(acc)})



@app.route('/predict', methods=['POST'])
def predict():
    global model
    if model is None:
        return jsonify({'error': 'Model not found. Train and save it first.'}), 400

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    df = pd.DataFrame([data])
    df = preprocess(df)

    try:
        prediction = model.predict(df)[0]
    except Exception as e:
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 400

    return jsonify({'prediction': str(prediction)})

if __name__ == "__main__":
    app.run(debug=True)
