from fastapi import UploadFile, File, Query, APIRouter
from pickle import dumps, loads
import tempfile
import os
import numpy as np
from io import BytesIO
from PIL import Image
from api.response import ApiResponse
import torch
from torchvision import transforms
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity


resnet = InceptionResnetV1(pretrained='vggface2').eval()


router = APIRouter(prefix="")

@router.post("/register-face")
async def register_face(name: str, image: UploadFile = File(...)):
    embedding_path = 'embeddings.pickle'
    try:
        all_embeddings = {}
        if os.path.isfile(embedding_path):
            all_embeddings = loads(open(embedding_path, "rb").read())

        embeddings = await get_face_embeddings(image)

        all_embeddings[name] = embeddings
        with open(embedding_path, "wb") as f:
            f.write(dumps(all_embeddings))
        data = {"is_registered": True}
        return ApiResponse.response_ok(data=data)
    except Exception as e:
        return ApiResponse.response_internal_server_error(e=str(e))


@router.post("/recognise-face")
async def register_face(image: UploadFile = File(...)):
    try:
        embedding_path = 'embeddings.pickle'
        embeddings_data = loads(open(embedding_path, "rb").read())

        input_embedding = await get_face_embeddings(image)
        input_embedding = np.array(input_embedding).reshape(1,-1)
        max_score=0
        predicted_name=""
        for name, embedding in embeddings_data.items():
            embedding = np.array(embedding).reshape(1,-1)
            similarity_score = cosine_similarity(embedding, input_embedding)[0][0]
            if similarity_score > max_score:
                max_score=similarity_score
                predicted_name = name


        data = {"name": predicted_name}
        return ApiResponse.response_ok(data=data)
    
    except Exception as e:
        ApiResponse.response_internal_server_error(e=str(e))

async def get_face_embeddings(image):
    image = Image.open(BytesIO(await image.read())).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((160, 160)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    image = transform(image).unsqueeze(0)
    with torch.no_grad():
        embeddings = resnet(image)
    embeddings = embeddings.tolist()[0]

    return embeddings
