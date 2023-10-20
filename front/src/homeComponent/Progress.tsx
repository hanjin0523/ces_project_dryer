import React, { useEffect, useMemo, useState } from 'react';
import { Image, StyleSheet, Text, View, AppState } from 'react-native';
import colors from '../../public/colors/colors';
import { useDispatch, useSelector } from 'react-redux';
import { heatRayOper, decrement, dehumidifierControl, settingStatus } from "../reduxT/slice";
import * as config from '../config';
import { useTimeConversion_ko } from '../customHook/useCustomHook';

const Progress = () => {
    const [appState, setAppState] = useState(AppState.currentState);
    const server_ip = config.SERVER_URL;
    const dispatch = useDispatch()
    const [percentage, setPercentage] = useState<number>(0);
    const [timer, setTimer] = useState<number>(0);
    const dryer_number = useSelector((state: any) => state.counter.dryerNumber);
    const time = useTimeConversion_ko(timer);
    const time1 = useSelector((state: any) => state.counter.setTime);

    useEffect(() => {
        setTimer(0)
    }, [time1])

    useEffect(() => {
        const handleAppStateChange = (nextAppState: any) => {
            setAppState(nextAppState);
            console.log('App state changed to', nextAppState);
        };
        AppState.addEventListener('change', handleAppStateChange);
    }, []);

    const [websocket, setWebsocket] = useState<any>(null);
    useEffect(() => {
            const socket = new WebSocket(`ws://${server_ip}/ws/${dryer_number}`)
            setWebsocket(socket)
            console.log(websocket)
            socket.onopen = () => { console.log("websocket..connected..") }
            socket.onmessage = (event: any) => {
                const value = JSON.parse(event.data);
                const roundedTime = value[0];
                const setTime = value[1];
                const heat_ray = value[2];
                const blower = value[3];
                const dehumidifier = value[4];
                const status = value[5];
                setPercentage(roundedTime);
                setTimer(setTime);
                dispatch(heatRayOper(heat_ray))
                dispatch(decrement(blower))
                dispatch(dehumidifierControl(dehumidifier))
                dispatch(settingStatus(status))
            }
            socket.onclose = () => {
                dispatch(heatRayOper(false))
                dispatch(decrement(false))
                dispatch(dehumidifierControl(false))
                dispatch(settingStatus(false))
                setPercentage(0)
                setTimer(0)
                socket.send('WebSocketDisconnect');
            }
            return () => {
                socket.close()
                setWebsocket(null)
                console.log("클라웹소켓종료")
            }
    }, [dryer_number, appState])

    const getOperationImage = (percentage: number) => {
        if (percentage <= 10) {
            return require('../../public/images/operation/operation10.png');
        } else if (percentage >= 10 && percentage < 36) {
            return require('../../public/images/operation/operation35.png');
        } else if (percentage >= 36 && percentage < 51) {
            return require('../../public/images/operation/operation50.png');
        } else if (percentage >= 51 && percentage < 76) {
            return require('../../public/images/operation/operation75.png');
        } else if (percentage >= 76 && percentage < 81) {
            return require('../../public/images/operation/operation80.png');
        } else if (percentage >= 81 && percentage < 95) {
            return require('../../public/images/operation/operation90.png');
        } else if (percentage >= 95) {
            return require('../../public/images/operation/operation100.png');
        } else {
            return null;
        }
    };

    const operText = percentage >= 95 ? null : `${percentage}%`;
    {/*숫자95는 시간완료퍼센테이지입니다. */ }

    return (
        <View style={styles.progressBox}>
            <Text style={styles.operTime}>{timer !== 0 ? `${time}남음` : ''}</Text>
            <Text style={styles.operText}>{operText}</Text>
            <Image
                style={styles.operation}
                source={getOperationImage(percentage)}
                resizeMode='cover'
            />
        </View>
    );
};
const styles = StyleSheet.create({
    progressBox: {
        height: '45%',
        justifyContent: 'center',
        alignItems: 'center'
    },
    operation: {
        height: '95.5%',
        width: '62%',
        marginTop: '18%',
    },
    operTime: {
        color: colors.black,
        position: 'absolute'
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