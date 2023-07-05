import React, { useState, useEffect, useRef } from "react";
import { useNavigation } from "@react-navigation/native";
import {
  Text,
  View,
  TouchableOpacity,
  FlatList,
  Image,
  StyleSheet,
} from "react-native";
import CaptureObject from "./CaptureObject";
import BoxButton from "./BoxButton";
import { SafeAreaView } from "react-native-safe-area-context";
import Header from "./Header";
import { extractText } from "../api";
import handleCaptureButtonPress from "./common";
import * as Speech from "expo-speech";

const Read = () => {
  const btnOptions = ["Scan"];
  const [cameraRef, setCameraRef] = useState(null);
  const handleExtractText = async () => {
    if (cameraRef) {
      const photo = await cameraRef.takePictureAsync();
      console.log(photo.uri);
      extractText({ photoURI: photo.uri })
        .then((res) => {
          if (res.status === 200) {
            const text = res.data.data.text;
            if (text) {
              Speech.speak(text);
            }
          }
        })
        .catch((error) => {
          console.log(error);
        });
    }
  };

  return (
    <SafeAreaView>
      <Header />
      <CaptureObject setCameraRef={setCameraRef} />
      <View style={styles.read}>
        <FlatList
          data={btnOptions}
          renderItem={({ item }) => (
            <BoxButton label={item} handleOnPress={handleExtractText} />
          )}
          keyExtractor={(item) => item}
          contentContainerStyle={{ columnGap: 50 }}
          horizontal
        />
      </View>
    </SafeAreaView>
  );
};

export default Read;

const styles = StyleSheet.create({
  read: {
    width: "100%",
    height: 90,
    backgroundColor: "#808080",
    paddingTop: 8,
    alignItems: "center",
  },
});
