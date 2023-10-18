import React, { useState } from "react";
import { StyleSheet, View } from "react-native";
import RecipeTitle from "./RecipeTitle";
import SliderButton from "./recipesliderBtn";
import RecipeButton from "./RecipeButton";
import Time from "../homeSecond/Time";
import RecipeList from "./RecipeList";

const RecipeBox = () => {

    const [select, setSelect] = useState<string>('')
    const selectBtn = (key: string) => {
        setSelect(key)
    }

    return (
        <View style={styles.RecipeMainBox}>
            <View style={styles.firstBox}>
                <RecipeTitle />
                <SliderButton select={select} />
                <RecipeButton fn={selectBtn} />
            </View>
            <View style={styles.secondBox}>
                    <Time />
                    <RecipeList />
            </View>
        </View>
    );
}
const styles = StyleSheet.create({
    RecipeMainBox: {
        backgroundColor: '#EFEAFF',
        height: '100%',
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row'
    },
    firstBox: {
        height: '90%',
        width: '47%'
    },
    secondBox: {
        height: '90%',
        width: '47%',
        backgroundColor: '#ffffff',
        borderRadius: 20,
        elevation:20,
        // justifyContent: 'center',
        alignItems: 'center'
    },
})
export default RecipeBox;