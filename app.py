from flask import Flask, request, jsonify, render_template
from PyPDF2 import PdfReader

app = Flask(__name__)

# Load PDF and preprocess content
def load_pdf_content(pdf_path):
    reader = PdfReader(pdf_path)
    text = " ".join([page.extract_text() for page in reader.pages if page.extract_text()])
    sentences = text.split(".")
    return [sentence.strip() for sentence in sentences if sentence.strip()]

# Search algorithm for direct answers
def search_content(query, sentences):
    query = query.lower()
    results = sorted(
        sentences,
        key=lambda s: sum(word in s.lower() for word in query.split()),
        reverse=True
    )
    # Return the most relevant 1-2 sentences
    return results[:2] if results else ["No relevant information found."]

# Preload the PDF content
PDF_PATH = "medicalbook.pdf"
SENTENCES = load_pdf_content(PDF_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_query = request.json.get("query", "")
    results = search_content(user_query, SENTENCES)
    response = " ".join(results)
    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True)
