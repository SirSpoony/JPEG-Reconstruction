import os

from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import keras

import model as model

BATCH_SIZE = 4

train_datagen = ImageDataGenerator(rescale=1. / 255)

# Args for the training data generator. Both x and y should be identical,
# so they are put into a tuple
generator_args = dict(
    target_size=(96, 96),
    batch_size=BATCH_SIZE,
    class_mode=None,
    color_mode='grayscale',
    seed=1)

train_generator_x = train_datagen.flow_from_directory('bin/train/compressed/',
                                                      **generator_args)

train_generator_y = train_datagen.flow_from_directory(
    'bin/train/uncompressed/', **generator_args)

train_generator = zip(train_generator_x, train_generator_y)

# Validation data generator
validate_generator_x = train_datagen.flow_from_directory(
    'bin/validate/compressed/', **generator_args)

validate_generator_y = train_datagen.flow_from_directory(
    'bin/validate/uncompressed/', **generator_args)

validate_generator = zip(validate_generator_x, validate_generator_y)

if __name__ == "__main__":
    cb = keras.callbacks.TensorBoard(
        log_dir='./tmp', write_graph=True, write_images=True)

    model = model.get_model()

    model.fit_generator(
        train_generator,
        steps_per_epoch=1000,
        epochs=5,
        validation_data=validate_generator,
        validation_steps=6,
        callbacks=[cb])

    model.save_weights('weights.h5')
    print('Saved weights as weights.h5')
