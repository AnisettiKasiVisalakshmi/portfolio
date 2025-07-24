from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Validate API key
if not api_key:
    raise Exception("❌ GEMINI_API_KEY not found in .env file!")

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-2.0-flash")  # Text model

# Setup Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend (React or Postman)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        print("📩 User asked:", message)

        # Get Gemini response
        response = model.generate_content(message)

        # Return the actual LLM-generated text
        return jsonify({"reply": response.text})

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({"reply": "Sorry, something went wrong."}), 500

if __name__ == "__main__":
    app.run(debug=True)
