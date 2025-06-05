from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
from openai import OpenAI  # new import style

load_dotenv()  # Load environment variables from .env file

app = Flask(__name__)

# Initialize OpenAI client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

system_prompt = {"role": "system", "content": "You are a polite customer support representative."}
postfix = """
\n\nWrite an email to customers to address the issues put forward in the above review, thank them if they write good comments, and encourage them to make further purchases. Do not give promotion codes or discounts to the customers. Do not recommend other products. Keep the emails short.
"""

# Sample reviews to populate the dropdown
reviews = [
    "The product arrived damaged and customer service took too long to respond.",
    "Absolutely love this! It exceeded my expectations.",
    "The quality is not great, but delivery was fast.",
    "I am happy with my purchase, and the packaging was perfect!",
    "It didn't work as advertised. Very disappointed."
]

@app.route('/')
def index():
    return render_template('index.html', reviews=reviews)

@app.route('/generate', methods=['POST'])
def generate():
    review = request.json['review']
    chat = [system_prompt, {"role": "user", "content": review + postfix}]
    try:
        # Use the new client interface
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=chat
        )
        message = response.choices[0].message.content
        return jsonify({'email': message})
    except Exception as e:
        return jsonify({'email': f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
