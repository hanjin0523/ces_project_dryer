import React, { useState } from "react";
import colors from "../../public/colors/colors";
import { StyleSheet, View } from "react-native";
import RecipeTitle from "./RecipeTitle";
import SliderButton from "./recipesliderBtn";
import RecipeButton from "./RecipeButton";


const RecipeBox = () => {

    const [select, setSelect] = useState<string>('temp')
    console.log(select)
    const selectBtn = (key: string) => {
        setSelect(key)
    }

    return (
        <View style={styles.RecipeMainBox}>
            <View style={styles.firstBox}>
                <RecipeTitle />
                <SliderButton select={select}/>
                <RecipeButton fn={selectBtn}/>
            </View>
            <View style={styles.firstBox}>

            </View>
        </View>    
    );
}
const styles = StyleSheet.create({
    RecipeMainBox: {
        // borderWidth: 1,
        height: '100%',
        width: '100%',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'row'
    },
    firstBox: {
        borderWidth: 1,
        height: '90%',
        width: '47%'
    }
})
export default RecipeBox;