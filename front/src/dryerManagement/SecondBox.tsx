import React, { useState } from "react";
import colors from '../../public/colors/colors';
import * as config from '../config';
import { StyleSheet, View, Text, TouchableOpacity } from "react-native";

const SecondBox = () => {



    return (
        <View style={styles.mainBox}>
            <TouchableOpacity style={{width:100, height: 100, backgroundColor:'grey'}} onPress={()=>console.log("11")}>
                <Text style={{fontSize:20}}>
                    1번건조기
                </Text>
            </TouchableOpacity>
            <TouchableOpacity style={{width:100, height: 100, backgroundColor:'green'}}>
                <Text style={{fontSize:20}}>
                    2번건조기
                </Text>
            </TouchableOpacity>
        </View>
    );
}
const styles = StyleSheet.create({
    mainBox: {
        backgroundColor: '#FFFFFF',
        height: '100%',
        width: '100%',
        borderRadius: 20
    }
})
export default SecondBox;