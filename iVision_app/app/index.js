import { View, Text, ScrollView, SafeAreaView } from "react-native";
import { Footer, Read, Identify } from "../src/components";
import { Stack, useRouter } from "expo-router";
import { NavigationContainer } from "@react-navigation/native";
import StackNavigator from "./StackNavigator";
import { StatusBar } from 'expo-status-bar';



const Home = () => {
  return (
    <NavigationContainer independent={true}>
      <StatusBar style={Platform.OS === 'android' ? 'light' : 'dark'} backgroundColor="#8F00FF"/>
      <StackNavigator/>
      <Footer/>
    </NavigationContainer>

  );
};

export default Home;
