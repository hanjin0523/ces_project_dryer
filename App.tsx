import * as React from 'react';
import { View, Text, Image } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';
import CustomSidebarMenu from './front/src/sideMenu/CustomSidebarMenu';
import MyDrawer from './front/src/sideMenu/MyDrawer'


export default function App() {
  return (
    <NavigationContainer>
      <MyDrawer />
    </NavigationContainer>
  );
}