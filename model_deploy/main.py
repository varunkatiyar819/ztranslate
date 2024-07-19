from flask import Flask, request, jsonify, render_template_string
from inference_ct2 import ModelInference
from html_template import create_template

app = Flask(__name__)
model = ModelInference()

@app.route('/')
def home():
    """
    Serve the HTML form for input.
    """
    return render_template_string(create_template())

@app.route('/translate', methods=['POST'])
def predict():
    """
    Endpoint to get predictions from the model.
    Expects a JSON payload with a key "input" containing the text to be translated.
    """
    data = request.json
    print("data = ", data)
    if not data or 'input' not in data:
        return jsonify({"error": "Invalid input. Please provide text to translate.","message": {"status_code": 400, "status" : "failure"}}), 400
    
    # Perform translation using the CTranslate2 model
    input_text = data['input']
    source_text = input_text.split('\n')  # Assuming input is a \n-separated sentence
    # source_text = input_text # Assuming input is a list of sentence
    print("source text = ", source_text)
    results = model.batch_translate(source_text)
    print("results = ", results)

    return jsonify({"translations" : [{"source": source, "translation": target} for source, target in zip(source_text, results)], "message": {"status_code": 200, "status" : "success"}})

@app.route('/health', methods=['GET'])
def health():
    """
    Health check endpoint to ensure the API is running.
    """
    return jsonify({"status": "Healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


