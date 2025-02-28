# 📌 Diet Recommendation Flask API

## 🚀 Overview

This project is a **Flask-based API** that allows users to **register, log in, save diet data, train a machine learning model, and get diet recommendations** based on their data. The application is deployed on **PythonAnywhere**, with a **GitHub webhook** for automatic updates and database migrations.

---

## 📂 1️⃣ Models

The database models are built using **SQLAlchemy**, and they store **user details and diet data**.

### 📝 `Users` Model

- Stores **user account details**.
- **Fields**: `id`, `first_name`, `last_name`, `username`, `password`, `created_at`, `updated_at`.
- **Functions**:
  - `set_password(password)`: Hashes user password.
  - `check_password(password)`: Verifies hashed password.
  - `find_by_username(username)`: Retrieves user by username.

### 📝 `DietData` Model

- Stores **user diet details** for prediction.
- **Fields**: `id`, `user_id` (foreign key), `age`, `gender`, `height`, `weight`, `activity_level`, `goal`, `dietary_preference`, `predicted_diet`.
- **Functions**:
  - `save_to_db()`: Saves the diet record to the database.
  - `delete_from_db()`: Deletes a diet record.

---

## 📌 2️⃣ Resources

Flask **RESTful resources** handle **user authentication, diet data, training, and prediction**.

### 🛠️ `UserRegister` Resource

- **Endpoint**: `/register` (POST)
- **Functionality**:
  - Registers a new user.
  - Hashes the password before storing.
  - Returns `400` if the username already exists.

### 🛠️ `UserLogin` Resource

- **Endpoint**: `/login` (POST)
- **Functionality**:
  - Authenticates a user.
  - Generates **JWT access and refresh tokens**.
  - Returns `401` if credentials are invalid.

### 🛠️ `DietDataResource` Resource

- **Endpoints**:
  - `/diet` (POST) - Saves diet data (Requires JWT).
  - `/diet` (GET) - Retrieves saved diet data for the logged-in user.
- **Functionality**:
  - Saves diet data to the database.
  - Ensures the user ID is attached via **JWT authentication**.

### 🛠️ `AllUsersWithDietData` Resource

- **Endpoint**: `/users_diet_data` (GET)
- **Functionality**:
  - Fetches **all users and their diet data**.

### 🛠️ `TrainModelResource`

- **Endpoint**: `/train_model` (POST, Requires JWT)
- **Functionality**:
  - Loads **diet data from the database**.
  - Preprocesses and **trains a RandomForestClassifier**.
  - Saves the trained model and its **feature names**.
  - Returns **model accuracy**.

### 🛠️ `PredictFoodResource`

- **Endpoint**: `/predict_food` (POST, Requires JWT)
- **Functionality**:
  - Retrieves **diet data from the database** for the logged-in user.
  - **Ensures the input data matches the model features.**
  - Runs **machine learning prediction** for a recommended diet.

---

## 📂 3️⃣ Schemas

Flask-Marshmallow schemas help **serialize and deserialize data**.

### 📌 `UserSchema`

- Serializes user objects.
- Hides **password** when returning user data.

### 📌 `DietDataSchema`

- Serializes **diet data** objects.
- Ensures data **matches the database schema**.

---

## 🌐 4️⃣ Routes with cURL Examples

### 📌 Authentication & User Routes

#### **1️⃣ Register a User**

```sh
curl -X POST https://kollie.pythonanywhere.com/register      -H "Content-Type: application/json"      -d '{
           "first_name": "John",
           "last_name": "Doe",
           "username": "johndoe",
           "password": "password123"
         }'
```

#### **2️⃣ Log In a User**

```sh
curl -X POST https://kollie.pythonanywhere.com/login      -H "Content-Type: application/json"      -d '{
           "username": "johndoe",
           "password": "password123"
         }'
```

### 📌 Diet Data Routes

#### **3️⃣ Save Diet Data**

```sh
curl -X POST https://kollie.pythonanywhere.com/diet      -H "Content-Type: application/json"      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"      -d '{
           "age": 30,
           "gender": "Male",
           "height": 175,
           "weight": 75,
           "activity_level": "Moderate",
           "goal": "Muscle Gain",
           "dietary_preference": "Balanced"
         }'
```

#### **4️⃣ Get Diet Data**

```sh
curl -X GET https://kollie.pythonanywhere.com/diet      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 📌 Machine Learning Routes

#### **5️⃣ Train Model**

```sh
curl -X POST https://kollie.pythonanywhere.com/train_model      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### **6️⃣ Predict Diet Recommendation**

```sh
curl -X POST https://kollie.pythonanywhere.com/predict_food      -H "Content-Type: application/json"      -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 📂 5️⃣ Training & Prediction

- Uses **`RandomForestClassifier`**.
- Data is **one-hot encoded** to handle categorical features.
- **Feature names are saved** (`model_features.pkl`) to ensure consistent input.

---

## 🚀 6️⃣ Webhook for Auto-Deployment

A **GitHub webhook** is set up to:

1. **Pull the latest code** from the repository.
2. **Run database migrations (`flask db upgrade`).**
3. **Restart the web server** on PythonAnywhere.

---

## 🚀 7️⃣ Deployment on PythonAnywhere

### 📌 Steps Followed:

1. **Created a virtual environment** (`venv`) to manage dependencies.
   ```sh
   python -m venv ~/.virtualenvs/my-virtualenv
   source ~/.virtualenvs/my-virtualenv/bin/activate
   pip install -r requirements.txt
   ```
2. **Configured WSGI (`/var/www/kollie_pythonanywhere_com_wsgi.py`):**

   ```python
   import sys
   import os

   project_path = "/home/kollie/flask-project/ad-backend-flask-webhook"
   venv_path = "/home/kollie/.virtualenvs/my-virtualenv"

   activate_this = os.path.join(venv_path, "bin", "activate_this.py")
   exec(open(activate_this).read(), dict(__file__=activate_this))

   if project_path not in sys.path:
       sys.path.append(project_path)

   from main import application as app
   ```

3. **Restarted PythonAnywhere Web Server:**
   ```sh
   touch /var/www/kollie_pythonanywhere_com_wsgi.py
   ```

---

## 🎯 Conclusion

This project successfully implements:
✅ **User authentication (JWT)**  
✅ **Diet data storage & retrieval**  
✅ **Machine learning-based diet recommendation**  
✅ **GitHub webhook for auto-deployment**  
✅ **Manual execution endpoints**

🚀 **System is now fully functional and scalable!** 🚀
