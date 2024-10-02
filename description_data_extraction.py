import os
import pandas as pd
import re
import spacy
from spacy.cli import download

# Check if the spaCy model is already downloaded
if not os.path.exists(spacy.util.get_package_path('en_core_web_sm')):
    download("en_core_web_sm")
# Load spaCy model for NER and dependency parsing
nlp = spacy.load('en_core_web_sm')

# Regex function to find email in the description
def find_email(description):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', description)
    return match.group(0) if match else None

# spaCy function to find names in the description
def find_names(description):
    doc = nlp(description)
    names = [ent.text for ent in doc.ents if ent.label_ == 'PERSON']
    if names and len(names[0].split()) >= 2:
        return names[0].split()[0], names[0].split()[1]
    return None, None


# Regex function to extract PQE
def find_pqe(description):
    pqe_patterns = [
        r'(\d+\s*[\+-]\s*\d+\s*years?\s*PQE)',  # Matches "3-5 years PQE" or "3 + 5 years PQE"
        r'(\d+\s*to\s*\d+\s*years?\s*PQE)',  # Matches "3 to 5 years PQE"
        r'(\d+\+?\s*years?\s*of\s*experience)',  # Matches "5+ years of experience"
        r'(\d+\s*-\s*\d+\s*years?\s*of\s*experience)',  # Matches "3 - 5 years of experience"
        r'(\d+\s*years?\s*PQE)',  # Matches "5 years PQE" (broad match last)
    ]
    for pattern in pqe_patterns:
        pqe_match = re.search(pattern, description, re.IGNORECASE)
        if pqe_match:
            return pqe_match.group(0).replace(' ', '')  # Optional: remove spaces for consistency
    return nlp_fallback_pqe(description)

# NLP-based fallback function for PQE extraction
def nlp_fallback_pqe(description):
    doc = nlp(description)
    # Define common phrases and words associated with experience
    target_phrases = ['year', 'experience', 'PQE', 'professional', 'qualification']
    # Look for numeric tokens near these keywords
    for token in doc:
        if token.text.lower() in target_phrases or token.head.text.lower() in target_phrases:
            if token.head.pos_ in ['NUM', 'NOUN']:  # Likely to be the quantity of years
                # Check for nearby 'year' or number
                for child in token.head.children:
                    if child.pos_ == 'NUM' or (child.text.lower() in target_phrases and child.pos_ == 'NOUN'):
                        return child.text + ' ' + token.text
    return None


# Load the CSV file
df = pd.read_csv('scraped_data.csv')

# Apply the email and name finding functions
df['Email'] = df['Description'].apply(find_email)
df['Name'], df['Surname'] = zip(*df['Description'].apply(find_names))

# Apply the PQE finding function
df['PQE'] = df['Description'].apply(find_pqe)

# Optionally, remove the Description column if it's no longer needed
df.drop(columns=['Description'], inplace=True)

# Save the updated dataframe to a new CSV
df.to_csv('final_data.csv', index=False)

# Save the updated dataframe to an Excel file
df.to_excel('final_data.xlsx', index=False)

# Print a sample of the updated dataframe to check the new columns
print(df.head())
