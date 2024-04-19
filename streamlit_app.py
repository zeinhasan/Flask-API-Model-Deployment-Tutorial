import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# Dictionary mapping model name to their corresponding model files
best_model = {
    'concrate': 'Model\MobileNet_Modified077.h5' # You can add more models here
}

# Function to predict the fruit condition
def predict_condition(model_name, image):
    # if the model name is not in the dictionary
    if model_name not in best_model:
        return 'Model not found', 0
    
    # Get model pathModel\MobileNet_Modified077.h5
    model_path = best_model[model_name]
    
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    # Resize image to match model input shape
    img = image.resize((224, 224))
    
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

# Streamlit app
def main():
    st.title("Fruit Condition Prediction")

    # File uploader for image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    # Select model
    model_name = st.selectbox("Select Model", list(best_model.keys()))

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Button to predict
        if st.button("Predict"):
            condition, confidence = predict_condition(model_name, image)
            st.success(f"Predicted Condition: {condition}, Confidence: {confidence:.2f}")

if __name__ == "__main__":
    main()
