import React, { useState, useEffect } from 'react';
import { Alert, StyleSheet, Text, View } from 'react-native';
import * as config from '../config';
import { useSelector, useDispatch } from 'react-redux';
import Title from './Title';
import Progress from './Progress';
import Temp from './Temp';
import Hum from './Hum';
import Time from '../homeSecond/Time';
import Menu from '../homeSecond/Menu';
import { selectDryer } from '../reduxT/slice';

const Home = () => {
    const dispatch = useDispatch()
    const server_ip = config.SERVER_URL;
    const [temp, setTemp] = useState<number>(0);
    const [hum, setHum] = useState<number>(0);
    const dryer_num = useSelector((state: any) => state.counter.dryerNumber)
    const [isAlertShown, setAlertShown] = useState(false);

    const fetchData = () => {
        fetch(`http://${server_ip}/dry_status?select_num=${dryer_num}`)
            .then((response) => response.json())
            .then((data) => {
                if(data.message) {
                    if(!isAlertShown) {
                        Alert.alert("연결되지 않은 건조기입니다. 확인해주세요.")
                        setAlertShown(true);
                    }
                }
                else {
                setTemp(data[0]);
                setHum(data[1]);
                }
            })
            .catch((error) => {
                console.log("서버연결을해주세요");
                // dispatch(selectDryer(0));
            });
    }
    
    useEffect(() => {
            fetchData();
            const intervalId = setInterval(fetchData, 5000);
            return () => {
                clearInterval(intervalId);
        }
    }, [dryer_num]);

    return (
        <View style={styles.homeMain}>
            <View style={styles.homeInner}>
                <View style={styles.firstInner}>
                    <Title />
                    <Progress />
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
Home.defaultProps = {
    temp: 0,
    hum: 0,
};
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