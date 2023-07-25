import React, { useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import Title from './Title';
import Progress from './Progress';
import Temp from './Temp';
import Hum from './Hum';
import Time from '../homeSecond/Time';
import Menu from '../homeSecond/Menu';

const Home = () => {

    const [operRays, setOperRays] = useState<boolean>(true);
    const [temp, setTemp] = useState<number>(50);
    const [hum, setHum] = useState<number>(90);

    return (
        <View style={styles.homeMain}>
            <View style={styles.homeInner}>
                <View style={styles.firstInner}>
                    <Title status={operRays} />
                    <Progress operation={10} />
                    <View style={styles.tempHumBox}>
                        <Temp temp={temp} />
                        <Hum hum={hum} />
                    </View>
                </View>
                <View style={styles.seceondInner}>
                    <Time />
                    <Menu />
                </View>
            </View>
        </View>
    );
}
const styles = StyleSheet.create({
    homeMain: {
        height: '100%',
        width: '100%',
        backgroundColor: '#EFEAFF',
        alignItems: 'center',
        justifyContent: 'center',
    },
    homeInner: {
        width: '95%',
        height: '90%',
        flexDirection: 'row'
    },
    firstInner: {
        height: '100%',
        width: '40%',
        backgroundColor: '#FFFFFF',
        marginRight: "3%",
        borderRadius: 25,
        paddingTop: '3.5%',
        // paddingLeft: '2.5%',
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 3,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 10,
    },
    seceondInner: {
        height: '100%',
        width: '57%',
        backgroundColor: '#FFFFFF',
        borderRadius: 25,
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 3,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 10,
        alignItems: 'center'
    },
    tempHumBox: {
        height: "25%",
        width: "100%",
        marginTop: "15%",
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center'
    }
})
export default Home;