import React, { useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, TouchableOpacity, View } from "react-native";

interface propsType {
    fn: (key: string) => void;
}

const RecipeButton = (props: propsType) => {
    
    const [seletItem, setSelectItem] = useState<string>('')

    const handlePress = (key: string) => {
        props.fn(key);
        setSelectItem(key)
    };

    return(
        <View style={styles.btnMainBox}>
            <View style={styles.innerBox}>
                <TouchableOpacity onPress={()=>handlePress('temp')} style={{width:'28%', height:'100%'}} key={'temp'}>
                    <Image style={styles.btnImg} source={seletItem === 'temp' ? require('../../public/images/settingView/tempBtnOn.png') : require('../../public/images/settingView/tempBtnOff.png')} resizeMode="contain"/>
                </TouchableOpacity >
                <TouchableOpacity onPress={()=>handlePress('hum')} style={{width:'28%',height:'100%'}} key={'hum'}>
                    <Image style={styles.btnImg} source={seletItem === 'hum' ? require('../../public/images/settingView/humBtnOn.png') : require('../../public/images/settingView/humBtnOff.png')} resizeMode="contain"/>
                </TouchableOpacity>
                <TouchableOpacity onPress={()=>handlePress('time')} style={{width:'28%', height:'100%'}} key={'time'}>
                    <Image style={styles.btnImg} source={seletItem === 'time' ? require('../../public/images/settingView/timeBtnOn.png') : require('../../public/images/settingView/timeBtnOff.png')} resizeMode="contain"/>
                </TouchableOpacity >
            </View>
        </View>
    );
}
const styles = StyleSheet.create({
    btnMainBox: {
        // borderWidth: 1,
        height: "21%",
        width: "100%",
        justifyContent: 'center',
        alignItems: 'center'
    },
    innerBox: {
        // borderWidth: 1,
        height: "60%",
        width: "60%",
        justifyContent: 'center',
        flexDirection: 'row'
    },
    btnImg: {
        width: '100%',
        height: '100%'
    }
})
export default RecipeButton;