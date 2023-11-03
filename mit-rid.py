import joblib
import re
import nltk
import numpy as np
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
#from tkinter import messagebox
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate

def send_email(subject, message):
    from_email = 'iotsafehaven@gmail.com'  # Replace with your Gmail email address
    password = 'pqfhdhvmejyfxgtu'  # Replace with your Gmail password

    to_email = 'temp.dinidhu@gmail.com'  # Replace with the recipient's email address

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    msg.attach(MIMEText(message, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(from_email, password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()

# Load the dumped models
regressor = joblib.load('random_forest_model.joblib')
cv = joblib.load('count_vectorizer.joblib')

# Function to Clean the texts
def preprocess_text(text):
    log = re.sub('[^a-zA-Z0-9]', ' ', text)
    log = log.lower()
    log = log.split()
    ps = PorterStemmer()
    log = [ps.stem(word) for word in log if not word in set(stopwords.words('english'))]
    log = ' '.join(log)
    return log

# Mapping of predictions to respective types
prediction_types = {
    0: "Credential Access",
    1: "Privilege Escalation",
    2: "Execution",
    3: "Resource Development"
}

# Instead of just the mapping, initialize a dictionary to count the occurrences
prediction_counts = {
    "Credential Access": 0,
    "Privilege Escalation": 0,
    "Execution": 0,
    "Resource Development": 0
}

def read_file_line_by_line(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

# List of filenames you want to process
file_names = ['auth.log', 'syslog', 'log.txt']

# Loop through the list of filenames and read each file line by line
for file_name in file_names:
    for line in read_file_line_by_line(file_name):
        new_text = str(line)
        preprocessed_text = preprocess_text(new_text)
        
        # Use the loaded CountVectorizer object to transform the preprocessed text into a bag of words representation
        new_text_bow = cv.transform([preprocessed_text]).toarray()

        # Make predictions using the loaded model
        predictions = regressor.predict(new_text_bow)
        rounded_predictions = np.round(predictions)
        predicted_type = prediction_types[int(rounded_predictions[0])]
        
        # Update the count for the predicted type
        prediction_counts[predicted_type] += 1

# Generate the email message
email_subject = "User Activity detection according to the MITRE ATTACK"
email_message ="Identified Types \n\nCredential Access: This type involves techniques and methods used by attackers to obtain valid usernames and passwords, allowing them to access systems and resources that require authentication.\n\nPrivilege Escalation: Privilege escalation techniques are employed by attackers to elevate their level of access or permissions within a compromised system, enabling them to perform actions and access resources that are typically restricted.\n\nExecution: Execution techniques refer to the methods used by attackers to run malicious code or execute arbitrary commands on a target system. This can be a crucial step in carrying out various types of cyberattacks.\n\nResource Development: Resource development encompasses the activities undertaken by attackers to create or acquire the tools, scripts, or resources needed to facilitate their cyber operations. This may include custom malware, utilities, or infrastructure setup.\n\n\n\nHere are the ativitis list according to the MITRE attack framework,:\n\n"
for prediction_type, count in prediction_counts.items():
    email_message += f"{prediction_type}: {count} occurrences\n"

# Print the email subject and message (Instead of sending it)
# print(email_subject)
# print("\n")
# print(email_message)

#print(email_message)
if send_email(email_subject, email_message):
    print("Email Sent")
else:
    print("Email sent")
