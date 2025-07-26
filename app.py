from flask import Flask, render_template, request
import requests

app = Flask(__name__)

OLLAMA_URI = "http://localhost:11434/api/generate"
MODEL = "gemma3"

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = None

    if request.method == 'POST':
        user_prompt = request.form.get('prompt')
        
        payload = {
            "model": MODEL,
            "prompt": user_prompt,
            "stream": False  
        }

        try:
            response = requests.post(OLLAMA_URI, json=payload)
            if response.status_code == 200:
                result = response.json()
                response_text = result.get("response", "No response key in result.")
            else:
                response_text = f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            response_text = f"Request failed: {str(e)}"

    return render_template('index.html', response=response_text)

if __name__ == '__main__':
    app.run(debug=True)
