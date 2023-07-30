import React, { useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";

const RecipeTitle = () => {
    
    const [setTemp, setSetTemp] = useState<number>(50)
    const [setHum, setSetHum] = useState<number>(10)
    const [setTime, setSetTime] = useState<number>(80)

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
                    <Text style={styles.settingNum}>{setTime}</Text>
                </View>
            </View>
        </View>
    );
}
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
