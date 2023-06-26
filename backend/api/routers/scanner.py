from fastapi import UploadFile, File, Query, APIRouter
from api.response import ApiResponse
from PIL import Image
import easyocr
import tempfile
# from keras_ocr.tools import read
# import keras_ocr


router = APIRouter(prefix="")


@router.post("/extract-text")
async def extract_text_from_image(image: UploadFile = File(...)):
    try:
        reader = easyocr.Reader(['en'])
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the uploaded image to the temporary directory
            temp_image_path = f"{temp_dir}/uploaded_image.jpg"
            with open(temp_image_path, "wb") as f:
                f.write(await image.read())

            # Read text from the uploaded image
            result = reader.readtext(temp_image_path)
            text = " ".join([res[1] for res in result])
        data = {"text": text}
        return ApiResponse.response_ok(data=data)
    except Exception as e:
        return ApiResponse.response_internal_server_error(e=str(e))



# @app.post("/extract-text")
# async def extract_text_from_image(image: UploadFile = File(...)):
#     pipeline = keras_ocr.pipeline.Pipeline()
#     image = read(image.file)
#     prediction_groups = pipeline.recognize([image])
#     predicted_image = prediction_groups[0]
#     recognized_text = " ".join([text for text, _ in predicted_image])
#     return {"text": recognized_text}