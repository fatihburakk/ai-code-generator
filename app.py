from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>AI Kod Üretici</title>
</head>
<body>
    <h1>Yapay Zekâ Destekli Kod Üretici</h1>
    <form method="post">
        Prompt: <input type="text" name="prompt" size="50">
        <input type="submit" value="Kod Üret">
    </form>
    {% if code %}
        <h2>Başlık: {{ title }}</h2>
        <h3>Üretilen Kod:</h3>
        <pre>{{ code }}</pre>
    {% endif %}
</body>
</html>
'''

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "codellama"

@app.route("/", methods=["GET", "POST"])
def index():
    code = ""
    title = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        response = requests.post(OLLAMA_API_URL, json={
            "model": MODEL_NAME,
            "prompt": f"Aşağıdaki isteğe göre bir Python kodu ve kısa bir başlık üret:\n{prompt}",
            "stream": False
        })
        if response.status_code == 200:
            data = response.json()
            response_text = data.get("response", "")
            parts = response_text.split('\n', 1)
            if len(parts) == 2:
                title, code = parts
    return render_template_string(HTML_TEMPLATE, title=title, code=code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
