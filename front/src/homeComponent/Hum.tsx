import React from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";

interface propsTpye {
    hum: number
}

const Hum = (props: propsTpye) => {

    const humText = props.hum === 100 ? null : `${props.hum}%`;

    const getHumImage = () => {
        if (props.hum >= 0 || props.hum === undefined) {
            return require("../../public/images/hum/hum10.png");
        } else if (props.hum >= 11 && props.hum < 36) {
            return require("../../public/images/hum/hum35.png");
        } else if (props.hum >= 36 && props.hum < 51) {
            return require("../../public/images/hum/hum50.png");
        } else if (props.hum >= 51 && props.hum < 76) {
            return require("../../public/images/hum/hum75.png");
        } else if (props.hum >= 76 && props.hum < 81) {
            return require("../../public/images/hum/hum80.png");
        } else if (props.hum >= 81 && props.hum < 100) {
            return require("../../public/images/hum/hum90.png");
        } else if (props.hum === 100) {
            return require("../../public/images/hum/humError.png");
        } else {
            return null;
        }
    };

    return (
        <View style={styles.mainTemp}>
            <View style={styles.textBox}>
                <Text style={styles.mainText}>Humidity</Text>
                <Text style={styles.subText}>습도</Text>
            </View>
            <Text style={styles.tempText}>
                {props.hum === 0 || props.hum === undefined ? "측정중.." : humText}
            </Text>
            <Image
                style={styles.tempImg}
                source={getHumImage()}
                resizeMode="cover"
            />
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
        zIndex:1,
        marginTop: "47%",
        fontSize: 25,
        color: colors.black,
        fontWeight: "700"
    }
})
export default Hum;