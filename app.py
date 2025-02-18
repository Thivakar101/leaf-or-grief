import os
import google.generativeai as genai
from flask import Flask, request, render_template
from PIL import Image
import io
import html  # Add this import

app = Flask(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyDNwrt9gH5iSEKJH4VY548Nr7TDIkhvPB4"  # Replace with your Gemini API Key
genai.configure(api_key=GEMINI_API_KEY)

# Load Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-002")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process-image', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return render_template('error.html', error_message="No image uploaded")

    image = request.files['image']
    
    try:
        # Convert image bytes to PIL Image
        image_data = image.read()
        image_pil = Image.open(io.BytesIO(image_data))

        # Send to Gemini Vision
        gemini_response = model.generate_content(
            ["Analyze the plant in this image and provide the species, health status, and care recommendations all in points and in 60 words IN A HUMORS WAY AND IN POINTS LIKE HEALTH IN A SINGLE LINE AND THEN NEXT SECTION IN NEWLINE WITH ONE LINE GAP BEFORE EACH STAR and also dont use (') this ", image_pil]
        )

        response_text = gemini_response.text if gemini_response else "No response from Gemini."

        # Decode HTML entities
        clean_response = html.unescape(response_text)

        return render_template('results.html', gemini_response=clean_response)

    except Exception as e:
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)


AIzaSyDNwrt9gH5iSEKJH4VY548Nr7TDIkhvPB4

