import tensorflow as tf

# Load the saved model
saved_model = tf.keras.models.load_model('./model.h5')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(saved_model)
tflite_model = converter.convert()

# Save the TFLite model
with open('./model.tflite', 'wb') as f:
    f.write(tflite_model)
