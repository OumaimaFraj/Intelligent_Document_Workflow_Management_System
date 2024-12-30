
from transformers import pipeline
import PyPDF2

# Fonction pour extraire le texte du fichier PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

# Fonction pour classifier le texte extrait
def classify_text(text):
    classifier = pipeline("zero-shot-classification")  # Chargement du modèle de classification
    candidate_labels = ["remote work", "project progress", "invoice"]
    result = classifier(text, candidate_labels=candidate_labels)
    return result['labels'][0] 


from transformers import pipeline

def summarize_text(text):
    try:
        summarizer = pipeline("summarization")
        print("Summarizer loaded successfully.")
        summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
        print("Summarization result:", summary)
        return summary[0]['summary_text']
    except Exception as e:
        print("Error during summarization:", e)
        return None
