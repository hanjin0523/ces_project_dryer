import React, { useState, useEffect } from "react";
import colors from "../../public/colors/colors";
import { StyleSheet, View, Image, Text, Alert } from "react-native";
import * as config from '../config';
import { ScrollViewIndicator } from "@fanchenbao/react-native-scroll-indicator";
import { TouchableOpacity } from "react-native-gesture-handler";
import { useDispatch, useSelector } from "react-redux";
import { detailSettingTemp, 
        detailSettingHum, 
        detailSettingTime,
        initTemp, initHum, initTimeValue } from '../reduxT/slice';
import AddStageModal from "../modal/AddStageModal";

interface propsType {
    select: number;
}

interface DetailSettingType {
    recipe_number: string;
    dry_number: number;
    numbering: number;
    dried_product_name: string;
    set_temperature: number;
    set_humidity: number;
    uptime: number;
}

const RecipeDetailSetting = React.memo((props: propsType) => {
    console.log(props.select)
    const server_ip = config.SERVER_URL;
    const dispacth = useDispatch();

    const setTemp = useSelector((state: any) => state.counter.setTemp)
    const setHum = useSelector((state: any) => state.counter.setHum)
    const setTime = useSelector((state: any) => state.counter.setTimeValue)

    const [detailList, setDetailList] = useState<DetailSettingType[]>([]);
    const [active, setActive] = useState<number>(0);
    const [addModalOpen, setAddModalOpen] = useState<boolean>(false);
    console.log(active, "active")

    const addStageModal = () => {
        setAddModalOpen(true)
    }
    const closeStageModal = () => {
        setAddModalOpen(false)
    }

    useEffect(() => {
        if (detailList.length > 0) {
            const temp = detailList[active].set_temperature
            const hum = detailList[active].set_humidity
            const time = detailList[active].uptime
            dispacth(detailSettingTemp(temp))
            dispacth(detailSettingHum(hum))
            dispacth(detailSettingTime(time))
        }
    }, [active])

    useEffect(() => {
        dispacth(initTemp())
        dispacth(initHum())
        dispacth(initTimeValue())
    },[props.select])

    const modifyStage = () => {
        if (detailList.length > 0 && detailList[active]) {
            fetch(`http://${server_ip}/modifyStage/`, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    seletStage: detailList[active].recipe_number,
                    settingTemp: setTemp,
                    settingHum: setHum,
                    settingTime: setTime
                })
            })
            .then(()=>getDetailRecipe())
        }
    }

    useEffect(() => {
        setActive(0);
    }, [props.select])

    const timeConversion = (seconds: number) => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        return `${hours}:${minutes}:${second}`;
    }

    const getDetailRecipe = () => {
        fetch(`http://${server_ip}/get_detail_recipe?selectNum=${props.select}`, {
        })
            .then((response) => response.json())
            .then((data) => {
                const detail_list = Array.from(data, (item: any) => ({
                    recipe_number: item[0],
                    dry_number: item[1],
                    numbering: item[2],
                    dried_product_name: item[3],
                    set_temperature: item[4],
                    set_humidity: item[5],
                    uptime: item[6]
                }));
                setDetailList(detail_list);
            })
    }
    useEffect(() => {
        getDetailRecipe();
    }, [props.select])

    const deleteStage = () => {
        const stage_num = detailList[active].recipe_number
        fetch(`http://${server_ip}/delete_stageNum?stageNum=${stage_num}`, {
            method: "DELETE"
        })
        .then(()=>{Alert.alert("삭제합니다"); getDetailRecipe()})
    }

    if (detailList.length > 0) {
        return (
            <View style={styles.mainBox}>
                <AddStageModal isvisible={addModalOpen} 
                                propsFn={closeStageModal}
                                selectNum={detailList[active].dry_number}
                                propsDetailFn={getDetailRecipe}/>
                <ScrollViewIndicator indStyle={{ backgroundColor: '#6C3CF0' }}>
                    {detailList.map((item, idx) => (
                        <TouchableOpacity style={styles.stageButton} key={idx}  onPressIn={()=>{modifyStage(); setActive(idx);}} onLongPress={()=>{setActive(idx-1); deleteStage(); }}>
                            <View style={styles.stageBox}>
                                <View style={[styles.imgBox, active === idx ? null : { backgroundColor: '#F5F6FA' }]}>
                                    <Image style={[{ height: '40%', width: '40%' }, active === idx ? null : { opacity: 0.4 }]} source={require('../../public/images/stageClick.png')} resizeMode="contain" />
                                    <Text style={[{ fontSize: 16, color: '#FFFFFF', fontWeight: '600' }, active === idx ? null : { color: '#E7E7EC' }]}>Stage{idx + 1}</Text>
                                </View>
                                <View style={styles.imgText}>
                                    <Text style={active === idx ? styles.tempText : styles.tempTextNon}>{item.set_temperature}°C</Text>
                                    <Text style={active === idx ? styles.tempText : styles.tempTextNon}>{item.set_humidity}%</Text>
                                    <Image style={{ height: '45%', marginTop: '6%', marginLeft: '5%' }} tintColor={active === idx ? 'black' : '#E7E7EC'} source={require('../../public/images/stageTime.png')} resizeMode="contain" />
                                    <Text style={active === idx ? styles.timeText : styles.timeTextNon}>{timeConversion(item.uptime)}</Text>
                                </View>
                            </View>
                        </TouchableOpacity>))}
                </ScrollViewIndicator>
                <View style={styles.addOutBox}>
                    <TouchableOpacity style={styles.addBox} onPress={()=>addStageModal()}>
                        <Image style={{ height: '58%' }} source={require('../../public/images/addRecipe.png')} resizeMode="contain" />
                    </TouchableOpacity>
                </View>
            </View>
        )
    } else {
        return (
            <View style={styles.mainBox}>
                <ScrollViewIndicator indStyle={{ backgroundColor: '#6C3CF0' }}>
                    <TouchableOpacity style={styles.stageButton}>
                        <View style={styles.stageBox}>
                            <View style={styles.imgBox}>
                                <Image style={{ height: '40%', width: '40%' }} source={require('../../public/images/stageClick.png')} resizeMode="contain" />
                                <Text style={{ fontSize: 16, color: '#FFFFFF', fontWeight: '600' }}>Stage{1}</Text>
                            </View>
                            <View style={styles.imgText}>
                                <Text style={styles.emptyTempText}>레시피가 없습니다 등록해주세요</Text>
                            </View>
                        </View>
                    </TouchableOpacity>
                </ScrollViewIndicator>
                <View style={styles.addOutBox}>
                    <TouchableOpacity style={styles.addBox} onPress={addStageModal}>
                        <Image style={{ height: '58%' }} source={require('../../public/images/addRecipe.png')} resizeMode="contain" />
                    </TouchableOpacity>
                </View>
            </View>);
    }
})
const styles = StyleSheet.create({
    mainBox: {
        // borderWidth: 1,
        height: '73%',
        width: 395,
        alignItems: 'center',
    },
    stageBox: {
        height: 70,
        width: 380,
        flexDirection: 'row',
    },
    imgBox: {
        backgroundColor: '#753CEF',
        width: 90,
        height: 70,
        borderTopLeftRadius: 5,
        borderBottomLeftRadius: 5,
        alignItems: 'center',
        justifyContent: 'center',
    },
    stageButton: {
        width: '100%',
        height: 70,
        marginBottom: 10,
        backgroundColor: '#FFFFFF',
        borderColor: '#D9D9D9',
        borderWidth: 1,
        borderRadius: 5,
        elevation: 5,
    },
    imgText: {
        width: '58%',
        height: '60%',
        marginLeft: 10,
        marginTop: 13,
        flexDirection: 'row',
    },
    tempText: {
        color: colors.black,
        fontSize: 27,
        borderRightWidth: 2,
        borderRightColor: '#DCDCDC',
        paddingRight: 10,
        paddingLeft: 10,
        fontWeight: '600'
    },
    tempTextNon: {
        color: '#E7E7EC',
        fontSize: 27,
        borderRightWidth: 2,
        borderRightColor: '#E7E7EC',
        paddingRight: 10,
        paddingLeft: 10,
        fontWeight: '600'
    },
    timeText: {
        color: colors.black,
        fontWeight: '600',
        marginTop: '4%',
        fontSize: 18
    },
    timeTextNon: {
        color: '#EEEFF0',
        fontWeight: '600',
        marginTop: '4%',
        fontSize: 18
    },
    emptyTempText: {
        color: colors.black,
        fontSize: 15,
        borderRightWidth: 2,
        borderRightColor: '#DCDCDC',
        paddingRight: 10,
        paddingLeft: 10,
        fontWeight: '600',
        marginTop: 10
    },
    addBox: {
        borderWidth: 1.5,
        borderColor: '#C3C2C7',
        borderStyle: 'dashed',
        borderRadius: 5,
        width: 380,
        height: '100%',
        marginTop: '2%',
        backgroundColor: 'rgba(239,234,255, 0.5)',
        alignItems: 'center',
        justifyContent: 'center'
    },
    addOutBox: {
        width: 380,
        height: '19%'
    }
})
export default RecipeDetailSetting;