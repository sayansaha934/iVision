from fastapi import UploadFile, File, Query, APIRouter
from PIL import Image
from io import BytesIO
import torch
from api.response import ApiResponse
from transformers import BlipProcessor, BlipForConditionalGeneration

router = APIRouter(prefix="")


@router.post("/image-caption")
async def generate_image_caption(image: UploadFile = File(...)):
    try:
        # Read the uploaded image file
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        image = Image.open(BytesIO(await image.read())).convert('RGB')
        print("image read done")
        # Unconditional image captioning
        inputs = processor(image, return_tensors="pt")

        out = model.generate(**inputs)
        image_caption = processor.decode(out[0], skip_special_tokens=True)

        data = {"image_caption": image_caption}
        return ApiResponse.response_ok(data=data)
    except Exception as e:
        return ApiResponse.response_internal_server_error(e=str(e))