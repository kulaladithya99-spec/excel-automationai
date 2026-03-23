from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Process Excel
        df = pd.read_excel(filepath)

        # Example: Clean data
        df = df.dropna()  # remove empty rows

        # Save cleaned file
        output_path = os.path.join(UPLOAD_FOLDER, "cleaned_" + file.filename)
        df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return "No file uploaded"

if __name__ == '__main__':
    app.run(debug=True)