import React from "react";
import { StyleSheet, View, TouchableOpacity, Text } from "react-native";

const BoxButton = ({ label, handleOnPress, selected = false }) => {
  return (
    <View>
      <TouchableOpacity style={styles.btn(selected)} onPress={handleOnPress}>
        <Text style={styles.btnText}>{label}</Text>
      </TouchableOpacity>
    </View>
  );
};

export default BoxButton;

const styles = StyleSheet.create({
  btn: (selected) => ({
    backgroundColor: selected ? "#00FF00" : "#DFD3E3",
    height: 70,
    width: 80,
    borderRadius: 15,
    alignItems: "center",
    justifyContent: "center",
  }),
  btnText: {
    fontSize: 17,
    textAlign: "center",
  },
});
