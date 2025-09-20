
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer
import numpy as np
from vectorDB.retrieve import similarity_search
from models.llm import llm_response


app = Flask(__name__)

# Load the embedding model once at startup
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    prompt = data.get('prompt', '')
    print(f"User prompt: {prompt}")
    context = similarity_search(prompt)
    response = llm_response(context, prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
