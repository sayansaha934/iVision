from fastapi import UploadFile, File, Query, APIRouter
from pickle import dumps, loads
import tempfile
import os
import face_recognition as fr
from api.response import ApiResponse




router = APIRouter(prefix="")

@router.post("/register-face")
async def register_face(name: str, image: UploadFile = File(...)):
    embedding_path = 'embeddings.pickle'
    try:
        if os.path.isdir(embedding_path):
            all_embeddings = loads(open(embedding_path, "rb").read())
            knownEmbeddings = all_embeddings["embeddings"]
            knownNames = all_embeddings["names"]

        else:
            knownEmbeddings = []
            knownNames = []

        with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded image to the temporary directory
            temp_image_path = f"{temp_dir}/uploaded_image.jpg"
            with open(temp_image_path, "wb") as f:
                f.write(await image.read())
            image = fr.load_image_file(temp_image_path)

        face_locations = fr.face_locations(image)
        encoding = fr.face_encodings(image, face_locations)[0]
        knownEmbeddings.append(encoding)
        knownNames.append(name)

        data = {"embeddings": knownEmbeddings, "names": knownNames}
        f = open(embedding_path, "wb")
        f.write(dumps(data))
        f.close()
        data = {"is_registered": True}
        return ApiResponse.response_ok(data=data)
    except Exception as e:
        return ApiResponse.response_internal_server_error(str(e))


@router.post("/recognise-face")
async def register_face(image: UploadFile = File(...)):
    try:
        embedding_path = 'embeddings.pickle'
        embeddings = loads(open(embedding_path, "rb").read())
        known_name_encodings = embeddings["embeddings"]
        known_names = embeddings["names"]

        with tempfile.TemporaryDirectory() as temp_dir:
        # Save the uploaded image to the temporary directory
            temp_image_path = f"{temp_dir}/uploaded_image.jpg"
            with open(temp_image_path, "wb") as f:
                f.write(await image.read())
            image = fr.load_image_file(temp_image_path)

        face_locations = fr.face_locations(image)
        face_encodings = fr.face_encodings(image, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = fr.compare_faces(known_name_encodings, face_encoding)
                name = ""

                face_distances = fr.face_distance(known_name_encodings, face_encoding)
                best_match = np.argmin(face_distances)

                if matches[best_match]:
                    name = known_names[best_match]
        data = {"name": name}
        return ApiResponse.response_ok(data=data)
    
    except Exception as e:
        ApiResponse.response_internal_server_error(e=str(e))