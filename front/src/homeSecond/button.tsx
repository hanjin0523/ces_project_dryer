import React, { useEffect, useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";
import * as config from '../config';

const OperationButton = () => {
    const server_ip = config.SERVER_URL;
    const [startDryingBtn, setStartDryingBtn] = useState<boolean>(false);
    const [startButton, setStartButton] = useState<boolean>(false);
    const [powerHandlerStopped, setPowerHandlerStopped] = useState<boolean>(false);

    const checkPowerStatus = async () => {
        try {
            const response = await fetch(`http://${server_ip}/power/status`);
            const data = await response.json();
            setPowerHandlerStopped(data.power_handler_stopped);
            // Update your front-end UI based on the powerHandlerStopped value
            // For example, show a "Start" button if powerHandlerStopped is true, and a "Stop" button if it's false.
        } catch (error) {
            console.error('Error fetching power status:', error);
        }
    };

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
                    arr: on_arr
                })
            })
            checkPowerStatus();
        }
        else {
            fetch(`http://${server_ip}/stop`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    arr: off_arr
                })
            })
            checkPowerStatus();
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
                arr: startButton ? on_arr : off_arr
            })
        })
    }, [startButton]);

    const on_off = () => {
        setStartDryingBtn((prev) => !prev);
    };

    const on_off1 = () => {
        setStartButton((prev) => !prev);
    };

    return (
        <View style={styles.buttonBox}>
            <TouchableOpacity onPress={on_off} style={styles.startDryingBtn}>
                {startDryingBtn ? <Image style={styles.stopBtn} source={require('../../public/images/stop.png')} resizeMode="contain" /> :
                    <Text style={styles.buttonText}>건조시작</Text>}
            </TouchableOpacity>
            <TouchableOpacity onPress={on_off1} style={styles.startButton}>
                <Text style={styles.buttonText1}>
                    {startButton ? "송풍(탈취) 정지" : "송풍(탈취) 가동"}
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