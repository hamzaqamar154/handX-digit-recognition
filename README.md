# HandX-Handwriting recognition

I built this handwriting recognition project to recognize handwritten digits using deep learning. It's a complete end-to-end solution with a CNN model, training pipeline, API, and a simple web interface.

## What This Does

This project recognizes handwritten digits (0-9) using a Convolutional Neural Network. You can draw digits on a canvas and get predictions in real-time.

## Project Structure

```
handwriting-recognition-ml/
├── src/
│   ├── config.py              # Configuration settings
│   ├── data_preprocessing.py  # Image preprocessing
│   ├── model.py               # CNN model architecture
│   ├── train.py               # Training script
│   ├── predict.py             # Prediction module
│   └── main.py                # Main entry point
├── api/
│   └── app.py                 # FastAPI application
├── ui/
│   └── app.py                 # Streamlit UI
├── data/
│   ├── raw/                   # Raw data
│   └── processed/             # Processed data
├── models/                    # Saved model files
├── docs/
│   └── architecture.md        # Architecture docs
├── tests/                     # Test files
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Installation

1. Navigate to the project directory:
   ```bash
   cd handwriting-recognition-ml
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

That's it! Pretty straightforward.

## Usage

### 1. Train the Model

First, you need to train the model on the MNIST dataset:

```bash
python train_model.py
```

Or if you prefer:
```bash
python -m src.main --train
```

The model will be saved to `models/handwriting_model.h5`. Training takes about 3-4 minutes on a regular CPU.

### 2. Run the Web Interface

Launch the Streamlit UI:

```bash
streamlit run ui/app.py
```

Then open your browser to the URL shown (usually `http://localhost:8501`).

**How to use:**
- Draw a digit (0-9) on the canvas
- Click "Predict" to see the result
- Use "Clear Canvas" to start over

### 3. Run the API (Optional)

If you want to use the REST API:

```bash
uvicorn api.app:app --reload
```

The API will be available at `http://localhost:8000`.

**API Endpoints:**
- `GET /` - API info
- `GET /health` - Health check
- `POST /predict` - Upload an image and get prediction

**Example API call:**
```bash
curl -X POST "http://localhost:8000/predict" -F "file=@your_image.png"
```

## Model Details

The CNN model has:
- 3 convolutional blocks with batch normalization
- MaxPooling layers for downsampling
- Dense layers with dropout for regularization
- Softmax output for 10 digit classes (0-9)

See `docs/architecture.md` for more details.

## Features

- Image preprocessing (grayscale, resize, normalize, contrast enhancement)
- CNN model with batch normalization
- Model evaluation with accuracy metrics
- FastAPI REST API
- Simple Streamlit UI with drawing canvas
- Top-3 predictions display
- Confidence scores

## Performance

The model achieves:
- **Test Accuracy**: 99.56% on MNIST test set
- **Training Time**: ~3-4 minutes on CPU (10 epochs)

## Technologies Used

- **TensorFlow/Keras**: Deep learning framework
- **Streamlit**: Web UI framework
- **FastAPI**: REST API framework
- **Pillow**: Image processing
- **NumPy**: Numerical operations
- **MNIST Dataset**: Training data

## Notes

- The model is trained on MNIST dataset (28x28 grayscale images)
- Works best with clear, centered digits
- The UI uses a drawing canvas - just draw and predict!
- Model automatically downloads MNIST on first run
- Preprocessing handles canvas images with automatic centering and contrast enhancement

## Tips for Best Results

- Draw digits clearly in the center of the canvas
- Make sure the digit is reasonably sized (not too small or too large)
- The model works best with single digits

## Deployment

### Docker

The project includes Docker support for easy deployment:

```bash
cp env.example .env
docker-compose up -d
```

Access at http://localhost:8000 (API) and http://localhost:8501 (UI).



### Environment Variables

Copy `env.example` to `.env`. Main settings:
- `ENVIRONMENT`: development or production
- `API_PORT`: API port (default 8000)
- `STREAMLIT_PORT`: UI port (default 8501)
- `CORS_ORIGINS`: Allowed origins (comma-separated)

---

**Author** Mirza Noor Hamza
