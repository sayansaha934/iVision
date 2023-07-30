import React from 'react';
import { useNavigation } from '@react-navigation/native';
import { View, Text, StyleSheet, TouchableOpacity, FlatList} from 'react-native';

const Footer = () => {
  footerOptions = ['Read', 'Identify', 'Find']  //'Settings'
  const navigation = useNavigation()
  const handleOnPress = (router) => {
    navigation.navigate(router)
  }
  return (
    <View style={styles.footer}>
      <View style={styles.footer}>
        <FlatList
          data={footerOptions}
          renderItem={({item})=>(<TouchableOpacity style={styles.btn} onPress={()=>handleOnPress(item)}><Text>{item}</Text></TouchableOpacity>)}
          keyExtractor = {(item)=>item}
          contentContainerStyle = {{columnGap: 30}}
          horizontal
        />
      </View>
    </View>
  );
};

export default Footer

const styles = StyleSheet.create({
  footer: {
    width: "100%",
    height: 90,
    backgroundColor: "#FFFFFF",
    alignItems: "center",
    paddingTop: 8,
  },
  footerText: {
    fontSize: 16,
    color: "#888",
  },
  btn: {
    height: 50,
    width: 70,
    // backgroundColor: "#FFFFFF",
    justifyContent: "center",
    alignItems: "center",
    borderRadius: 20,
    borderColor: '#000000',
    borderWidth: 2
  },
});