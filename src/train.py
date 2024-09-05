from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from model import create_model
import tensorflow as tf

import os
from PIL import Image

def print_images_status(directory):
    for subdir, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(subdir, file)
            try:
                img = Image.open(file_path)
                img.verify()  # ตรวจสอบว่าเป็นไฟล์ภาพที่ถูกต้อง
                print(f"Valid image file: {file_path}")
            except (IOError, SyntaxError) as e:
                print(f"Invalid image file: {file_path}")

# เรียกใช้การตรวจสอบและพิมพ์ชื่อไฟล์ทั้งหมด
print_images_status('Melonamo_dataset/train_data')
print_images_status('Melonamo_dataset/validation_data')



def train_model(train_dir, val_dir, epochs=10):
    # Data augmentation and preparation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )

    validation_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(224, 224),
        batch_size=32,
        class_mode='categorical'
    )

    model = create_model()

    # Callbacks
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True
    )
    checkpoint = ModelCheckpoint(
        'model.keras',
        save_best_only=True
    )

    # Train model
    history = model.fit(
        train_generator,
        epochs=epochs,
        validation_data=validation_generator,
        callbacks=[early_stopping, checkpoint]
    )

if __name__ == "__main__":
    train_dir = 'Melonamo_dataset/train_data'
    val_dir = 'Melonamo_dataset/validation_data'
    train_model(train_dir, val_dir)
