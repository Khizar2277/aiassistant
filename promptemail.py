import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
import json

# Configuration
GEMINI_API_KEY = "AIzaSyAsS924IW62FGSt-L7JxJdCnUNGrJGPscg"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent"
SENDER_EMAIL = "info@business2businessltd.com"  # Set your default sender email
SENDER_PASSWORD = "Mada[3377]"  # Set your default sender password
SMTP_SERVER = "smtp.hostinger.com"  # Change as needed
SMTP_PORT = 587

# Schedule Storage
if "schedule" not in st.session_state:
    st.session_state["schedule"] = []

# Email sending function
def send_email(recipient_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
        server.quit()
        
        return "Email sent successfully!"
    except Exception as e:
        return f"Error: {str(e)}"

# AI Email Generation
def generate_email(prompt):
    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": f"Write a short, friendly, and conversational email. Keep it natural and engaging. End with 'Best,\nClive M.'. {prompt}"}]}]}
    
    response = requests.post(GEMINI_API_URL, headers=headers, params=params, json=data)
    if response.status_code == 200:
        response_json = response.json()
        return response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Error: Could not generate email.")
    else:
        return f"Error: {response.status_code} - {response.text}"

# Internet Search Function
def search_internet(query):
    search_url = "https://www.googleapis.com/customsearch/v1"
    api_key = "AIzaSyDnam_uTb_prcg_9QadUCiaO9MIbqKR6zc"
    cx = "8604722c019054a57"
    params = {"q": query, "key": api_key, "cx": cx}
    response = requests.get(search_url, params=params)
    
    if response.status_code == 200:
        results = response.json().get("items", [])
        return [f"{idx + 1}. [{item['title']}]({item['link']})" for idx, item in enumerate(results[:10])]
    else:
        return ["Error: Could not fetch search results"]

# Streamlit UI
st.title("B2B AI Assistant")

option = st.radio("Choose a feature:", ["Email Assistant", "Schedule Manager", "Internet Search"])

if option == "Email Assistant":
    prompt = st.text_area("Enter email prompt:")
    recipient_email = st.text_input("Recipient Email")
    subject = st.text_input("Email Subject")
    
    if st.button("Generate Email"):
        if prompt.strip():
            email_content = generate_email(prompt)
            st.session_state["generated_email"] = email_content
            st.subheader("Generated Email:")
            st.write(email_content)
        else:
            st.error("Please enter a prompt.")
    
    if "generated_email" in st.session_state:
        email_content = st.text_area("Edit email before sending:", st.session_state["generated_email"])
        
        if st.button("Send Email"):
            if recipient_email and subject:
                result = send_email(recipient_email, subject, email_content)
                st.success(result)
            else:
                st.error("Please fill in all fields before sending.")

elif option == "Schedule Manager":
    st.subheader("Manage Your Schedule")
    new_event = st.text_input("Add a new event:")
    if st.button("Add Event"):
        if new_event:
            st.session_state["schedule"].append(new_event)
            st.success("Event added to schedule!")
        else:
            st.error("Please enter an event.")
    
    if st.button("Show Schedule"):
        if st.session_state["schedule"]:
            st.subheader("Your Schedule:")
            for idx, event in enumerate(st.session_state["schedule"], 1):
                st.write(f"{idx}. {event}")
        else:
            st.write("Your schedule is empty.")

elif option == "Internet Search":
    st.subheader("Search the Internet")
    search_query = st.text_input("Enter search query:")
    
    if st.button("Search"):
        if search_query.strip():
            results = search_internet(search_query)
            st.subheader("Top 10 Search Results:")
            for result in results:
                st.markdown(result, unsafe_allow_html=True)
        else:
            st.error("Please enter a search query.")
