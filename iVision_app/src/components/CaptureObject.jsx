import React, { useState, useEffect, useRef } from "react";
import { Camera } from 'expo-camera';
import { Text, View, TouchableOpacity, Platform, StyleSheet } from "react-native";
import { useIsFocused } from '@react-navigation/native';


const CaptureObject = ({ setCameraRef }) => {
  const [hasPermission, setHasPermission] = useState(null);
  // const [cameraRef, setCameraRef] = useState(null);
  const isFocused = useIsFocused();



  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();

  }, []);

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }


  return (
    <View style={styles.camera}>
      {isFocused && <Camera
        style={styles.camera}
        ref={(ref) => setCameraRef(ref)}
        type={Camera.Constants.Type.back}
      />}
    </View>
  );
};


export default CaptureObject;


const styles = StyleSheet.create({
  camera: {
    width: '100%',
    height: Platform.OS === 'ios'? 390 : 550
  },
  button: {
    backgroundColor: '#8F00FF',
    padding: 20,
  },
  buttonText: {
    fontSize: 10,
    color: '#000000',
  },
});
