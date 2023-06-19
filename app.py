from flask import Flask, request, redirect, url_for, render_template, jsonify
from werkzeug.utils import secure_filename
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI
import os
import openai

openai.api_key = os.environ["OPENAI_API_KEY"]

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}
model_name = 'gpt-3.5-turbo'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PDF_FILENAME'] = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # POST: Handle file upload
        if 'file' not in request.files:
            # No file part
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            # No selected file
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            app.config['PDF_FILENAME'] = filename
            return redirect(url_for('chat_page'))
    else:
        # GET: Show the file upload form
        return render_template('upload.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    # Load the PDF file
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['PDF_FILENAME'])
    loader = PyPDFLoader(pdf_path)
    pages = loader.load_and_split()

    # Create the ChatVectorDBChain object
    embeddings = OpenAIEmbeddings(model=model_name)
    vectordb = Chroma.from_documents(pages, embedding=embeddings, persist_directory=".")
    vectordb.persist()
    pdf_chat = ChatVectorDBChain.from_llm(OpenAI(temperature=0.9, model_name=model_name), vectordb, return_source_documents=True)

    # Parse the question from the request
    question = request.get_json()['question']

    # Use your existing script to process the question and get an answer
    query = {"question": question, "chat_history": []}
    response = pdf_chat(query)
    print(response)
    answer = response["answer"]
    source_docs = response["source_documents"]
    page_numbers = [doc.metadata["page"] for doc in source_docs]
    page_numbers = list(set(page_numbers))

    # Return the answer and page numbers as a JSON object
    return jsonify({'answer': answer, 'page_numbers': page_numbers})

if __name__ == "__main__":
    app.run(debug=True)
