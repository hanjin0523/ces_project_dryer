import React, { useEffect, useState } from "react";
import colors from "../../public/colors/colors";
import { Alert, StyleSheet, Text, View } from "react-native";
import * as config from '../config';
import { ScrollViewIndicator } from "@fanchenbao/react-native-scroll-indicator";
import { useDispatch, useSelector } from "react-redux";
import { settingTimer, initTimeValue, operationTimer } from "../reduxT/slice";
import { RadioButton } from 'react-native-paper';

interface TypeRecipeNum {
    recipeNum: number;
}

interface Detail_recipe {
    dried_product_name: string;
    dry_number: number;
    total_stage_number: number;
    total_uptime: number;
}



const DetailRecipe = (props: TypeRecipeNum) => {
    
    const dispatch = useDispatch();
    const server_ip = config.SERVER_URL;
    const [detailRecipe, setDetailRecipe] = useState<Detail_recipe[]>([]);
    const [isChecked, setIsChecked] = useState<boolean>(false);
    const status = useSelector((state: any) => state.counter.status);

    // 함수: 시간 변환
    const timeConversion = (seconds: number) => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;
        return `${hours}시간 ${minutes}분 ${second}초`;
    };

    // 함수: 레시피 상세 정보 로딩
    const loadRecipeDetails = () => {
        if (status === false) {
            fetch(`http://${server_ip}/get_detail_recipe/${props.recipeNum}`)
                .then((response) => response.json())
                .then((detailRecipe) => {
                    const detailList = Array.from(detailRecipe, (item: any) => ({
                        dried_product_name: item[0],
                        dry_number: item[1],
                        total_stage_number: item[2],
                        total_uptime: item[3],
                    }));
                    setDetailRecipe(detailList);
                });
        }
    };

    // 함수: 레시피 선택 변경
    const handleRecipeSelection = (item: Detail_recipe) => {
        if (status === false) {
            dispatch(settingTimer(item.total_uptime));
            dispatch(operationTimer(item.total_uptime));
            toggleCheckbox();
        } else {
            Alert.alert("건조기를 정지한 후 사용하세요.");
        }
    };

    // 함수: 체크박스 토글
    const toggleCheckbox = () => {
        if (status === false) {
            setIsChecked(!isChecked);
            if (isChecked) {
                resetOperation();
            }
        }
    };

    // 함수: 작업 초기화
    const resetOperation = () => {
        setIsChecked(false);
        dispatch(operationTimer(0));
    };

    useEffect(() => {
        dispatch(initTimeValue());
    }, [props.recipeNum]);

    useEffect(() => {
        loadRecipeDetails();
    }, [props.recipeNum]);

    useEffect(() => {
        if (isChecked === true) {
            const dry_number = props.recipeNum;
            fetch(`http://${server_ip}/send_operating_conditions/setting_on?dry_number=${dry_number}`)
                .then((response) => response.json());
        } else {
            fetch(`http://${server_ip}/send_operating_conditions/setting_off`);
            resetOperation();
        }
    }, [isChecked]);

    useEffect(() => {
        setIsChecked(false);
        resetOperation();
    }, [props.recipeNum]);

    return (
        <View style={styles.DetailBox}>
            <View style={styles.title}>
                <Text style={styles.titleText}>레시피 이름</Text>
                <Text style={styles.titleText1}>총 건조시간</Text>
                <Text style={styles.titleText2}>스테이지</Text>
            </View>
            <ScrollViewIndicator>
                {detailRecipe.length > 0 ? (
                    detailRecipe.map((item, idx) => (
                        <View style={styles.detailList} key={idx}>
                            <RadioButton
                                value='1'
                                status={isChecked === true ? 'checked' : 'unchecked'}
                                onPress={() => handleRecipeSelection(item)}
                            />
                            <Text style={styles.detailTitle}>{item.dried_product_name}</Text>
                            <Text style={styles.detailTime}>{timeConversion(item.total_uptime)}</Text>
                            <Text style={styles.detailStage}>{item.total_stage_number}</Text>
                        </View>
                    ))
                ) : (
                    <View style={styles.detailNot}>
                        <Text style={{ width: '100%', fontSize: 15 }}>등록된 레시피가 없습니다...레시피설정을 해주세요...</Text>
                    </View>
                )}
            </ScrollViewIndicator>
        </View>
    );
};

const styles = StyleSheet.create({
    DetailBox: {
        height: "37%",
        width: "84%",
        alignItems: 'center',
    },
    title: {
        backgroundColor: "#F5F6FA",
        height: "20%",
        flexDirection: "row",
        borderTopLeftRadius: 10,
        borderTopRightRadius: 10,
    },
    titleText: {
        color: colors.black,
        fontSize: 15,
        width: "24%",
        textAlign: "center",
        lineHeight: 50,

    },
    titleText1: {
        color: colors.black,
        fontSize: 16,
        width: "52%",
        textAlign: "center",
        lineHeight: 50,
    },
    titleText2: {
        color: colors.black,
        fontSize: 16,
        width: "24%",
        textAlign: "center",
        lineHeight: 50,
    },
    detailList: {
        flexDirection: 'row',
        width: '100%',
        height: 47.2,
        textAlign: "center",
        borderBottomWidth: 1,
        borderColor: '#E5E5E5',
    },
    detailNot: {
        flexDirection: 'row',
        width: '100%',
        height: 51.2,
        textAlign: "center",
        borderBottomWidth: 1,
        borderColor: '#E5E5E5',
        justifyContent: 'center',
        alignItems: 'center',
        paddingLeft: '20%',
    },
    checkBox1: {
        marginLeft: 25,
    },
    detailTitle: {
        fontSize: 15,
        width: "20%",
        height: '100%',
        fontWeight: '400',
        textAlign: "left",
        lineHeight: 47,
        paddingLeft: "2%",
        color: '#A3A2A8',
    },
    detailTime: {
        fontSize: 15,
        width: "43%",
        height: '100%',
        fontWeight: '400',
        textAlign: "center",
        lineHeight: 47,
        color: '#A3A2A8',
        paddingLeft: '9%',
    },
    detailStage: {
        fontSize: 15,
        width: "29.6%",
        height: '100%',
        fontWeight: '400',
        textAlign: "center",
        lineHeight: 47,
        color: '#A3A2A8',
        paddingLeft: '16%'
    },
})
export default DetailRecipe;