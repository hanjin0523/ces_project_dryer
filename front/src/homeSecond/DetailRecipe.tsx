import React, { useEffect } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";
import * as config from '../config';
import { ScrollViewIndicator } from "@fanchenbao/react-native-scroll-indicator";
import BouncyCheckbox from "react-native-bouncy-checkbox";

interface TypeRecipeNum{
    recipeNum: number;
}



const DetailRecipe = (props: TypeRecipeNum) => {
    
    const server_ip = config.SERVER_URL;

    useEffect(() => {
        fetch(`http://${server_ip}/get_detail_recipe/${props.recipeNum}`)
            .then(() => console.log("성공!!"))
    },[props.recipeNum])

    return (
        <View style={styles.DetailBox}>
            <View style={styles.title}>
                <Text style={styles.titleText}>레시피 이름</Text>
                <Text style={styles.titleText1}>총 건조시간</Text>
                <Text style={styles.titleText2}>스테이지</Text>
            </View>
            <ScrollViewIndicator>
                <View style={styles.detailList}>
                    <BouncyCheckbox
                        isChecked={false}
                        size={16}
                        fillColor="#763AFF"
                        unfillColor="#E1E3E6"
                        iconStyle={{ borderRadius: 3, borderWidth: 0 }}
                        innerIconStyle={{ borderWidth: 0}}
                        style={styles.checkBox1}
                        onPress={(checked1) => {
                            // setChecked1(checked1);
                            // storeData(checked1);
                        }}
                    />
                    <Text style={styles.detailTitle}>청양고추건조</Text>
                    <Text style={styles.detailTime}>14시 21분 16초</Text>
                    <Text style={styles.detailStage}>4</Text>
                </View>
            </ScrollViewIndicator>
        </View>
    );
}
const styles = StyleSheet.create({
    DetailBox: {
        height: "40%",
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
        height: 51.2,
        textAlign: "center"
    },
    checkBox1:{
        marginLeft:25,
    },
    detailTitle: {
        fontSize: 15,
        width: "20%",
        height: '100%',
        fontWeight: '400',
        textAlign: "center",
        lineHeight: 47,
        marginLeft: "-3%",
        color: '#A3A2A8'
    },
    detailTime: {
        fontSize: 15,
        width: "43%",
        height: '100%',
        fontWeight: '400',
        textAlign: "center",
        lineHeight: 47,
        color: '#A3A2A8'
    },
    detailStage: {
        fontSize: 15,
        width: "29%",
        height: '100%',
        fontWeight: '400',
        textAlign: "center",
        lineHeight: 47,
        paddingLeft: '3.2%',
        color: '#A3A2A8'
    }
})
export default DetailRecipe;