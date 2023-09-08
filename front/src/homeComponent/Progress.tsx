import React, { useEffect, useState } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import colors from '../../public/colors/colors';
import { useDispatch, useSelector } from 'react-redux';
import { initTimeValue, operationStartTimer, heatRayOper, decrement, settingStatus } from "../reduxT/slice";
import * as config from '../config';

interface propsTpye {
    operation: number;
}

const Progress = React.memo(() => {
    const server_ip = config.SERVER_URL;
    const dispatch = useDispatch()
    const [percentage, setPercentage] = useState<number>(0);
    const [timer, setTimer] = useState<number>(0);
    const dryer_number = useSelector((state:any) => state.counter.dryerNumber)
    
    useEffect(() => {
        const socket = new WebSocket(`ws://${server_ip}/ws/${dryer_number}`)
        socket.onopen = () => {console.log("websocket..connected..")}
        socket.onmessage = (event:any) => {
            const value = JSON.parse(event.data);
            const roundedTime = value[0];
            const setTime = value[1];
            const heat_ray = value[2];
            const blower = value[3];
            const status = value[4];
            setPercentage(roundedTime);
            setTimer(setTime);
            dispatch(heatRayOper(heat_ray))
            dispatch(decrement(blower))
            dispatch(settingStatus(status))
            console.log(value,"건조기변경각!?")
        }
        socket.onclose = () => {
            dispatch(heatRayOper(false))
            dispatch(decrement(false))
            dispatch(settingStatus(false))
            setPercentage(0)
            setTimer(0)
            socket.close();
        }
    },[dryer_number])


    const timeConversion = (seconds: number) => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        return `${hours}시간 ${minutes}분 ${second}초`;
    }

    const operText = percentage >= 95 ? null : `${percentage}%`;
    {/*숫자95는 시간완료퍼센테이지입니다. */}

    return (
        <View style={styles.progressBox}>
            <Text style={styles.operTime}>{timer !== 0 ? `${timeConversion(timer-1)}남음` : ''}</Text>
            <Text style={styles.operText}>{operText}</Text>
            <Image
                style={styles.operation}
                source={percentage <= 10 ? require('../../public/images/operation/operation10.png') : 
                percentage >= 10 && percentage < 36 ? require('../../public/images/operation/operation35.png') :
                percentage >= 36 && percentage < 51 ? require('../../public/images/operation/operation50.png') :
                percentage >= 51 && percentage < 76 ? require('../../public/images/operation/operation75.png') :
                percentage >= 76 && percentage < 81 ? require('../../public/images/operation/operation80.png') : 
                percentage >= 81 && percentage < 95 ? require('../../public/images/operation/operation90.png') :
                percentage >= 95 ? require('../../public/images/operation/operation100.png') :
                        null}
                resizeMode='cover'
            />
        </View>
    );
})
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