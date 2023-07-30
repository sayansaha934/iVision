import React, { useState, useEffect } from "react";
import { View, Text, FlatList, Modal, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Header from "./Header";
import CaptureObject from "./CaptureObject";
import BoxButton from "./BoxButton";
import * as Speech from "expo-speech";
import { BarCodeScanner } from 'expo-barcode-scanner';
import { StyleSheet } from "react-native";

import { describeScene, detectColor } from "../api";
const Identify = () => {
  // Describe Scene
  const btnOptions = ["Detect Colors"]; // Describe Scene, Scan Barcode
  const [cameraRef, setCameraRef] = useState(null);
  const [modalVisible, setModalVisible] = useState(false);
  const [scannedData, setScannedData] = useState(null);
  


  const handleDescribeScene = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      console.log(photo.uri);
      describeScene({ photoURI: photo.uri })
        .then((res) => {
          if (res.status === 200) {
            const image_caption = res.data.data.image_caption;
            if (image_caption) {
              Speech.speak(image_caption);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  const handleDetectColor = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      console.log(photo.uri);
      detectColor({ photoURI: photo.uri })
        .then((res) => {
          if (res.status === 200) {
            const color = res.data.data.color;
            if (color) {
              Speech.speak(color);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }

  }

  const handleBarCodeScanned = ({ type, data }) => {
    console.log(data)
    setScannedData({ type, data });
    setModalVisible(false);
    Speech.speak(`Bar code with type ${type} and data ${data} has been scanned!`);
    setScannedData(null)
  };
  const handleBarcodeScan = () => {
    setModalVisible(true);
  };

  
  const handleOnPress = (label) => {

    if (label == "Detect Colors") {
      handleDetectColor();
    }
    else if (label == "Scan Barcode") {
      handleBarcodeScan()
    }
  };
  

  return (
    <SafeAreaView>
      <Header />
      <CaptureObject setCameraRef={setCameraRef} />
      <View
        style={{
          width: "100%",
          height: 90,
          backgroundColor: "#808080",
          paddingTop: 8,
          alignItems: "center",
        }}
      >
        <FlatList
          data={btnOptions}
          renderItem={({ item }) => (
            <BoxButton label={item} handleOnPress={() => handleOnPress(item)} />
          )}
          keyExtractor={(item) => item}
          contentContainerStyle={{ columnGap: 50 }}
          horizontal
        />
      </View>
      <Modal
        animationType="slide"
        transparent={false}
        visible={modalVisible}
        onRequestClose={() => {
          setModalVisible(false);
        }}
      >
        <View style={styles.modalContainer}>
          <BarCodeScanner
            onBarCodeScanned={scannedData ? undefined : handleBarCodeScanned}
            style={StyleSheet.absoluteFillObject}
          />
          {/* {scannedData && (
            <TouchableOpacity
              style={styles.button}
              onPress={() => setScannedData(null)}
            >
              <Text style={styles.buttonText}>Scan Again</Text>
            </TouchableOpacity>
          )} */}
        </View>
      </Modal>
    </SafeAreaView>
  );
};

export default Identify;


const styles = StyleSheet.create({
  modalContainer: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'flex-end',
  },
  button: {
    backgroundColor: '#2196F3',
    padding: 16,
    alignItems: 'center',
  },
  buttonText: {
    color: 'black',
    fontSize: 16,
  },
});
