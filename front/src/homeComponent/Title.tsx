import React from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import colors from '../../public/colors/colors';
import { useSelector } from 'react-redux';

const Title = () => {

    const heatRay = useSelector((state: any) => state.counter.heatRay);
    const dehumidifier = useSelector((state: any) => state.counter.dehumidifier);
    const blowing = useSelector((state: any) => state.counter.blowing);
    
    const getSituationImage = (isOn: boolean) => {
        return isOn ? require('../../public/images/On.png') : require('../../public/images/Off.png');
    };

    return (
        <View style={styles.titleBox}>
            <View style={styles.textBox}>
                <Text style={styles.text}>Recipe Progress</Text>
                <Text style={styles.textSub}>현재 건조기 상태</Text>
            </View>
            <View style={styles.situation}>
                <Text style={styles.situationText}>열선</Text>
                <Image style={styles.Img} source={getSituationImage(heatRay)} resizeMode='contain'/>
                <Text style={styles.situationText}>송풍</Text>
                <Image style={styles.Img} source={getSituationImage(dehumidifier)} resizeMode='contain'/>
                <Text style={styles.situationText}>배습</Text>
                <Image style={styles.Img} source={getSituationImage(blowing)} resizeMode='contain'/>
            </View>
        </View>
    );
}
const styles = StyleSheet.create({
    titleBox: {
        width: '100%',
        height: '14%',
        justifyContent: 'center',
        alignItems: 'center',
    },
    textBox: {
        width:'100%',
        flexDirection: 'row',
        justifyContent: 'center',
        alignItems: 'center',
    },
    text: {
        fontSize: 26,
        fontWeight: '700',
        color: colors.black,
        marginRight: "5%",
    },
    textSub: {
        fontSize: 15,
        color: colors.black,
        fontWeight: '500',
        lineHeight: 85,
    },
    situation: {
        height: "43%",
        width: "60%",
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: '-5%'
    },
    Img: {
        height: "50%",
        width: "16%",
        marginRight: "4%",
    },
    situationText: {
        color: colors.black,
        fontWeight: '400',
    }
})
export default Title;