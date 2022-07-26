import os
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.models import load_model
from pickle import load
import numpy as np
from PIL import Image
import cv2
from voice.generate_voice import generate_voice


def extract_features(filename, model):
        try:
            image = Image.open(filename)
            
        except:
            print("ERROR: Couldn't open image! Make sure the image path and extension is correct")
        image = image.resize((299,299))
        image = np.array(image)
        # for images that has 4 channels, we convert them into 3 channels
        if image.shape[2] == 4: 
            image = image[..., :3]
        image = np.expand_dims(image, axis=0)
        # image = image/127.5
        # image = image - 1.0
        image = preprocess_input(image)
        feature = model.predict(image)
        return feature

def word_for_id(integer, tokenizer):
 for word, index in tokenizer.word_index.items():
     if index == integer:
         return word
 return None


def generate_desc(model, tokenizer, photo, max_length):
    in_text = 'start'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        pred = model.predict([photo,sequence], verbose=0)
        pred = np.argmax(pred)
        word = word_for_id(pred, tokenizer)
        if word is None:
            break
        in_text += ' ' + word
        if word == 'end':
            break
    in_text = ' '.join(in_text.split()[1:-1])
    return in_text


max_length = 32
tokenizer = load(open("describe_scene/tokenizer.pickle","rb"))
model = load_model('describe_scene/models/model_32.h5')
inception_model = InceptionV3(include_top=False, pooling="avg")


def get_caption():
    cap = cv2.VideoCapture(0)
    ret, image = cap.read()
    del (cap)
    img_path = 'describe_scene/scene.jpg'
    cv2.imwrite(img_path, image)
    cv2.imshow('Scene', image)
    photo = extract_features(img_path, inception_model)
    img = Image.open(img_path)
    description = generate_desc(model, tokenizer, photo, max_length)
    img.close()
    os.remove(img_path)
    generate_voice(description)
    cv2.waitKey(0)
    cv2.destroyAllWindows()









