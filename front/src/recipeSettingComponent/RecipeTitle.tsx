import React, { useMemo, useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";
import { useSelector } from "react-redux";

interface propsTpye {
    setTemp: number;
}

const RecipeTitle = React.memo(() => {
    const setTemp = useSelector((state: any) => state.counter.setTemp)
    const setHum = useSelector((state: any) => state.counter.setHum)
    const setTime = useSelector((state: any) => state.counter.setTimeValue)

    const timeConversion = (seconds: number) => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        return `${hours}: ${minutes}: ${second}`;
    }

    return(
        <View style={styles.titleMainBox}>
            <View style={{flexDirection:'row',height:'60%'}}>
                <Text style={styles.titleText}>Recipe Setting</Text>
                <Text style={styles.titleSubText}>레시피 설정</Text>
            </View>
            <View style={{flexDirection:'row', alignItems:'center', marginTop:'1.5%', justifyContent:'center'}}>
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
                    <Text style={styles.settingNum}>{setTime === '00:00' ? '00:00:00' : timeConversion(setTime)}</Text>
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
        marginLeft: '4%'
    },
    img: {
        height: 50,
        width: 40,
    },
    setting: {
        flexDirection: 'row',
        marginRight: '2%'
    }
})
export default RecipeTitle;
