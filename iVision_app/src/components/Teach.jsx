import React, {
  useState,
  useEffect,
  useSyncExternalStore,
  useRef,
} from "react";
import {
  View,
  Text,
  FlatList,
  TouchableOpacity,
  StyleSheet,
  TextInput,
  Modal,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Header from "./Header";
import CaptureObject from "./CaptureObject";
import { registerFace } from "../api";

const Teach = () => {
  const [cameraRef, setCameraRef] = useState(null);
  const [name, setName] = useState("");
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [photoURI, setPhotoURI] = useState(null);

  const handleRegisterFace = async () => {
    if (cameraRef) {
      try {
        const photo = await cameraRef.takePictureAsync();
        setPhotoURI(photo.uri);
        setIsModalVisible(true);
      } catch (error) {
        console.log(error);
      }
    }
  };
  const handleModalClose = async () => {
    setIsModalVisible(false);
    if (photoURI) {
      registerFace({ name: name, photoURI: photoURI })
        .then((res) => {
          if (res.status === 200) {
            if (res?.data?.data?.isRegistered === true) {
              console.log("Face Registeration successfull!");
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
    setPhotoURI(null);
    setName("");
  };
  return (
    <SafeAreaView>
      <Header />
      <CaptureObject setCameraRef={setCameraRef} />
      <View
        style={{
          width: "100%",
          height: 90,
          backgroundColor: "#FFFFFF",
          paddingTop: 8,
          alignItems: "center",
        }}
      >
        <TouchableOpacity onPress={handleRegisterFace} style={styles.btn} />
      </View>

      <Modal
        visible={isModalVisible}
        onRequestClose={handleModalClose}
        animationType="slide"
      >
        <View style={styles.modalContainer}>
          <Text style={styles.modalTitle}>Enter Name</Text>
          <TextInput
            style={styles.modalInput}
            placeholder="Name"
            value={name}
            onChangeText={setName}
          />
          <TouchableOpacity
            onPress={handleModalClose}
            style={styles.modalButton}
          >
            <Text style={styles.modalButtonText}>Submit</Text>
          </TouchableOpacity>
        </View>
      </Modal>
    </SafeAreaView>
  );
};

export default Teach;

const styles = StyleSheet.create({
  btn: {
    backgroundColor: "#FFFFFF",
    height: 70,
    width: 80,
    borderRadius: 30,
    borderColor: "#000000",
    borderWidth: 4,
    alignItems: "center",
    justifyContent: "center",
  },
  modalContainer: {
    flex: 1,
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgba(0, 0, 0, 0.5)",
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: "bold",
    marginBottom: 10,
    color: "#FFFFFF",
  },
  modalInput: {
    height: 40,
    width: 300,
    borderColor: "gray",
    borderWidth: 1,
    borderRadius: 4,
    marginBottom: 10,
    paddingHorizontal: 10,
    backgroundColor: "#FFFFFF",
  },
  modalButton: {
    backgroundColor: "#FFFFFF",
    height: 40,
    width: 100,
    borderRadius: 20,
    alignItems: "center",
    justifyContent: "center",
  },
  modalButtonText: {
    fontSize: 16,
    fontWeight: "bold",
    color: "#000000",
  },
});
