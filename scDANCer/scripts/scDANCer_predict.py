# -*- coding: utf-8 -*-

# Commented out IPython magic to ensure Python compatibility.
## Author: Kathryn O'Neill
## Description: A classifier on weighted gene co-expression network eigengenes

# %tensorflow_version 2.x
from __future__ import absolute_import, division, print_function, unicode_literals

import sys, os
import tensorflow as tf
import pandas as pd
import numpy as np
tf.keras.backend.clear_session()  # For easy reset of notebook state.
from tensorflow import keras
from keras import layers
from keras import utils

print("Tensorflow version: %s" % (tf.__version__))
print("Keras version: %s" % (keras.__version__))
print("Pandas version: %s" % (pd.__version__))

if len(sys.argv) <= 2:
    print("scDANCer_predict.py [file with eigenvalues] [model weights]")
    exit(1)


# Define a classifier for prediction

inputs = layers.Input(shape=(17,))
x = layers.Dense(5,activation='relu')(inputs)
outputs = layers.Dense(3,activation='softmax')(x)

scpseudo_subtype_classifier = tf.keras.Model(inputs,outputs)

#Predict on new data with old model but report data with more info

scpseudo_subtype_classifier.load_weights(sys.argv[2])

#Read input dataset

input_df_new = pd.read_csv(sys.argv[1], sep = '\t', index_col = 0)
print(input_df_new)

#input_df_new = input_df_new.iloc[:,:-1]
sample_idxs = input_df_new.index

X_all = input_df_new.values

softmax_output = scpseudo_subtype_classifier.predict(X_all)
softmax_df = pd.DataFrame(softmax_output, index=sample_idxs)

categorical_output = np.argmax(scpseudo_subtype_classifier.predict(X_all), axis=-1)
categorical_df = pd.DataFrame(categorical_output, index=sample_idxs)

one_outputs = [scpseudo_subtype_classifier.layers[1].output] # Extracts the outputs of the 1st layer
activation_model =  tf.keras.Model(inputs=scpseudo_subtype_classifier.input, outputs=one_outputs) # Creates a model that will return these outputs, given the model input
activations = activation_model.predict(X_all)
activations_df = pd.DataFrame(activations,index = sample_idxs)

X_new_pred_full = pd.concat([activations_df, softmax_df, categorical_df], axis=1)
X_new_pred_full.columns = ["act_0", "act_1", "act_2", "act_3","act_4","soft_0","soft_1","soft_2","class"]

print(X_new_pred_full)

outfile = os.path.basename(sys.argv[1])
outfile = os.path.splitext(outfile)[0] + "_classifier_out.tsv"
X_new_pred_full.to_csv(outfile, sep='\t', header=True)