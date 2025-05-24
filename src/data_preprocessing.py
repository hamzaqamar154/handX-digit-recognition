import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.datasets import mnist
import os
from .config import DATA_PROCESSED_DIR, IMG_SIZE

def preprocess_image(image):
    if isinstance(image, np.ndarray):
        if image.dtype != np.uint8:
            if image.max() <= 1.0:
                image = (image * 255).astype(np.uint8)
            else:
                image = image.astype(np.uint8)
        image = Image.fromarray(image)
    
    if image.mode != 'L':
        image = image.convert('L')
    
    img_array = np.array(image, dtype=np.float32)
    
    if img_array.max() == img_array.min():
        img_array = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)
        return img_array.reshape(IMG_SIZE, IMG_SIZE, 1)
    
    if img_array.mean() < 128:
        img_array = 255 - img_array
    
    threshold = np.percentile(img_array, 10)
    rows = np.any(img_array < threshold, axis=1)
    cols = np.any(img_array < threshold, axis=0)
    
    if rows.any() and cols.any():
        rmin, rmax = np.where(rows)[0][[0, -1]]
        cmin, cmax = np.where(cols)[0][[0, -1]]
        
        if rmax > rmin and cmax > cmin:
            img_array = img_array[rmin:rmax+1, cmin:cmax+1]
    
    h, w = img_array.shape
    if h == 0 or w == 0:
        img_array = np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.float32)
        return img_array.reshape(IMG_SIZE, IMG_SIZE, 1)
    
    scale = min(20.0 / max(h, w), 1.0)
    new_h, new_w = int(h * scale), int(w * scale)
    
    if new_h > 0 and new_w > 0:
        image = Image.fromarray(img_array.astype(np.uint8))
        image = image.resize((new_w, new_h), Image.LANCZOS)
        img_array = np.array(image, dtype=np.float32)
    
    h, w = img_array.shape
    pad_h = (IMG_SIZE - h) // 2
    pad_w = (IMG_SIZE - w) // 2
    
    img_array = np.pad(img_array, 
                      ((pad_h, IMG_SIZE - h - pad_h), (pad_w, IMG_SIZE - w - pad_w)), 
                      mode='constant', constant_values=255)
    
    img_array = 255 - img_array
    
    img_array = np.clip(img_array, 0, 255)
    
    img_array = img_array / 255.0
    
    img_array = img_array.reshape(IMG_SIZE, IMG_SIZE, 1)
    
    return img_array

def load_mnist_data():
    print("Loading MNIST dataset...")
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    
    X_train = X_train.astype('float32') / 255.0
    X_test = X_test.astype('float32') / 255.0
    
    X_train = X_train.reshape(X_train.shape[0], IMG_SIZE, IMG_SIZE, 1)
    X_test = X_test.reshape(X_test.shape[0], IMG_SIZE, IMG_SIZE, 1)
    
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    
    return X_train, y_train, X_test, y_test

def save_processed_data(X_train, y_train, X_test, y_test):
    os.makedirs(DATA_PROCESSED_DIR, exist_ok=True)
    
    np.save(os.path.join(DATA_PROCESSED_DIR, "X_train.npy"), X_train)
    np.save(os.path.join(DATA_PROCESSED_DIR, "y_train.npy"), y_train)
    np.save(os.path.join(DATA_PROCESSED_DIR, "X_test.npy"), X_test)
    np.save(os.path.join(DATA_PROCESSED_DIR, "y_test.npy"), y_test)
    
    print(f"Processed data saved to {DATA_PROCESSED_DIR}")
