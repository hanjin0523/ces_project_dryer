import React, { useEffect, useState } from "react";
import colors from '../../public/colors/colors';
import * as config from '../config';
import { StyleSheet, View, Text, Image, TouchableOpacity } from "react-native";
import Time from "../homeSecond/Time";
import { useDispatch, useSelector } from "react-redux";
import {selectDryer} from "../reduxT/slice";

interface Dryer_List {
    dryer_number: number;
    dryer_ipaddress: string;
    last_access_date: string;
    dryer_status: number;
}

const SecondBox = () => {
    const dispatch = useDispatch()
    const server_ip = config.SERVER_URL;
    const [dryerNum, setDryerNum] = useState<number>(0)
    const [dryerList, setDryerList] = useState<string[]>([])

    console.log(dryerList, "---------data---------")

    const selectNum = (key: number) => {
        setDryerNum(key)
    }

    const loadDryer = () => {
        fetch(`http://${server_ip}/dryer_connection_list/`)
            .then((response) => response.json())
            .then((data) => {
                setDryerList(data)
                if (data.length === 0) {
                    dispatch(selectDryer(dryerNum));
                }
            })
            .catch((error) => {
                console.log("건조기접속확인에러..", error)
            })
    }

    useEffect(() => {
        loadDryer();
        const intervalId = setInterval(loadDryer, 5000); // 5초마다 실행
        return () => {
          clearInterval(intervalId); // 컴포넌트가 언마운트될 때 interval 해제
        };
    }, [dryerNum]);

    const chageDryerNum = (device_id: string, dryer_number: number) => {
        console.log(device_id, dryer_number, "device_id, dryer_number")
        fetch(`http://${server_ip}/change_dryer_num?device_id=${device_id}&dryer_number=${dryer_number}`)
        .then(()=> dispatch(selectDryer(dryer_number)));
    }

    return (
        <View style={styles.mainBox}>
            <Time />
            <View style={styles.listBox}>
                <TouchableOpacity>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtn.png')} resizeMode="contain" />
                </TouchableOpacity>
                <View style={styles.menu}>
                    {dryerList.map((item, idx) => (
                        <TouchableOpacity key={idx} style={dryerNum === idx ? styles.menuBtn1Act : styles.menuBtn1} onPress={()=>{selectNum(idx); setDryerNum(idx); chageDryerNum(item, idx); }}>
                            <View >
                                <Text style={{color:'red'}}>
                                    일련번호 : {(item)} 건조기
                                </Text>
                            </View>
                        </TouchableOpacity>
                    ))}
                </View>
                <View style={styles.addBtn}>
                </View>
                <TouchableOpacity>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtnR.png')} resizeMode="contain" />
                </TouchableOpacity>
            </View>
                {/* <TouchableOpacity onPress={()=>test_packet()} style={{width:100,backgroundColor:"gray",marginBottom:20,}}>
                    <Text style={{color:"white"}}>세션확인요청</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={()=>test_packet1()} style={{width:100,backgroundColor:"gray",marginBottom:20,}}>
                    <Text style={{color:"white"}}>센서데이터요청</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={()=>test_packet2()} style={{width:100,backgroundColor:"gray",marginBottom:20,}}>
                    <Text style={{color:"white"}}>완전정지</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={()=>test_packet3()} style={{width:100,backgroundColor:"gray",marginBottom:20,}}>
                    <Text style={{color:"white"}}>일시정지</Text>
                </TouchableOpacity>
                <TouchableOpacity onPress={()=>test_packet4()} style={{width:100,backgroundColor:"gray",marginBottom:20,}}>
                    <Text style={{color:"white"}}>가동명령</Text>
                </TouchableOpacity> */}
        </View>
    );
}
const styles = StyleSheet.create({
    mainBox: {
        backgroundColor: '#FFFFFF',
        height: '100%',
        width: '100%',
        borderRadius: 20,
        alignItems: 'center',
    },
    listBox: {
        // borderWidth: 1,
        height: '25%',
        width: '88%',
        alignItems: 'center',
        flexDirection: 'row'
    },
    buttonImg: {
        height: '12%',
    },
    menu: {
        // borderWidth: 1,
        width: '65%',
        height: '100%',
        alignItems: 'center',
        flexDirection: 'row'
    },
    menuBtn1:{
        borderWidth: 1,
        width: '28%',
        height: '70%',
        marginRight: '5%',
        borderRadius: 5,
        alignItems: 'center',
        justifyContent: 'center',
        borderColor: '#E6E6E6'
    },
    menuBtn1Act:{
        borderWidth: 1,
        width: '28%',
        height: '70%',
        marginRight: '5%',
        borderRadius: 5,
        alignItems: 'center',
        justifyContent: 'center',
        borderColor: '#E6E6E6',
        backgroundColor: '#6A3CF0'
    },
    addBtn: {
        borderWidth: 2,
        width: '18%',
        height: '70%',
        borderRadius: 5,
        borderStyle: 'dotted',
        borderColor: '#E6E6E6'
    }
})
export default SecondBox;