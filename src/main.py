import os
import sys
import argparse
from .train import train_model
from .predict import HandwritingPredictor
from .config import MODEL_PATH

def main():
    parser = argparse.ArgumentParser(description="Handwriting Recognition ML Project")
    parser.add_argument("--train", action="store_true", help="Train the model")
    parser.add_argument("--predict", type=str, help="Path to image for prediction")
    parser.add_argument("--demo", action="store_true", help="Run demo prediction")
    
    args = parser.parse_args()
    
    if args.train:
        print("Training mode...")
        train_model()
    elif args.predict:
        print(f"Prediction mode for: {args.predict}")
        if not os.path.exists(MODEL_PATH):
            print(f"Model not found at {MODEL_PATH}. Please train the model first.")
            return
        predictor = HandwritingPredictor()
        result = predictor.predict(args.predict)
        print(f"\nPrediction: {result['predicted_digit']}")
        print(f"Confidence: {result['confidence']:.2%}")
    elif args.demo:
        print("Running demo prediction...")
        if not os.path.exists(MODEL_PATH):
            print(f"Model not found at {MODEL_PATH}. Training model first...")
            train_model()
        
        from tensorflow.keras.datasets import mnist
        (_, _), (X_test, y_test) = mnist.load_data()
        
        predictor = HandwritingPredictor()
        sample_image = X_test[0]
        true_label = y_test[0]
        
        result = predictor.predict(sample_image)
        
        print(f"\nTrue label: {true_label}")
        print(f"Predicted: {result['predicted_digit']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"\nTop 3 predictions:")
        for pred in result['top_3']:
            print(f"  Digit {pred['digit']}: {pred['confidence']:.2%}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
