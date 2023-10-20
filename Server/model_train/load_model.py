from keras.models import load_model
from PIL import Image
import numpy as np

class ModelRoad:
    def predict(imagePath):
        classifier = load_model('model_train/road_EfficientNetB4_model150.h5')
        # Get a list of all image files sorted by modification time
        image_files = imagePath

        # Load the latest image file
        test_image = Image.open(image_files).resize((150, 150))   
        test_image = np.array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        y_pred = classifier.predict(test_image)
        y_pred =np.array(y_pred)
        y_pred =y_pred.flatten()
        if y_pred[0] < 0:
            prediction = 'Bad'
        else:
            prediction = 'Good'
        return prediction