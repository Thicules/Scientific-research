from keras.models import load_model 
import os


classifier = load_model('road_cnn_model.h5')
import numpy as np
from keras.utils import image_utils

test_image =image_utils.load_img("test.jpg",target_size =(64,64,3))
test_image =image_utils.img_to_array(test_image)
test_image =np.expand_dims(test_image, axis =0)
result = classifier.predict(test_image)
if result[0][0] >= 0.5:
    prediction = 'Bad'
else:
    prediction = 'Good'
print(prediction)