import cv2
import easyocr
from voice.generate_voice import generate_voice
import os

path = 'scanner/ocr.jpg'
def ocr():
    cap = cv2.VideoCapture(0)
    while True:
        ret, image = cap.read()

        cv2.imshow('OCR', image)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    cv2.imwrite(path, image)
    reader = easyocr.Reader(['en'])
    result = reader.readtext(path)

    os.remove(path)

    texts = []
    for i in result:
        texts.append(i[1])

    for text in texts:
        generate_voice(text)
