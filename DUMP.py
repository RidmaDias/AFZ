import joblib
import re
import nltk
import numpy as np
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from tkinter import messagebox

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

# New data insert
new_text = input("Enter The Log Here: ")
preprocessed_text = preprocess_text(new_text)

# Use the loaded CountVectorizer object to transform the preprocessed text into a bag of words representation
new_text_bow = cv.transform([preprocessed_text]).toarray()

# Make predictions using the loaded model
predictions = regressor.predict(new_text_bow)
rounded_predictions = np.round(predictions)
predicted_type = prediction_types[int(rounded_predictions[0])]

# Print the predictions
print(rounded_predictions)

# Display a pop-up message with the predicted type
message = f"The predicted Mapping is: {predicted_type}"
messagebox.showinfo("Prediction", message)
