from flask import Flask, render_template, request, redirect, session , jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'uploads/'  # Directory to save profile images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Jags@7227",
    database="your_database_name"
)

@app.route('/')
def index():
    return render_template('login.html')


# # Sign-up Route
# @app.route('/signup', methods=['POST'])
# def signup():
#     username = request.form['username']
#     password = generate_password_hash(request.form['password'])

#     cursor = db.cursor()
#     cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
#     db.commit()
#     return redirect('/login')

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

# # Login Route
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']

#         cursor = db.cursor()
#         cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
#         result = cursor.fetchone()

#         if result and check_password_hash(result[0], password):
#             session['user'] = username
#             return redirect('/home')
#         else:
#             return "Invalid credentials"
#     return render_template('login.html')


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



# # Home Page Route
# @app.route('/home')
# def home():
#     # if 'user' not in session:
#     #     return redirect('/login')

#     cursor = db.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM patients")
#     patients = cursor.fetchall()
#     cursor.close()

#     return render_template('home.html', patients=patients)


@app.route('/home')
def home():
    # Query the patients from the database
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    # Process patient data for frontend display
    for patient in patients:
        # Assume profile images are stored in the static/uploads directory
        if patient['profile_image_path']:
            patient['profile_image_path'] = f'uploads/{patient["profile_image_path"]}'
        else:
            patient['profile_image_path'] = 'uploads/default_profile.png'  # Use default image if none

    return render_template('home.html', patients=patients)




# @app.route('/get_patients', methods=['GET'])
# def get_patients():
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT name, age FROM patients")
#     patients = cursor.fetchall()
#     cursor.close()
#     conn.close()

#     return jsonify(patients)


# # Add Patient Route
# @app.route('/add_patient', methods=['POST'])
# def add_patient():
#     if 'user' not in session:
#         return redirect('/login')

#     name = request.form['name']
#     age = request.form['age']

#     cursor = db.cursor()
#     cursor.execute("INSERT INTO patients (name, age) VALUES (%s, %s)", (name, age))
#     db.commit()

#     return redirect('/home')

@app.route('/add_patient', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    contact = request.form['contact']
    address = request.form['address']
    email = request.form['email']
    profile_image = request.files['profileImage']
    
    if profile_image:
        # Save profile image
        filename = secure_filename(profile_image.filename)
        profile_image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        profile_image.save(profile_image_path)
    
    # Store patient information in the database
    # Replace with actual database insertion logic
    cursor = db.cursor()
    cursor.execute("INSERT INTO patients (name, age, contact, address, email, profile_image_path) VALUES (%s, %s, %s, %s, %s, %s)", 
                   (name, age, contact, address, email, profile_image_path))
    db.commit()
    
    # Return the new patient data to be displayed in the frontend
    new_patient = {
        'name': name,
        'age': age,
        'contact': contact,
        'address': address,
        'email': email,
        'profileImageUrl': f'uploads/{filename}'
    }
    
    return jsonify({'success': True, 'patient': new_patient})


# Predict Disease Route (Placeholder for actual ML logic)
@app.route('/predict', methods=['POST'])
def predict():
    # if 'user' not in session:
    #     return redirect('/login')

    image = request.files['image']
    # Here you can integrate your ML model to process the image

    result = "Prediction result goes here"  # Replace with actual model prediction
    return render_template('predict_disease.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
