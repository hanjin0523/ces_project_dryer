import React, { useEffect, useState } from "react";
import { Alert, Image, StyleSheet, Text, View } from "react-native";
import { useDispatch, useSelector } from "react-redux";
import { TouchableOpacity } from "react-native-gesture-handler";
import * as config from '../config';
import { SwipeListView } from 'react-native-swipe-list-view';
import { settingStatus, heatRayOper } from '../reduxT/slice'

const OperationButton = () => {
    const dispatch = useDispatch()
    const server_ip = config.SERVER_URL;
    const [startDryingBtn, setStartDryingBtn] = useState<boolean>(false);
    const operTime = useSelector((state: any) => state.counter.operTime)
    const dryer_number = useSelector((state: any) => state.counter.dryerNumber)
    const status = useSelector((state: any) => state.counter.status)
    const [mainBotton, setMainBotton] = useState<boolean>(false);

    useEffect(() => {
        if (!status) {
            fetch(`http://${server_ip}/power`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    time: operTime,
                })
            })
                .then((response) => response.json())
                .then((data) => {
                    console.log(data)
                })
        }
    }, [startDryingBtn]);
    
    const dryer_pause = () => { 
        fetch(`http://${server_ip}/pause`, {
    }).then(()=>{setStartDryingBtn(true)})}

    const dryer_stop = () => { 
        fetch(`http://${server_ip}/stop`, {
    }).then(()=>{setMainBotton(true)})}

    const on_off = () => {
        setStartDryingBtn((prev) => !prev);

    };

    const LIST_VIEW_DATA = Array(1)
        .fill('')
        .map((_, i) => ({ key: `${i}`, text: `item #${i}` }));
    return (
        <View style={styles.buttonBox}>
            {/* <TouchableOpacity onPress={()=>{on_off(); dispatch(heatRayOper(!startDryingBtn))}} style={styles.startDryingBtn}> */}
            <TouchableOpacity onPress={() => { on_off(); }} style={styles.startDryingBtn}>
                {status ?
                    <SwipeListView
                        data={LIST_VIEW_DATA}
                        renderItem={(data, rowMap) => (
                            <Image style={styles.stopBtn} source={require('../../public/images/stop.png')} resizeMode="contain" />
                        )}
                        renderHiddenItem={(data, rowMap) => (
                            <View style={styles.swipeHiddenItemContainer}>
                                <TouchableOpacity
                                    onPress={() => dryer_pause()}> 
                                    {/* onPress={() => dispatch(settingStatus(false))}>아직 미완성 상태 최선임펌웨어 받고 작업하자 서버엔드포인트따고 정지패킷날려야해*/}
                                    <View style={[styles.swipeHiddenItem, { backgroundColor: 'pink' }]}>
                                        <Text style={styles.swipeHiddenItemText}>일시정지</Text>
                                    </View>
                                </TouchableOpacity>
                                <TouchableOpacity
                                    onPress={() => dryer_stop()}>
                                    <View
                                        style={[styles.swipeHiddenItem, { backgroundColor: 'skyblue' }]}>
                                        <Text style={styles.swipeHiddenItemText}>완전정지</Text>
                                    </View>
                                </TouchableOpacity>
                            </View>
                        )}
                        leftOpenValue={70}
                        rightOpenValue={-70}
                    />
                    // <Image style={styles.stopBtn} source={require('../../public/images/stop.png')} resizeMode="contain" />
                    : status ? <Text style={styles.buttonText}>시작</Text> : <Text style={styles.buttonText}>건조시작</Text>
                }
            </TouchableOpacity>
            {/* <TouchableOpacity onPress={() => { on_off1(); }} style={styles.startButton}>
                <Text style={styles.buttonText1}>
                    {!blowing ? "송풍(탈취) 정지" : "송풍(탈취) 가동"}
                </Text>
            </TouchableOpacity> */}
        </View>
    );
}
const styles = StyleSheet.create({
    swipeHiddenItemContainer: {
        flex: 1,
        height: '100%',
        justifyContent: 'space-between',
        alignItems: 'center',
        backgroundColor: '#753CEF',
        flexDirection: 'row',
    },
    swipeHiddenItem: {
        width: 70,
        height: '100%',
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 20,
    },
    swipeHiddenItemText: {
        color: 'black',
        fontSize: 14,
    },
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
        height: 46,
        width: 350,
        backgroundColor: '#753CEF'
    }
})
export default OperationButton;