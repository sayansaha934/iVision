from fastapi import UploadFile, File, Query, APIRouter
from PIL import Image
from io import BytesIO
import torch
from typing import Optional

from transformers import YolosImageProcessor, YolosForObjectDetection
from api.response import ApiResponse
from pydantic import BaseModel

router = APIRouter(prefix="")


model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")
image_processor = YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")

@router.post("/find-object")
async def find_object(object_name: Optional[str] = None, image: UploadFile = File(...)):

    try:
        object_present = False
        # Read the uploaded image file
        image_data = await image.read()
        image = Image.open(BytesIO(image_data))


        inputs = image_processor(images=image, return_tensors="pt")
        outputs = model(**inputs)

        # Model predicts bounding boxes and corresponding COCO classes
        logits = outputs.logits
        bboxes = outputs.pred_boxes

        # Post-process the results
        target_sizes = torch.tensor([image.size[::-1]])
        results = image_processor.post_process_object_detection(
            outputs, threshold=0.9, target_sizes=target_sizes
        )[0]

        predictions = []
        for score, label, box in zip(
            results["scores"], results["labels"], results["boxes"]
        ):
            box = [round(i, 2) for i in box.tolist()]
            prediction = {
                "label": model.config.id2label[label.item()],
                "confidence": round(score.item(), 3),
                "box": box,
            }
            predictions.append(prediction)
        if object_name:
            object_present = any(
                object_name.lower() == p["label"].lower() for p in predictions
            )
        data = {"predictions": predictions, "object_present": object_present}
        return ApiResponse.response_ok(data=data)
    except Exception as e:
        return ApiResponse.response_internal_server_error(str(e))
