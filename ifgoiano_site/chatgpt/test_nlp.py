import spacy

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

subjects = [
    "Fox",
    "Life",
    "Wrong",
    # Add more subjects as needed
]

def assess_text(text, subject):
    doc = nlp(text)
    
    # You can implement your own logic here to assess relevance to the subject
    # For example, you can count the frequency of the subject in the text
    # or use more advanced NLP techniques for sentiment analysis, keyword extraction, etc.
    
    # For simplicity, let's just check if the subject is mentioned in the text
    return subject in text

# Example list of texts
texts = [
    "The quick brown fox jumped over the fence.",
    "Life is full of surprises.",
    "It's wrong to lie.",
    # Add more texts as needed
]

# Assess each text for each subject
for subject in subjects:
    print(f"Assessing texts for subject: {subject}")
    for text in texts:
        relevance = assess_text(text, subject)
        print(f"Text: '{text}' - Relevant: {relevance}")
