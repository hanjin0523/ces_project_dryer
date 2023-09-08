import React, { useEffect, useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";
import { useDispatch, useSelector } from "react-redux";
import { heatRayOper, decrement } from "../reduxT/slice";
import { TouchableOpacity } from "react-native-gesture-handler";
import * as config from '../config';

const OperationButton = () => {
    const dispatch = useDispatch()
    const server_ip = config.SERVER_URL;
    const [startDryingBtn, setStartDryingBtn] = useState<boolean>(false);
    const [startButton, setStartButton] = useState<boolean>(false);
    const heatRay = useSelector((state: any) => state.counter.heatRay)
    const blowing = useSelector((state: any) => state.counter.blowing)
    const setTime = useSelector((state: any) => state.counter.setTime)
    const operTime = useSelector((state: any) => state.counter.operTime)
    const dryer_number = useSelector((state:any) => state.counter.dryerNumber)
    const status = useSelector((state:any) => state.counter.status)

    // useEffect(() => {
    //     if(startButton === true){
    //         setStartButton(false);
    //     }
    //     if(startDryingBtn === true){
    //         setStartDryingBtn(false);
    //     }
    // },[dryer_number])

    // useEffect(() => {
    //     if(operTime === 0){
    //         setStartDryingBtn(false)
    //     }
    // },[operTime])

    useEffect(() => {
        const on_arr = ['h1_on', 'h2_on', 'h3_on']
        const off_arr = ['h1_off', 'h2_off', 'h3_off']
        if (startDryingBtn) {
            fetch(`http://${server_ip}/power`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    arr: on_arr,
                    time: operTime,

                })
            })
            .then((response) => response.json())
            .then((data) => {
                console.log(data)
                // setTimeout(() => {
                //     setStartDryingBtn(false)
                // }, data*1000);
            })
        }
        else{
            fetch(`http://${server_ip}/stop`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    arr: off_arr
                })
            })
            // checkPowerStatus();
        }
    }, [startDryingBtn]);

    useEffect(() => {
        const on_arr = ['fan1_on', 'fan2_on']
        const off_arr = ['fan1_off', 'fan2_off']
        fetch(`http://${server_ip}/deodorization_operation`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                arr: blowing ? on_arr : off_arr
            })
        })
    }, [blowing]);

    const on_off = () => {
        setStartDryingBtn((prev) => !prev);
        // dispatch(heatRayOper(startDryingBtn))
    };

    const on_off1 = () => {
        setStartButton((prev) => !prev);
        // dispatch(decrement(!startButton))
    };

    return (
        <View style={styles.buttonBox}>
            {/* <TouchableOpacity onPress={()=>{on_off(); dispatch(heatRayOper(!startDryingBtn))}} style={styles.startDryingBtn}> */}
            <TouchableOpacity onPress={()=>{on_off(); }} style={styles.startDryingBtn}>
                {status ? <Image style={styles.stopBtn} source={require('../../public/images/stop.png')} resizeMode="contain" /> :
                    <Text style={styles.buttonText}>건조시작</Text>}
            </TouchableOpacity>
            <TouchableOpacity onPress={()=>{on_off1();}} style={styles.startButton}>
                <Text style={styles.buttonText1}>
                    {!blowing ? "송풍(탈취) 정지" : "송풍(탈취) 가동"}
                </Text>
            </TouchableOpacity>
        </View>
    );
}
const styles = StyleSheet.create({
    buttonBox: {
        height: '18%',
        width: '100%',
        alignItems: 'center',
    },
    startDryingBtn: {
        borderWidth: 2,
        borderColor: '#753CEF',
        height: 50,
        width: 350,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
        backgroundColor: '#753CEF'
    },
    startButton: {
        borderColor: '#B5B3B9',
        borderWidth: 2,
        height: 50,
        width: 350,
        marginTop: '2%',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 5,
    },
    buttonText: {
        fontSize: 17,
        color: '#ffffff',
        fontWeight: '700'
    },
    buttonText1: {
        fontSize: 17,
        color: '#B5B3B9',
        fontWeight: '700'
    },
    stopBtn: {
        height: 33,
    }
})
export default OperationButton;