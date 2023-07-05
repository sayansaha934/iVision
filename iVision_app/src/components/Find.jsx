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
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Header from "./Header";
import CaptureObject from "./CaptureObject";
import ObjectList from "./ObjectList";
import BoxButton from "./BoxButton";
import { useNavigation } from "@react-navigation/native";
import { useRoute } from "@react-navigation/native";
import * as Speech from "expo-speech";
import { findObject, recogniseFace } from "../api";
const Find = () => {
  const btnOptions = ["Find People", "Find Object", "Teach"];
  const [cameraRef, setCameraRef] = useState(null);
  const [detecting, setDetecting] = useState(false);
  const [selected, setSelected] = useState(false);
  const navigation = useNavigation();
  const route = useRoute();

  speak = (text) => {
    Speech.speak(text);
  };

  const handleDetection = async (cameraRef) => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      console.log(photo.uri);
      // const { isDetected, data } = await findObject({ photoURI: photo.uri });
      findObject({ photoURI: photo.uri })
        .then((res) => {
          if (res.status === 200) {
            const predictions = res?.data?.data?.predictions;
            if (predictions && predictions.length > 0) {
              const text = predictions[0].label;
              speak(text);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  const handleFindObject = () => {
    // selected ? setSelected(false) : setSelected(true);
    if (!detecting) {
      handleDetection(cameraRef);
      setDetecting(true);
    } else {
      setDetecting(false);
    }
  };

  const handleTeach = () => {
    navigation.navigate("Teach");
  };
  const handleFindPeople = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      console.log(photo.uri);
      recogniseFace({ photoURI: photo.uri })
        .then((res) => {
          if (res.status === 200) {
            const name = res?.data?.data?.name
            if (name) {
              speak(name);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  const handleOnPress = (label) => {
    if (label == "Find Object") {
      handleFindObject();
    } else if (label == "Teach") {
      handleTeach();
    } else if (label == "Find People") {
      handleFindPeople();
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
    </SafeAreaView>
  );
};
export default Find;
