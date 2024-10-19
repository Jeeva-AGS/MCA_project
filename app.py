from flask import Flask, render_template, request, redirect, session , jsonify, url_for, send_from_directory

import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import datetime

from flask import send_from_directory



from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
loaded_model = load_model(r'C:\Users\jeeva\Study\MCA\final_project\models\brain_tumor1.h5')


app = Flask(__name__)
app.secret_key = 'your_secret_key'
# UPLOAD_FOLDER = 'uploads/'  # Directory to save profile images
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Folder to store prediction images
PREDICTION_FOLDER = 'prediction_uploads'
app.config['PREDICTION_FOLDER'] = PREDICTION_FOLDER

if not os.path.exists(PREDICTION_FOLDER):
    os.makedirs(PREDICTION_FOLDER)

# Check if the file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jags@7227",
    database="healthpredict"
)

@app.route('/')
def index():
    return render_template('login.html')

# Route to serve files from the uploads directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# Route for handling the signup
@app.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        # Get form fields
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        # Hash the password
        # hashed_password = generate_password_hash(password)

        # Insert into MySQL database
        cursor = db.cursor()
        cursor.execute('INSERT INTO users (username, email, password) VALUES (%s, %s, %s)', (username, email, password))
        db.commit()
        cursor.close()

        return redirect('/login')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form fields
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        cursor = db.cursor()
        cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user[0], password):
            # Set up the user session
            session['email'] = email
            return redirect('/home')
        else:
            return 'Invalid email or password!'
    
    # If the request method is GET, show the login page
    return render_template('login.html')



@app.route('/home')
def home():
    # Query the patients from the database
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    # Process patient data for frontend display
    for patient in patients:
        # Check if a profile image exists for the patient
        if patient['profile_image_path']:
            patient['profile_image_path'] = url_for('uploaded_file', filename=patient["profile_image_path"].split('/')[-1])
        else:
            patient['profile_image_path'] = url_for('static', filename='images/user.png')  # Use default image if none

    return render_template('home.html', patients=patients)



@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']
    address = request.form['address']
    email = request.form['email']

    profile_image = request.files['profileImage']
    image_path = None
    
    if profile_image and allowed_file(profile_image.filename):
        filename = secure_filename(profile_image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_image.save(image_path)  # Save the file to the uploads folder
        image_path = image_path.replace("\\", "/")

    # Insert the new patient into the database
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO patients (name, age, contact, email, address, profile_image_path)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, age, contact, email, address, image_path))
    db.commit()

    return jsonify({'message': 'Patient added successfully!'})



@app.route('/get_patients')
def get_patients():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, name, age FROM patients")
    patients = cursor.fetchall()
    return jsonify(patients)



@app.route('/predict_page')
def predict_page():
    # cursor = db.cursor(dictionary=True)
    # cursor.execute("SELECT id, name, age FROM patients")
    # patients = cursor.fetchall()
    # return render_template('predict.html', patients=patients)
    
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, age FROM patients")  # Sample query, replace as necessary
        patients = cursor.fetchall()
        return render_template('predict.html', patients=patients)
    finally:
        cursor.close()
        # db.close()


# Route to handle form submission and prediction
@app.route('/predict', methods=['POST'])
def predict():
    patient_id = request.form.get('patient_id')
    disease = request.form.get('disease')
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    image = request.files['image']

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Perform your prediction logic (Mocking a result here)
        prediction_result = result(image_path)
        # prediction_result = "Prediction result text"

        # Save result to database
        # db = connect_db()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO predictions (patient_id, disease, image_path, prediction_result)
            VALUES (%s, %s, %s, %s)
        """, (patient_id, disease, image_path, prediction_result))
        db.commit()
        cursor.close()
        # db.close()

        return jsonify({'result': prediction_result})

    return jsonify({'error': 'Invalid file type'}), 400


def result(image_path): 
    index = ['glioma','meningioma','normal','adenoma']
    test_image1 = load_img(image_path,target_size = (224,224))
    test_image1 = img_to_array(test_image1)
    test_image1 = np.expand_dims(test_image1,axis=0)
    result1 = np.argmax(loaded_model.predict(test_image1/255.0),axis=1)
    print(result1)
    print(index[result1[0]])
    return index[result1[0]]


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['PREDICTION_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'file_path': file_path})

    return jsonify({'error': 'File not allowed'}), 400



@app.route('/uploads/<filename>')
def get_uploaded_file(filename):
    return send_from_directory('uploads', filename)



@app.route('/prediction_result_page')
def prediction_result_page():
    # db = connect_db()
    cursor = db.cursor(dictionary=True)

    # Fetch all predictions from the database
    cursor.execute("""
    SELECT p.name, p.age, pr.disease, pr.prediction_result, pr.image_path, pr.prediction_time
    FROM predictions pr
    JOIN patients p ON p.id = pr.patient_id
    ORDER BY pr.prediction_time DESC
    """)
    predictions = cursor.fetchall()

    cursor.close()
    # db.close()

    return render_template('prediction_results.html', predictions=predictions)



if __name__ == '__main__':
    app.run(debug=True)
