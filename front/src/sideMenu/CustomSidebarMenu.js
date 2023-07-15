import React, { useState } from 'react';
import {
    SafeAreaView,
    View,
    StyleSheet,
    Image,
    Text,
    Dimensions
} from 'react-native';

import {
    DrawerContentScrollView,
    DrawerItemList,
    DrawerItem,
} from '@react-navigation/drawer';

const height = Dimensions.get('window').height;
const width = Dimensions.get('window').width;

const CustomSidebarMenu = (props) => {
    const BASE_PATH ='../../public/images/';
    const proileImage = 'operationbtn.png';
    const [dryOnOff, setDryOnOff] = useState(1);/////건조기 가동여부임!!!!첫번째 graphite값

    return (
    <SafeAreaView style={{ flex: 1 }}>
        <View style={styles.sideMenuBox}>
            <Text style={styles.sideMainText}>Crispy<Text style={{fontWeight:"normal", color: "black"}}> recipe</Text></Text>
            <Image
            source={dryOnOff ? require(BASE_PATH+'operationbtn.png') : require(BASE_PATH+'waitingbtn.png')}
            style={styles.sideMenuProfileIcon}
            />
        </View>
        <DrawerContentScrollView {...props} style={{ marginLeft:"5%",height:height/20.3720, width:width/6.8651 }}>
        <DrawerItemList {...props}/>
        </DrawerContentScrollView>
        <View style={{flexDirection:"row", marginBottom:height/65, marginLeft:width/53,alignContent:"center"}}>
        <Image source={require('../../public/images/Profilebtn.png')}/>
        <Text style={{ fontSize: 13, textAlign: 'center', color: 'grey', marginTop:height/50, marginLeft:width/140}}>
        영농조합법인페페
        </Text>
        </View>
    </SafeAreaView>
    );

};

const styles = StyleSheet.create({
    sideMenuBox: {
        alignItems: "flex-end", 
        flexDirection: "row", 
        marginLeft: width / 77.68421,
        marginTop: height / 12.0383,
        marginBottom: height / 60.375,
    },
    sideMainText: {
        fontSize: 21,
        fontWeight: "bold",
        color: "black",
    },
    sideMenuProfileIcon: {
        resizeMode: 'center',
        width: width / 33.3333,
        height: height / 50.5294,
        marginLeft: width / 175,
        marginBottom: height / 220
    },
});

export default CustomSidebarMenu;