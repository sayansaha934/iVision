import React, { useState, useEffect } from "react";
import { View, Text, FlatList } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import Header from "./Header";
import CaptureObject from "./CaptureObject";
import BoxButton from "./BoxButton";
import * as Speech from "expo-speech";
import { describeScene } from "../api";
const Identify = () => {
  const btnOptions = ["Describe Scene"];
  const [cameraRef, setCameraRef] = useState(null);
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
            <BoxButton label={item} handleOnPress={handleDescribeScene} />
          )}
          keyExtractor={(item) => item}
          contentContainerStyle={{ columnGap: 50 }}
          horizontal
        />
      </View>
    </SafeAreaView>
  );
};

export default Identify;
