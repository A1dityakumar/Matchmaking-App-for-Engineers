from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# MySQL database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port="3306",
    password="Aditya@604",
    database="compatibility_checker"
)
cursor = db.cursor()

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.json
        name = data.get('name')
        age = data.get('age')
        profession = data.get('profession')
        linkedin = data.get('linkedin')
        interests = data.get('interests')
        location = data.get('location')
        ctc = data.get('ctc')
        password = generate_password_hash(data.get('password'))

        cursor.execute("INSERT INTO profiles (name, age, profession, linkedin, interests, location, ctc, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (name, age, profession, linkedin, interests, location, ctc, password))
        db.commit()
        return jsonify({'message': 'User registered successfully'})
    except Exception as e:
        return jsonify({'message': 'Error occurred during registration', 'error': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        cursor.execute("SELECT * FROM profiles WHERE name = %s", (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[8], password):
            return jsonify({'message': 'Login successful', 'user': user})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': 'Error occurred during login', 'error': str(e)}), 500

@app.route('/api/profiles', methods=['GET'])
def get_profiles():
    try:
        cursor.execute("SELECT * FROM profiles")
        profiles = cursor.fetchall()
        return jsonify(profiles)
    except Exception as e:
        return jsonify({'message': 'Error occurred while fetching profiles', 'error': str(e)}), 500

# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'message': 'The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.'}), 404

if __name__ == '__main__':
    app.run(debug=True)


