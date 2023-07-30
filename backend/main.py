from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from api.routers.object_detection import router as object_detection_router
# from api.routers.image_caption import router as image_caption_router
from api.routers.scanner import router as scanner_router
from api.routers.face_recognition import router as face_recognition_router
from api.routers.color_detector import router as color_detector_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this list to specify the allowed origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(image_caption_router)
app.include_router(object_detection_router)
app.include_router(scanner_router)
app.include_router(face_recognition_router)
app.include_router(color_detector_router)



