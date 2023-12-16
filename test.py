import numpy as np
import random
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('text_generation_model.h5')

# Function to generate text given a seed text
def generate_text(model, start_string, num_generate=1000, temperature=1.0):
    input_eval = [char2idx[char] for char in start_string]
    input_eval = tf.expand_dims(input_eval, 0)
    text_generated = []

    model.reset_states()
    for _ in range(num_generate):
        predictions = model(input_eval)
        predictions = tf.squeeze(predictions, 0) / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1,0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)
        text_generated.append(idx2char[predicted_id])

    return (start_string + ''.join(text_generated))

# Provide a seed text for text generation
seed_text = "Once upon a time"

# Generate text based on the seed
generated_text = generate_text(model, start_string=seed_text, num_generate=500, temperature=0.8)

# Print the generated text
print(generated_text)
