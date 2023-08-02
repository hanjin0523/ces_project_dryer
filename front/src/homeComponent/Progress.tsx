import React, { useEffect, useState } from 'react';
import { Image, StyleSheet, Text, View } from 'react-native';
import colors from '../../public/colors/colors';
import { useDispatch, useSelector } from 'react-redux';
import { initTime, operationStartTimer, heatRayOper } from "../reduxT/slice";

interface propsTpye {
    operation: number;
}

const Progress = React.memo(() => {
    const dispatch = useDispatch()
    const setTime = useSelector((state: any) => state.counter.setTime)
    const operTime = useSelector((state: any) => state.counter.operTime)
    const heatRay = useSelector((state: any) => state.counter.heatRay)
    const [progress, setProgress] = useState<number>(0);
    const time =(((setTime - operTime+1) / setTime) * 100).toFixed(1)
    useEffect(() => {
        if (heatRay === true && operTime > 0) {
            const intervalId = setInterval(() => {
                dispatch(operationStartTimer());
                setProgress(Number(time))
            }, 1000);
            return () => {
                clearInterval(intervalId);
            };
        } else if (operTime === 0) {
            dispatch(heatRayOper())
            dispatch(initTime())
        } else if (operTime === 'null'){
            setProgress(0)
        }
    }, [heatRay, operTime]);

    const timeConversion = (seconds: number) => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        return `${hours}시간 ${minutes}분 ${second}초`;
    }

    const operText = progress === 100 ? null : `${progress}%`;
    

    return (
        <View style={styles.progressBox}>
            <Text style={styles.operTime}>{setTime !== '' ? `${timeConversion(operTime)}남음` : ''}</Text>
            <Text style={styles.operText}>{operText}</Text>
            <Image
                style={styles.operation}
                source={progress <= 10 ? require('../../public/images/operation/operation10.png') : 
                        progress >= 10 && progress < 36 ? require('../../public/images/operation/operation35.png') :
                        progress >= 36 && progress < 51 ? require('../../public/images/operation/operation50.png') :
                        progress >= 51 && progress < 76 ? require('../../public/images/operation/operation75.png') :
                        progress >= 76 && progress < 81 ? require('../../public/images/operation/operation80.png') : 
                        progress >= 81 && progress < 100 ? require('../../public/images/operation/operation90.png') :
                        progress === 100 ? require('../../public/images/operation/operation100.png') :
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