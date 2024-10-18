from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import sqlite3
import os
import requests

app = Flask(__name__)
CORS(app)

# Replace with your Gemini AI Key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect('applicants.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route for login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']
    
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password)).fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# Route to receive interview answers
@app.route('/interview', methods=['POST'])
def interview():
    data = request.get_json()
    email = data['email']
    # Save the applicant's details in the database
    conn = get_db_connection()
    conn.execute('INSERT INTO applicants (email, languages_known, years_of_experience, programming_languages, education, soft_skills, technical_skills) VALUES (?, ?, ?, ?, ?, ?, ?)',
                 (email, data['languages_known'], data['years_of_experience'], data['programming_languages'], data['education'], data['soft_skills'], data['technical_skills']))
    conn.commit()
    conn.close()

    # Send details to Gemini API for shortlisting
    applicants = get_all_applicants()
    shortlisted = shortlist_applicants(applicants)
    
    if email in shortlisted:
        send_shortlist_email(email)
    return jsonify({"message": "Details submitted successfully!"}), 200

# Fetch all applicants' data
def get_all_applicants():
    conn = get_db_connection()
    applicants = conn.execute('SELECT * FROM applicants').fetchall()
    conn.close()
    return applicants

# Send data to Gemini AI for analysis and shortlisting
def shortlist_applicants(applicants):
    # Simulate calling Gemini API
    gemini_response = requests.post('https://gemini-api/shortlist', json={"applicants": applicants}, headers={'Authorization': f'Bearer {GEMINI_API_KEY}'})
    shortlisted_emails = gemini_response.json().get('shortlisted', [])
    return shortlisted_emails

# Function to send email to shortlisted candidates
def send_shortlist_email(email):
    sender = 'your-email@gmail.com'
    receiver = email
    message = f"Subject: Shortlisted\n\nCongratulations! You have been shortlisted."
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, os.getenv('GMAIL_PASSWORD'))
        server.sendmail(sender, receiver, message)

if __name__ == "__main__":
    app.run(debug=True)
