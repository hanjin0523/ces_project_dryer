import * as React from 'react';
import { View, Text, Image } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createDrawerNavigator } from '@react-navigation/drawer';

import CustomSidebarMenu from './CustomSidebarMenu';
import Home from '../homeComponent/Home';
import RecipeBox from '../recipeSettingComponent/RecipeBox'

function Article() {
    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <Text>Article Screen</Text>
        </View>
    );
}

const Drawer = createDrawerNavigator();

function MyDrawer() {
    return (
        <Drawer.Navigator
            initialRouteName='recipeSetting'
            drawerContent={(props) => <CustomSidebarMenu {...props} />}
            screenOptions={{
                drawerType: 'permanent',
                drawerActiveTintColor: "#49319E",
                drawerStyle: {
                    width: '16%',
                    height: '100%',
                    borderTopRightRadius: 25,
                },
                drawerItemStyle: {
                    borderRadius: 50,
                    width: '90%',
                    height: '20%',
                    marginBottom: '3.5%',
                },
            }}>
            <Drawer.Screen name="home"
                component={Home}
                options={{
                    drawerLabel: 'Home',
                    drawerLabelStyle: {
                        fontSize: 16,
                        width: '100%',
                        height: '100%',
                        fontWeight: "bold",
                        marginBottom: 0,
                    },
                    headerTitle: "crispy recipe",
                    headerStyle: {
                        backgroundColor: '#49319E',
                        height: 35,
                    },
                    headerTitleStyle: {
                        color: "#FFFF",
                        fontSize: 17,
                    },
                    headerTintColor: '#fff',
                    headerTitleAlign: 'center',
                    drawerIcon: ({ focused }) => (
                        <Image
                            source={
                                !focused ?
                                    require('../../public/images/homebtn.png') :
                                    require('../../public/images/puplehome.png')}
                            style={{ width: '12%', height: '55%', marginLeft: "7%", marginRight: "-12%" }}
                        />)
                }}
            />
            <Drawer.Screen
                name="recipeSetting"
                component={RecipeBox}
                options={{
                    drawerLabel: '레시피 설정',
                    drawerLabelStyle: {
                        fontSize: 16,
                        width: '100%',
                        height: '100%',
                        fontWeight: "bold",
                        marginBottom: 0,
                    },
                    headerTitle: "crispy recipe",
                    headerStyle: {
                        backgroundColor: '#49319E',
                        height: 35,
                    },
                    headerTitleStyle: {
                        color: "#FFFF",
                        fontSize: 17,
                    },
                    headerTintColor: '#fff',
                    headerTitleAlign: 'center',
                    drawerIcon: ({ focused }) => (
                        <Image
                            source={
                                !focused ?
                                    require('../../public/images/programbtn.png') :
                                    require('../../public/images/programbtnOff.png')}
                            style={{ width: '12%', height: '55%', marginLeft: "7%", marginRight: "-12%" }}
                        />)
                }} />
            <Drawer.Screen
                name="DryerManagement"
                component={Article}
                options={{
                    drawerLabel: '건조기 관리',
                    drawerLabelStyle: {
                        fontSize: 16,
                        width: '100%',
                        height: '100%',
                        fontWeight: "bold",
                        marginBottom: 0,
                    },
                    headerTitle: "crispy recipe",
                    headerStyle: {
                        backgroundColor: '#49319E',
                        height: 35,
                    },
                    headerTitleStyle: {
                        color: "#FFFF",
                        fontSize: 17,
                    },
                    headerTintColor: '#fff',
                    headerTitleAlign: 'center',
                    drawerIcon: ({ focused }) => (
                        <Image
                            source={
                                !focused ?
                                    require('../../public/images/drybtn.png') :
                                    require('../../public/images/drybtnOff.png')}
                            style={{ width: '12%', height: '55%', marginLeft: "7%", marginRight: "-12%" }}
                        />)
                }} />
            <Drawer.Screen
                name="dataManagement"
                component={Article}
                options={{
                    drawerLabel: '데이터 관리',
                    drawerLabelStyle: {
                        fontSize: 16,
                        width: '100%',
                        height: '100%',
                        fontWeight: "bold",
                        marginBottom: 0,
                    },
                    headerTitle: "crispy recipe",
                    headerStyle: {
                        backgroundColor: '#49319E',
                        height: 35,
                    },
                    headerTitleStyle: {
                        color: "#FFFF",
                        fontSize: 17,
                    },
                    headerTintColor: '#fff',
                    headerTitleAlign: 'center',
                    drawerIcon: ({ focused }) => (
                        <Image
                            source={
                                !focused ?
                                    require('../../public/images/chartbtn.png') :
                                    require('../../public/images/chartbtnOff.png')}
                            style={{ width: '12%', height: '55%', marginLeft: "7%", marginRight: "-12%" }}
                        />)
                }} />
        </Drawer.Navigator>
    );
}
export default MyDrawer;