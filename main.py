# Library
import os
import numpy as np
from flask import Flask, render_template, request, jsonify
import random
from io import BytesIO
from skimage.transform import resize
from PIL import Image
import tensorflow as tf

# Library for Google Cloud Storage
"""import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud import storage
"""

# library for time
import pytz
from datetime import datetime, timedelta, timezone


# Initialize Firebase
"""
cred = credentials.Certificate('firebase-key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred)
# Initialize Firestore
db = firestore.client()
"""

# Dictionary mapping model name to their corresponding model files
best_model = {
    'concrate': 'Model/MobileNet_Modified077.h5' # You can add more models here
}

# Function to get the user timezone
def get_user_timezone(offset):
    # Convert offset to seconds
    offset_seconds = offset * 60  # Offset is in minutes
    
    # Create a timedelta object for the offset
    offset_timedelta = timedelta(seconds=offset_seconds)
    
    # Get the current UTC time
    utc_time = datetime.now(timezone.utc)
    
    # Add the offset to the UTC time
    user_local_time = utc_time + offset_timedelta
    
    return user_local_time

# Function to predict the fruit condition
def predict_condition(model_name, image):
    # if the model name is not in the dictionary
    if model_name not in best_model:
        return 'Model not found', 0
    
    # Get model path
    model_path = best_model[model_name]
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    # Read the image
    img = Image.open(image)
    img = img.convert('RGB')  # Ensure image is in RGB mode
    
    # Resize image to match model input shape
    img = img.resize((224, 224))
    
    # Convert image to array
    image_array = tf.keras.preprocessing.image.img_to_array(img)
    
    # Normalize the image
    image_array = image_array / 255.0
    
    # Add batch dimension
    image_array = np.expand_dims(image_array, axis=0)
    
    # Predict the condition of the fruit
    prediction = model.predict(image_array)
    
    # Get the condition of the fruit
    condition = np.argmax(prediction)
    
    # Get confidence
    confidence = prediction[0][condition]
    
    # Get the condition name
    condition_name = ['Negative', 'Positive'][condition]
    
    # Return the condition name and confidence
    return condition_name, confidence

# Initialize Flask app
app = Flask(__name__)

# Endpoint to predict condition
@app.route('/predict', methods=['POST'])
def predict():
    # Get user id from the request
    UID = request.form['user_id']
    # If the user id is not provided
    if not UID:
        return jsonify({'error': 'No user id provided'})

    # Get the image from the request
    image = request.files['image']
    # If the image is not provided
    if not image:
        return jsonify({'error': 'No image provided'})
    
    # Get the fruit name from the request
    model_name = request.form['model_name']
    # If the model name is not provided
    if not model_name:
        return jsonify({'error': 'No model name provided'})
    
    # Predict the condition
    condition, confidence = predict_condition(model_name, image)
    
    # Get the current time based on the timezone using pytz
    offset = request.form['offset']
    # If the offset is not provided
    if not offset:
        return jsonify({'error': 'No offset provided'})
    offset = int(offset)
    user_timezone = get_user_timezone(offset)
    
    # Save the prediction to Firestore
    """
    db = firestore.client()
    prediction_ref = db.collection('predictions').document()
    prediction_ref.set({
        'user_id': user_id,
        'condition': condition,
        'confidence': confidence,
        'time': user_timezone
    })
    """

    # Return the prediction
    return jsonify({'User_ID':UID,
                    'condition': condition, 
                    'confidence': float(confidence),
                    'time': user_timezone.strftime("%Y-%m-%d %H:%M:%S %Z")})

# Run the app
if __name__ == '__main__':
    app.run(port=8080, debug=True)