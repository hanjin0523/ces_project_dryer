import React, { useState } from "react";
import colors from '../../public/colors/colors';
import * as config from '../config';
import { View, Text, StyleSheet, Image } from "react-native";
import SecondBox from "./SecondBox";

const ManagementHome = () => {
    
    

    return(
        <View style={style.mainBox}>
            <View style={style.innerBox}>
                <View style={style.firstBox}>
                    <View style={style.titleTextBox}>
                        <Text style={style.titleText}>Dry management</Text>
                        <Text style={style.subText}>건조기 관리</Text>
                    </View>
                    <View style={style.imgBox}>
                        <Image style={{height:'85%', width:'90%'}} source={require('../../public/images/dryer.png')} resizeMode="contain"/>
                    </View>
                </View>
                <View style={style.secondBox}>
                    <SecondBox />
                </View>
            </View>
        </View>
    );
}
const style = StyleSheet.create({
    mainBox: {
        height: '100%',
        width: '100%',
        backgroundColor: '#EFEAFF',
        alignItems: 'center',
        justifyContent: 'center',
    },
    innerBox: {
        // borderWidth: 1, 
        width: '93%',
        height: '90%',
        flexDirection: 'row'
    },
    firstBox: {
        // borderWidth: 1,
        width: '50%'
    },
    titleTextBox: {
        // borderWidth: 1, 
        height: '10%',
        marginTop: '9%',
        flexDirection: 'row',
        alignItems: 'center'
    },
    titleText: {
        color: colors.black,
        fontWeight: '700',
        fontSize: 27,
        marginRight: '2.5%'
    },
    subText: {
        color: colors.black, 
        fontSize: 15,
        textAlign: 'center'
    },
    imgBox: {
        // borderWidth: 1, 
        height: '83%',
        alignItems: 'center',
        justifyContent: 'center'
    },
    secondBox: {
        // borderWidth: 1, 
        width: '50%',
        alignItems: 'center',
        justifyContent: 'center'
    }
})
export default ManagementHome;