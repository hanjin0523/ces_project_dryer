import React, { useState } from "react";
import colors from '../../public/colors/colors';
import { StyleSheet, View, Text, Modal, TextInput, TouchableOpacity, Alert } from "react-native";
import SelectDropdown from "react-native-select-dropdown";
import * as config from '../config';

interface propsType {
    isvisible: boolean;
    selectNum: number;
    propsFn: () => void;
    propsDetailFn: () => void;
}

const AddStageModal = (props: propsType) => {
    const server_ip = config.SERVER_URL;
    const hour = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]
    const minite = ["0", "10", "20", "30", "40", "50"]
    const second = ["0", "10", "20", "30", "40", "50"]
    const [selectedHour, setSelectedHour] = useState<number>(0);
    const [selectedMinute, setSelectedMinute] = useState<number>(0);
    const [selectedSecond, setSelectedSecond] = useState<number>(0);
    const [addTemp, setAddTemp] = useState<string>("");
    const [valiInputTemp, setValiInputTemp] = useState<boolean>(false);
    const [addHum, setAddHum] = useState<string>("");
    const [valiInputHum, setValiInputHum] = useState<boolean>(false);
    console.log(((selectedHour * 60) * 60) + (selectedMinute * 60) + (selectedSecond*10/10))
    const initClose = () => {
        setSelectedHour(0);
        setSelectedMinute(0);
        setSelectedSecond(0);
        setAddTemp('');
        setAddHum('');
    }

    const sendAddStageInfo = () => {
        if (selectedHour !== 0 &&
            selectedMinute !== 0 &&
            selectedSecond !== 0 &&
            valiInputTemp === true &&
            valiInputHum === true) {
            fetch(`http://${server_ip}/add_stage_list/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    dryNumber: props.selectNum,
                    addTemp: addTemp,
                    addHum: addHum,
                    addTime: (((selectedHour * 60) * 60) + (selectedMinute * 60) + (selectedSecond*10/10))
                })
            })
                .then(() => {props.propsFn(); initClose(); props.propsDetailFn();})
        } else {
            Alert.alert("항목을 올바르게 채워주세요.")
        }
    }

    const inputAddTemp = (text: string) => {
        setAddTemp(text)
        setValiInputTemp(validateInput(text));
    }
    const inputAddHum = (text: string) => {
        setAddHum(text)
        setValiInputHum(validateInput(text));
    }
    const validateInput = (input: string) => {
        const trimmedInput = input.trim();
        const length = trimmedInput.length;
        const isNumeric = /^[0-9]+$/.test(trimmedInput);
        return length === 2 && isNumeric;
    }

    const handleHour = (selectedTime: number, index: number) => {
        setSelectedHour(selectedTime)
    };
    const handleMinute = (selectedTime: number, index: number) => {
        setSelectedMinute(selectedTime)
    };
    const handleSecond = (selectedTime: number, index: number) => {
        setSelectedSecond(selectedTime)
    };

    return (
        <Modal visible={props.isvisible} animationType="fade" transparent>
            <View style={styles.modalContainer}>
                <View style={styles.modalMainBox}>
                    <View style={styles.innerBox}>
                        <Text style={styles.titleText}>추가 스테이지 입력</Text>
                        <View style={{ width: '100%', height: '40%', flexDirection: 'row', }}>
                            <View style={styles.tempBox}>
                                <Text style={styles.mainText}>
                                    온도°C
                                </Text>
                                <TextInput onChangeText={inputAddTemp} style={valiInputTemp ? styles.textInput : [styles.textInput, { borderColor: '#B3261E' }]} placeholder="온도를 입력하세요" placeholderTextColor="#E5E5E5" />
                                <Text style={valiInputTemp ? { color: '#5C5C5C' } : { color: '#B3261E' }}>
                                    숫자 두자리로 입력
                                </Text>
                            </View>
                            <View style={styles.tempBox}>
                                <Text style={styles.mainText}>
                                    습도°C
                                </Text>
                                <TextInput onChangeText={inputAddHum} style={valiInputHum ? styles.textInput : [styles.textInput, { borderColor: '#B3261E' }]} placeholder="습도를 입력하세요" placeholderTextColor="#E5E5E5" />
                                <Text style={valiInputHum ? { color: '#5C5C5C' } : { color: '#B3261E' }}>
                                    숫자 두자리로 입력
                                </Text>
                            </View>
                        </View>
                        <View style={[styles.timeText, { flexDirection: 'row' }]} >
                            <Text style={[styles.mainText, { marginRight: '2%' }]}>시간</Text>
                            <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                                <Text style={{ marginRight: '12%' }}>hour</Text>
                                <Text style={{ marginRight: '20%' }}>minute</Text>
                                <Text style={{ marginRight: '20%' }}>second</Text>
                            </View>
                        </View>
                        <View style={{ flexDirection: 'row', height: '13%' }}>
                            <SelectDropdown buttonStyle={{ width: '30%', marginLeft: '5%', height: '100%' }} data={hour} onSelect={handleHour} defaultButtonText="시간" buttonTextStyle={{ fontSize: 16, fontWeight: '600' }} />
                            <SelectDropdown buttonStyle={{ width: '30%', marginLeft: '5%', height: '100%' }} data={minite} onSelect={handleMinute} defaultButtonText="분" buttonTextStyle={{ fontSize: 16, fontWeight: '600' }} />
                            <SelectDropdown buttonStyle={{ width: '30%', marginLeft: '5%', height: '100%' }} data={second} onSelect={handleSecond} defaultButtonText="초" buttonTextStyle={{ fontSize: 16, fontWeight: '600' }} />
                        </View>
                        <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'center', height: "16%", width: '100%', marginTop: '3%' }}>
                            <TouchableOpacity onPress={() => { props.propsFn(); initClose(); }} style={[styles.closeBtn, { borderColor: '#B5B3B9' }]}>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#B5B3B9' }}>닫기</Text>
                            </TouchableOpacity>
                            <TouchableOpacity onPress={() => { sendAddStageInfo();}} style={[styles.closeBtn, { borderColor: '#753CEF', backgroundColor: '#753CEF' }]}>
                                <Text style={{ fontSize: 16, fontWeight: '600', color: '#FFFFFF' }}>입력완료</Text>
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </View>
        </Modal>
    );
}
const styles = StyleSheet.create({
    modalContainer: {
        height: 760,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    modalMainBox: {
        backgroundColor: '#FFFFFF',
        borderRadius: 15,
        width: '25%',
        height: '45%',
        marginBottom: '28%',
        justifyContent: 'center',
        alignItems: 'center',
        // borderWidth: 1,
    },
    innerBox: {
        // borderWidth: 1,
        height: '90%',
        width: '85%',
    },
    titleText: {
        color: colors.black,
        fontSize: 22,
        fontWeight: '700',
        borderBottomWidth: 1,
        paddingBottom: 12,
        marginBottom: 12,
        borderColor: '#E5E5E5',
    },
    tempBox: {
        // borderWidth: 1,
        width: '48%',
        height: '40%',
        marginRight: '4%'
    },
    mainText: {
        fontSize: 18,
        fontWeight: '800',
        marginBottom: 5,
    },
    textInput: {
        borderWidth: 1,
        borderColor: '#E5E5E5',
        borderRadius: 5,
        marginBottom: 5,
        height: '100%'
    },
    timeText: {
        // borderWidth: 1,
        height: '10%'
    },
    closeBtn: {
        height: '100%',
        width: '49%',
        alignItems: 'center',
        justifyContent: 'center',
        borderWidth: 1,
        borderRadius: 5,
        marginRight: '1%',
        marginLeft: '1%'
    }
})
export default AddStageModal;