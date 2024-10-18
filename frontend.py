import streamlit as st
import requests

def login():
    st.title("Applicant Login")
    email = st.text_input("Email ID")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post("http://localhost:5000/login", json={"email": email, "password": password})
        if response.status_code == 200:
            st.session_state["logged_in"] = True
            st.session_state["email"] = email
            st.success("Logged in successfully!")
            return True
        else:
            st.error("Invalid credentials")
    return False

def interview_questions():
    st.title("Interview Questions")
    details = {
        "languages_known": st.text_input("Languages Known"),
        "years_of_experience": st.number_input("Years of Experience", 0),
        "programming_languages": st.text_input("Programming Languages Known"),
        "education": st.text_input("University Education"),
        "soft_skills": st.text_input("Soft Skills"),
        "technical_skills": st.text_input("Technical Skills")
    }
    if st.button("Submit"):
        details['email'] = st.session_state["email"]
        response = requests.post("http://localhost:5000/interview", json=details)
        if response.status_code == 200:
            st.success("Your details have been submitted!")
        else:
            st.error("Failed to submit details")

def main():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        if login():
            interview_questions()
    else:
        interview_questions()

if __name__ == '__main__':
    main()
