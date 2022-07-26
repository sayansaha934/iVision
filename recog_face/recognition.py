import cv2
import numpy as np
import face_recognition as fr
from pickle import dumps, loads
import os
from voice.generate_voice import generate_voice

embedding_path = 'recog_face/embeddings.pickle'


def register_face():

    if os.path.isdir(embedding_path):
        all_embeddings = loads(open(embedding_path, "rb").read())
        knownEmbeddings = all_embeddings["embeddings"]
        knownNames = all_embeddings["names"]

    else:
        knownEmbeddings = []
        knownNames = []

    name = input('Enter name: ')
    max_faces = 10
    faces = 0
    cap = cv2.VideoCapture(0)


    while faces < max_faces:
        ret, frame = cap.read()

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            face_locations = fr.face_locations(image)
            encoding = fr.face_encodings(image, face_locations)[0]
            faces+=1

            knownEmbeddings.append(encoding)
            knownNames.append(name)

            (top, right, bottom, left) = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.imshow("Face Registration", frame)

        except:
            continue

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    data = {"embeddings": knownEmbeddings, "names": knownNames}
    f = open(embedding_path, "wb")
    f.write(dumps(data))
    f.close()




def recognise_face():
    embeddings = loads(open(embedding_path, "rb").read())
    known_name_encodings = embeddings["embeddings"]
    known_names = embeddings["names"]

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_name_encodings, face_encoding)
            name = ""

            face_distances = fr.face_distance(known_name_encodings, face_encoding)
            best_match = np.argmin(face_distances)

            if matches[best_match]:
                name = known_names[best_match]
            generate_voice(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Face Recognition', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break



