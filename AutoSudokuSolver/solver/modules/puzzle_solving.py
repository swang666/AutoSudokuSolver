import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import random
import gc
from keras import layers
from keras import models
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array, load_img
from keras.models import load_model
from .algorithm import solve
import datetime
import os

def read_puzzle(puzzle):
    base = os.path.dirname(os.path.realpath(__file__))
    model_dir = os.path.join(base, 'models/digit_rec_model2.h5')
    model = load_model(model_dir)
    
    X = []
    for i in range(0,9):
        for j in range(0,9):       
            crop_img = puzzle[i * 40: (i+1)*40, j * 40: (j+1)*40]
            crop_img = cv2.resize(crop_img, (150,150), interpolation = cv2.INTER_CUBIC)
            crop_img =  np.expand_dims(crop_img, axis=-1)
            crop_img =  np.expand_dims(crop_img, axis=0)
            X.append(crop_img)
            

    x = np.array(X)
    

    board = []
    for i in range(0,9):
        y = [0] * 9
        for j in range(0,9):
            y[j] = model.predict_classes(x[i*9+j])[0]
        print(y)
        board.append(y)

    return board

def solve_puzzle(board):
    solution = solve(board)
    return solution