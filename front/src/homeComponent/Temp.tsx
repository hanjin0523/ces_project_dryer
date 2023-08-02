import React, { useState, useEffect } from "react";
import colors from "../../public/colors/colors";
import * as config from '../config';
import { Image, StyleSheet, Text, View } from "react-native";

interface propsTpye {
    temp: number
}

const Temp = (props: propsTpye) => {
    const tempText = props.temp >= 80 ? null : `${props.temp}℃`

    return (
        <View style={styles.mainTemp}>
            <View style={styles.textBox}>
                <Text style={styles.mainText}>Temperature</Text>
                <Text style={styles.subText}> 온도</Text>
            </View>
            <Text style={styles.tempText}>{props.temp === 0 || props.temp === undefined ? '측정중..' : tempText}</Text>
            {props.temp ?
                <Image
                    style={styles.tempImg}
                    source={props.temp <= 20 ? require('../../public/images/temp/temp20.png') :
                        props.temp >= 21 && props.temp < 31 ? require('../../public/images/temp/temp30.png') :
                            props.temp >= 31 && props.temp < 41 ? require('../../public/images/temp/temp40.png') :
                                props.temp >= 41 && props.temp < 51 ? require('../../public/images/temp/temp50.png') :
                                    props.temp >= 51 && props.temp < 61 ? require('../../public/images/temp/temp60.png') :
                                        props.temp >= 61 && props.temp < 71 ? require('../../public/images/temp/temp70.png') :
                                            props.temp >= 71 && props.temp < 80 ? require('../../public/images/temp/temp80.png') :
                                                props.temp >= 80 ? require('../../public/images/temp/temperror.png') : null}
                    resizeMode="cover"
                /> : <Image style={styles.tempImg} source={require('../../public/images/temp/temp20.png')} />}
        </View>
    );
}
const styles = StyleSheet.create({
    mainTemp: {
        height: "100%",
        width: "37%",
        alignItems: 'center'
    },
    textBox: {
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: 0
    },
    mainText: {
        color: colors.black,
        fontWeight: "800",
        fontSize: 18,
    },
    tempImg: {
        marginTop: '2.5%',
        height: '78.5%',
        width: '77%',
    },
    subText: {
        fontSize: 13,
        color: colors.black,
        fontWeight: '500'
    },
    tempText: {
        position: "absolute",
        marginTop: "47%",
        fontSize: 25,
        color: colors.black,
        fontWeight: "700"
    }
})
export default Temp;