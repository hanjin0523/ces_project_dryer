import React, { useMemo, useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";
import { useSelector } from "react-redux";
import { useTimeConversion } from "../customHook/useCustomHook";

interface propsTpye {
    setTemp: number;
}

const RecipeTitle = React.memo(() => {

    const setTemp = useSelector((state: any) => state.counter.setTemp)
    const setHum = useSelector((state: any) => state.counter.setHum)
    const setTime = useSelector((state: any) => state.counter.setTimeValue)
    const time = useTimeConversion(setTime)

    return(
        <View style={styles.titleMainBox}>
            <View style={{flexDirection:'row',height:'60%'}}>
                <Text style={styles.titleText}>Recipe Setting</Text>
                <Text style={styles.titleSubText}>레시피 설정</Text>
            </View>
            <View style={{flexDirection:'row', alignItems:'center', marginTop:'1.5%', marginRight: '10%', justifyContent:'center'}}>
                <View style={styles.setting}>
                    <Image style={styles.img} source={require('../../public/images/settingView/tempView.png')} resizeMode="contain"/>
                    <Text style={styles.settingNum}>{setTemp}℃</Text>
                </View>
                <View style={styles.setting}>
                    <Image style={styles.img} source={require('../../public/images/settingView/humView.png')} resizeMode="contain"/>
                    <Text style={styles.settingNum}>{setHum}%</Text>
                </View>
                <View style={styles.setting}>
                    <Image style={styles.img} source={require('../../public/images/settingView/timeView.png')} resizeMode="contain"/>
                    <Text style={[styles.settingNum, {width:110}]}>{setTime === '00:00' ? '00:00:00' : time }</Text>
                </View>
            </View>
        </View>
    );
})
const styles = StyleSheet.create({
    titleMainBox: {
        // borderWidth: 1,
        width: '100%',
        height: '21%',
        marginTop: '10%',
    },
    titleText: {
        color: colors.black,
        fontWeight: '700',
        fontSize: 31,      
    },
    titleSubText: {
        fontSize: 15,
        color: colors.black,
        marginLeft: '2.3%',
        marginTop: '2.6%'
    },
    settingNum: {
        fontSize: 27,
        color: colors.black,
        fontWeight: '700',
        marginLeft: '4%',
        width: 60,
    },
    img: {
        height: 50,
        width: 40,
    },
    setting: {
        // borderWidth:1,
        flexDirection: 'row',
        marginRight: '0%',
        width:110
    }
})
export default RecipeTitle;
