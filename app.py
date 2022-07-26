import sys

sys.path.append('find_object')
sys.path.append('describe_scene')
sys.path.append('recog_face')
sys.path.append('scanner')

from find_object.find import find_object
from describe_scene.generate_caption import get_caption
from recog_face.recognition import register_face, recognise_face
from scanner.OCR import ocr

if __name__ == '__main__':
    while True:
        option = int(input('Enter option: '))

        if option==1:
            find_object()
            continue

        elif option==2:
            get_caption()
            continue

        elif option==3:
            register_face()
            continue

        elif option==4:
            recognise_face()
            continue

        elif option==5:
            ocr()
            continue
        else:
            continue





