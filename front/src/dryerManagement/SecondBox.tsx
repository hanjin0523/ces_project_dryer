import React, { useEffect, useState } from "react";
import colors from '../../public/colors/colors';
import * as config from '../config';
import { StyleSheet, View, Text, Image, TouchableOpacity } from "react-native";
import Time from "../homeSecond/Time";

interface Dryer_List {
    dryer_number: number;
    dryer_ipaddress: string;
    last_access_date: string;
    dryer_status: number;
}

const SecondBox = () => {
    const server_ip = config.SERVER_URL;
    const [dryerNum, setDryerNum] = useState<number>(0)
    const [dryerList, setDryerList] = useState<Dryer_List[]>([])
    
    const selectNum = (key: number) => {
        setDryerNum(key)
    }

    const loadDryer = () => {
        fetch(`http://${server_ip}/dryer_connection_list/`)
        .then((response) => response.json())
        .then((data) => {
            const dryerList = Array.from(data, (item: any) => ({
                dryer_number: item[0],
                dryer_ipaddress: item[1],
                last_access_date: item[2],
                dryer_status: item[3]
            }));
            setDryerList(dryerList);
        })
    }
    useEffect(()=>{
        loadDryer();
    },[])

    const chageDryerNum = (dryer_number: number) => {
        fetch(`http://${server_ip}/chage_dryer_num/${dryer_number}`)
        .then(()=>console.log(dryer_number))
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
                        <TouchableOpacity key={idx} style={dryerNum === idx ? styles.menuBtn1Act : styles.menuBtn1} onPress={()=>{selectNum(idx); chageDryerNum(item.dryer_number);}}>
                            <View >
                                <Text style={{color:'red'}}>
                                    {item.dryer_number}번 건조기
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