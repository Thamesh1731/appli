import streamlit as st
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# --- Database setup ---
def create_user_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users (name TEXT, email TEXT UNIQUE, password TEXT)')
    conn.commit()
    conn.close()

def add_user(name, email, hashed_password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_password))
    conn.commit()
    conn.close()

def login_user(email):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = c.fetchone()
    conn.close()
    return user

# --- Registration Form ---
def register():
    st.header("Register")
    name = st.text_input("Enter your name")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter a password", type="password")
    
    if st.button("Register"):
        if name and email and password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            try:
                add_user(name, email, hashed_password)
                st.success("Registration successful! You can now login.")
            except sqlite3.IntegrityError:
                st.error("This email is already registered.")
        else:
            st.error("Please fill out all fields.")

# --- Login Form ---
def login():
    st.header("Login")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")
    
    if st.button("Login"):
        user = login_user(email)
        if user and check_password_hash(user[2], password):
            st.success(f"Welcome back, {user[0]}!")
            # Redirect to interview questions
            interview_questions()
        else:
            st.error("Invalid credentials. Please try again.")

# --- Interview Questions ---
def interview_questions():
    st.subheader("Interview Questions")
    # Example of questions to ask after login
    languages_known = st.text_input("What programming languages do you know?")
    years_of_experience = st.text_input("How many years of experience do you have?")
    education = st.text_input("What is your educational background?")
    soft_skills = st.text_input("What are your key soft skills?")
    technical_skills = st.text_input("What technical skills do you possess?")
    
    if st.button("Submit"):
        st.success("Your interview details have been submitted!")
        # Process answers here

# --- Main Interface ---
def main():
    st.title("Full Stack Developer Application")

    # Create user table if not exists
    create_user_table()

    # Sidebar options for Registration or Login
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Login":
        login()
    elif choice == "Register":
        register()

if __name__ == '__main__':
    main()
