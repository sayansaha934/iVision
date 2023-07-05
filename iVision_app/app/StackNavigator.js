import { View, Text } from 'react-native'
import React from 'react'
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { Read, Identify, Find, Settings, ObjectList, Teach } from '../src/components';
const Stack = createNativeStackNavigator()

const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown:false}}>
            <Stack.Screen name="Read" component={Read} options={{unmountOnBlur: true}}/>
            <Stack.Screen name="Identify" component={Identify} options={{unmountOnBlur: true}}/>
            <Stack.Screen name="Find" component={Find}/>
            <Stack.Screen name="Settings" component={Settings}/>
            <Stack.Screen name="ObjectList" component={ObjectList}/>
            <Stack.Screen name="Teach" component={Teach}/>
    </Stack.Navigator>
  )
}

export default StackNavigator