import React from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import colors from '../../public/colors/colors';

interface propsTpye {
    operation: number;
}

const Progress = (props:propsTpye) => {

    const operationImages: { [key: number]: any} = {
        0: require('../../public/images/operation/rest.png'),
        10: require('../../public/images/operation/operation10.png'),
        35: require('../../public/images/operation/operation35.png'),
        50: require('../../public/images/operation/operation50.png'),
        75: require('../../public/images/operation/operation75.png'),
        80: require('../../public/images/operation/operation80.png'),
        90: require('../../public/images/operation/operation90.png'),
        100: require('../../public/images/operation/operation100.png'),
    };
    
    const operText = props.operation === 0 || props.operation === 100 ? null : `${props.operation}%`;


    return(
        <View style={styles.progressBox}>
            <Text style={styles.operText}>{operText}</Text>
            <Image
                style={styles.operation}
                source={operationImages[props.operation] || null}
                resizeMode='cover'
            />
        </View>
    );
}
const styles = StyleSheet.create({
    progressBox: {
        height: '45%',
        justifyContent:'center',
        alignItems: 'center'
    },
    operation: {
        height: '95.5%',
        width: '62%',
        marginTop: '18%',
    },
    operText: {
        position: 'absolute',
        marginTop: '0%',
        fontWeight: '900',
        height: '70%',
        fontSize: 55,
        lineHeight: 260,
        textAlign: 'center',
        color: colors.black
    }


})
export default Progress;