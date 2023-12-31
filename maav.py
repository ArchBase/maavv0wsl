import os
import gb
import time
import numpy as np
import tensorflow as tf
import pickle

from keras.backend import clear_session
from itertools import chain
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model as load_model


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Model:
    def __init__(self, dataset_length):
        self.tokenizer = Tokenizer()

        print("\n\nreading dataset")
        (self.questions, self.answers) = gb.read_from_paraquet(limit=dataset_length)
        self.answers = [answer for answer in self.answers if answer is not None]
        self.questions = [question for question in self.questions if question is not None]
        all_texts = self.questions + self.answers
        #all_texts = [text for text in all_texts if text]

        #print(self.questions[0] + "\n***********************************\n" + self.answers[0])
        # Tokenize the text data
        
        self.tokenizer.fit_on_texts(all_texts)
        self.question_sequences = self.tokenizer.texts_to_sequences(self.questions)
        self.answer_sequences = self.tokenizer.texts_to_sequences(self.answers)

        # Pad sequences to ensure uniform length
        self.max_sequence_length = max(max(map(len, self.question_sequences)), max(map(len, self.answer_sequences)))

        self.padded_question_sequences = pad_sequences(self.question_sequences, maxlen=self.max_sequence_length, padding='post')
        self.padded_answer_sequences = pad_sequences(self.answer_sequences, maxlen=self.max_sequence_length, padding='post')
        
    def train_steps(self, epochs=1):
        clear_session()

        # Define a list of batch sizes to try
        batch_sizes_to_try = [2048, 1024, 512, 256, 128, 32, 16, 8, 4, 2, 1]

        for batch_size in batch_sizes_to_try:
            try:
                print(f"Working with batch_size = {batch_size}")
                
                # Create a new model for each attempt to avoid issues with model state
                self.model = tf.keras.Sequential([
                    tf.keras.layers.Embedding(input_dim=len(self.tokenizer.word_index) + 1, output_dim=64, input_length=self.max_sequence_length),
                    tf.keras.layers.LSTM(100, return_sequences=True),
                    tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(len(self.tokenizer.word_index) + 1, activation='softmax'))
                ])

                # Compile the model
                self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

                # Train the model with the current batch size
                self.model.fit(self.padded_question_sequences, np.expand_dims(self.padded_answer_sequences, -1), epochs=epochs, batch_size=batch_size)

                return  # If successful, exit the loop
            except Exception as e:
                print(f"Batch size {batch_size} failed. Trying smaller batch size.")
                continue

        print("All batch sizes failed. Training with a default batch size.")
        self.model.fit(self.padded_question_sequences, np.expand_dims(self.padded_answer_sequences, -1), epochs=epochs, batch_size=8)

    def train_stepsd(self, epochs=1):
        clear_session()
        #9999999999999999
        batch_sizes_to_try = [9999999999999999, 999999999999, 99999999, 9999, 2048, 1024, 512, 256, 128, 32, 16, 8, 4, 2, 1]  # Add more sizes as needed

        for batch_size in batch_sizes_to_try:
            clear_session()
            try:
                print(f"Working with batch_size = {batch_size}")
                self.model.fit(self.padded_question_sequences, np.expand_dims(self.padded_answer_sequences, -1), epochs=epochs, batch_size=batch_size)
                return  # If successful, exit the loop
            except Exception as e:
                print(f"Batch size {batch_size} failed. Trying smaller batch size.")
                continue

        """
        try:
             self.model.fit(self.padded_question_sequences, np.expand_dims(self.padded_answer_sequences, -1), epochs=epochs, batch_size=2048)

        except Exception as e:
            clear_session()
            print("All batch sizes failed. Training with a default batch size.")
            self.model.fit(self.padded_question_sequences, np.expand_dims(self.padded_answer_sequences, -1), epochs=epochs, batch_size=8)
"""


    def bake_model(self, epochs=200):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Embedding(input_dim=len(self.tokenizer.word_index) + 1, output_dim=64, input_length=self.max_sequence_length),
            tf.keras.layers.LSTM(1000, return_sequences=True),
            #tf.keras.layers.LSTM(1000, return_sequences=True),
            #tf.keras.layers.LSTM(1, return_sequences=True),
            tf.keras.layers.TimeDistributed(tf.keras.layers.Dense(len(self.tokenizer.word_index) + 1, activation='softmax'))
        ])

        # Compile the model
        self.model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # Train the model
        #self.model.fit(self.padded_question_sequences, np.expand_dims(self.padded_answer_sequences, -1), epochs=epochs, batch_size=999999999999999999)
        #self.model.save('my_model.mdl')
    
    def generate_text(self, query=""):
        # Convert sequences back to text
        def sequences_to_text(sequences, reverse_word_index):
            return ' '.join([reverse_word_index.get(word_index, '') for word_index in sequences])

        self.query = [query]

        # Convert new questions to sequences
        new_question_sequences = self.tokenizer.texts_to_sequences(self.query)

        # Pad new sequences
        padded_new_question_sequences = pad_sequences(new_question_sequences, maxlen=self.max_sequence_length, padding='post')

        # Make predictions
        predicted_answer_sequences = self.model.predict(padded_new_question_sequences)

        # Reverse the word index
        reverse_word_index = {v: k for k, v in self.tokenizer.word_index.items()}
        self.predicted_answers = []
        # Convert predicted sequences to text
        for i, sequence in enumerate(predicted_answer_sequences):
            predicted_answer_text = sequences_to_text(tf.argmax(sequence, axis=-1).numpy(), reverse_word_index)
            self.predicted_answers.append(predicted_answer_text)

        return self.predicted_answers

class Transformer:
    def __init__(self, load_from_file=False, dataset_length=100) -> None:
        if load_from_file:
            # Load the object from the file
            with open('my_model.mdl', 'rb') as file:
                self.model = pickle.load(file)
            return

        self.model = Model(dataset_length)
        self.model.bake_model()
    def bake_existing_model(self, epochs):
        self.model.train_steps(epochs=epochs)
    def bake_model_step_by_step(self, epochs):
        self.model.train_steps(epochs)
        
    def save(self, obj):
        # Save the object to a file
        with open('my_model.mdl', 'wb') as file:
            pickle.dump(self.model, file)
        obj.config(text="Model saved")
    def generate_response(self, query):
        return self.model.generate_text(query)
    def train_entire_dataset(self):
        (self.questions, self.answers) = gb.read_from_paraquet(limit=-1)
