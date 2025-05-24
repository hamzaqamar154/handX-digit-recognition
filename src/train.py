import os
import numpy as np
from tensorflow import keras
from .model import create_model
from .data_preprocessing import load_mnist_data
from .config import MODEL_PATH, EPOCHS, BATCH_SIZE, MODELS_DIR

def train_model():
    print("=" * 50)
    print("Starting model training...")
    print("=" * 50)
    
    X_train, y_train, X_test, y_test = load_mnist_data()
    
    print("\nCreating model architecture...")
    model = create_model()
    model.summary()
    
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    callbacks = [
        keras.callbacks.ModelCheckpoint(
            MODEL_PATH,
            save_best_only=True,
            monitor='val_accuracy',
            mode='max',
            verbose=1
        ),
        keras.callbacks.EarlyStopping(
            monitor='val_accuracy',
            patience=3,
            restore_best_weights=True
        )
    ]
    
    from tensorflow.keras.preprocessing.image import ImageDataGenerator
    
    datagen = ImageDataGenerator(
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        zoom_range=0.15,
        shear_range=0.1
    )
    
    print(f"\nTraining for {EPOCHS} epochs with data augmentation...")
    history = model.fit(
        datagen.flow(X_train, y_train, batch_size=BATCH_SIZE),
        steps_per_epoch=len(X_train) // BATCH_SIZE,
        epochs=EPOCHS,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    
    print("\nEvaluating model on test set...")
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Test loss: {test_loss:.4f}")
    
    print(f"\nModel saved to {MODEL_PATH}")
    print("=" * 50)
    
    return model, history

if __name__ == "__main__":
    train_model()
