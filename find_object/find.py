import numpy as np
import tensorflow as tf
import playsound
import cv2
import speech_recognition as sr

from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util



def load_model():
    model_dir = 'find_object/ssd_mobilenet/saved_model'
    model = tf.saved_model.load(str(model_dir))
    model = model.signatures['serving_default']
    return model

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = 'find_object/object_detection/mscoco_label_map.pbtxt'
category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

all_objects = [i['name'] for i in category_index.values()]

def find_object():
    r = sr.Recognizer()

    playsound.playsound('find_object/find1.mp3', block=False)
    while True:
        with sr.Microphone() as source:

            audio = r.listen(source, phrase_time_limit=5)

            try:
                object_name = r.recognize_google(audio)
                object_name = object_name.lower()
                print(object_name)
                if object_name in all_objects:
                    break
                else:
                    playsound.playsound('find_object/find2.mp3', block=False)
                    continue
            except:
                playsound.playsound('find_object/find2.mp3', block=False)
                continue


    detection_model = load_model()

    cap = cv2.VideoCapture(0)


    while True:

        ret, image = cap.read()
        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis, ...]

        # Run inference
        output_dict = detection_model(input_tensor)

        # All outputs are batches tensors.
        # Convert to numpy arrays, and take index [0] to remove the batch dimension.
        # We're only interested in the first num_detections.
        num_detections = int(output_dict.pop('num_detections'))
        output_dict = {key: value[0, :num_detections].numpy()
                       for key, value in output_dict.items()}
        output_dict['num_detections'] = num_detections

        # detection_classes should be ints.
        output_dict['detection_classes'] = output_dict['detection_classes'].astype(np.int64)
        # Actual detection.
        for item_id in output_dict['detection_classes']:
            if category_index[item_id]['name'] == object_name:
                playsound.playsound('find_object/notification.wav')
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image,
                    output_dict['detection_boxes'],
                    output_dict['detection_classes'],
                    output_dict['detection_scores'],
                    category_index,
                    instance_masks=output_dict.get('detection_masks_reframed', None),
                    use_normalized_coordinates=True,
                    line_thickness=8)


        cv2.imshow('object detection', cv2.resize(image, (800, 600)))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

