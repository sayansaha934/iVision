import axios from "axios";
import FormData from "form-data";


const handleCaptureButtonPress = async (cameraRef) => {
    console.log("coming to handleDetection");
    if (cameraRef) {
      try {
        const photo = await cameraRef.takePictureAsync();
        console.log(photo.uri);
      } catch (error) {
        console.log(error);

      }
    }
  };

  export default handleCaptureButtonPress