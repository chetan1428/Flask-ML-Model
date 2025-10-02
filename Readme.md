Sure! Here's a ready-to-copy `README.md` file for your Flask ML API project:

````markdown
# Predictive Maintenance Flask API

This repository contains a Flask API for training, testing, and predicting machine failures using a **Logistic Regression** model. You can interact with the API via **Postman** or any HTTP client.

---

## Features

- Train a model on a CSV dataset (`/train`)
- Test model accuracy on a CSV dataset (`/test`)
- Make predictions for a single data point via JSON (`/predict`)

---

## Requirements

- Python 3.8+
- Flask
- pandas
- scikit-learn
- joblib

Install dependencies:

```bash
pip install flask pandas scikit-learn joblib
````

---

## Project Structure

```
project/
│
├─ app.py          # Flask API
├─ models/
│   └─ model.pkl   # Saved trained model
├─ README.md
└─ requirements.txt
```

---

## API Endpoints

### 1. Train Model

* **URL:** `/train`
* **Method:** `POST`
* **Body:** Form-data with CSV file
* **Form field:** `file`
* **Response:**

```json
{
  "status": "Model trained successfully",
  "preview": [
    {
      "type": 0,
      "Air temperature [K]": 293,
      "Process temperature [K]": 300,
      "Rotational speed [rpm]": 1500,
      "Torque [Nm]": 40,
      "Tool wear [min]": 120
    }
  ]
}
```

**Postman Example:**

1. Select **POST** method
2. Enter `http://127.0.0.1:5000/train`
3. Under **Body → form-data**, add:

   * Key: `file` → select CSV file
4. Send request

---

### 2. Test Model

* **URL:** `/test`
* **Method:** `POST`
* **Body:** Form-data with CSV file
* **Form field:** `file`
* **Response:**

```json
{
  "accuracy_score": 0.9752
}
```

**Postman Example:**

1. Select **POST** method
2. Enter `http://127.0.0.1:5000/test`
3. Under **Body → form-data**, add:

   * Key: `file` → select CSV file
4. Send request

---

### 3. Predict

* **URL:** `/predict`
* **Method:** `POST`
* **Body:** raw JSON
* **Example JSON:**

```json
{
  "type": 0,
  "Air temperature [K]": 293,
  "Process temperature [K]": 300,
  "Rotational speed [rpm]": 1500,
  "Torque [Nm]": 40,
  "Tool wear [min]": 120
}
```

* **Response:**

```json
{
  "prediction": "No Failure"
}
```

**Postman Example:**

1. Select **POST** method
2. Enter `http://127.0.0.1:5000/predict`
3. Under **Body → raw → JSON**, paste your JSON
4. Send request

---

## Running the App

```bash
python app.py
```

The API will run at:

```
http://127.0.0.1:5000
```

---

## Notes

* The model will be saved automatically to `models/model.pkl` after training.
* Make sure your CSV has proper columns:

```
Type, Air temperature [K], Process temperature [K], Rotational speed [rpm], Torque [Nm], Tool wear [min], Failure Type
```

* Type mapping: `M=0`, `L=1`, `H=2`
* All input features must be numeric except the 'Type' column.

---

## License

This project is open-source and available under the MIT License.

```

---

If you want, I can also create a **sample Postman collection JSON** ready to import so you can test `/train`, `/test`, and `/predict` directly.  

Do you want me to do that?
```
