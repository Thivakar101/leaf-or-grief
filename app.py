import os
import google.generativeai as genai
from flask import Flask, request, render_template, jsonify
from PIL import Image
import io
import html

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = "apikeyyyy"  # Replace with your Gemini API Key
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-002")  # Ensure this is the correct model

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for processing the plant image
@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return render_template('error.html', error_message="No image uploaded")

    image = request.files['image']

    try:
        # Convert image bytes to PIL Image
        image_data = image.read()
        image_pil = Image.open(io.BytesIO(image_data))

        # Send to Gemini Vision API
        gemini_response = model.generate_content(
            ["Analyze the plant in this image and provide the species, health status, and care recommendations in a humorous way, all in points and in 60 words. Don't use (') in your response .after each topic leaveee someee lineeeee", image_pil]
        )

        # Check for a valid response
        response_text = gemini_response.text if gemini_response else "No response from Gemini."

        # Decode HTML entities
        clean_response = html.unescape(response_text)

        return render_template('results.html', gemini_response=clean_response)

    except Exception as e:
        return render_template('error.html', error_message=str(e))


# Route for handling chatbot messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    # Send the user's message to the Gemini API for response
    try:
        gemini_response = model.generate_content([user_message])  # Pass the message to the model

        if gemini_response and gemini_response.text:
            # Use the text from the Gemini API response
            response_text = gemini_response.text
        else:
            response_text = "Sorry, I couldn't get a response from Gemini. Please try again later."
    except Exception as e:
        response_text = f"An error occurred while fetching the response: {str(e)}"

    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(debug=True)
