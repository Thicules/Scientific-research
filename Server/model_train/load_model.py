from keras.models import load_model
from PIL import Image
import numpy as np

class ModelRoad:
    def predict(imagePath):
        classifier = load_model('model_train/catdog_cnn_model.h5')
        # Get a list of all image files sorted by modification time
        image_files = imagePath

        # Load the latest image file
        test_image = Image.open(image_files).resize((64, 64))   
        test_image = np.array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = classifier.predict(test_image)
        if result[0][0] >= 0.5:
            prediction = 'dog'
        else:
            prediction = 'cat'
        return prediction