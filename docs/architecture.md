# Architecture

## Overview

CNN-based handwriting recognition system for digits 0-9. Uses TensorFlow/Keras for the model, FastAPI for the API, and Streamlit for the UI.

## Components

**Data Preprocessing** (`src/data_preprocessing.py`)
- Loads MNIST dataset
- Converts to grayscale, resizes to 28x28
- Normalizes pixel values
- Handles canvas images with centering and contrast adjustment

**Model** (`src/model.py`)
- CNN with 3 convolutional blocks
- Batch normalization and dropout
- Outputs 10 classes (digits 0-9)

**Training** (`src/train.py`)
- Trains on MNIST dataset
- Uses data augmentation
- Saves best model based on validation accuracy

**Prediction** (`src/predict.py`)
- Loads trained model
- Preprocesses input images
- Returns predictions with confidence scores

**API** (`api/app.py`)
- FastAPI REST endpoint
- POST /predict for image uploads
- GET /health for health checks

**UI** (`ui/app.py`)
- Streamlit interface
- Drawing canvas for input
- Displays predictions and confidence

## Data Flow

Training: MNIST → Preprocessing → Training → Save Model

Prediction: Image → Preprocessing → Model → Predictions

## Configuration

Settings in `src/config.py`:
- Image size: 28x28
- Batch size: 32
- Epochs: 10
- Learning rate: 0.001
