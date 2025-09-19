from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    prompt = data.get('prompt', '')
    print(f"User prompt: {prompt}")
    # For now, just echo the prompt back
    return jsonify({'response': f'You said: {prompt}'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
