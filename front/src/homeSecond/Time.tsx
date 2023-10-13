import React, { useEffect, useState } from "react";
import colors from "../../public/colors/colors";
import { StyleSheet, Text, View } from "react-native";
import { useDateAndTime } from "../customHook/useCustomHook";

const Time = () => {

    const { time, month, day, dayOfWeek, dayOfWeekText } = useDateAndTime();

    return (
        <View style={styles.timeMainBox}>
            <Text style={styles.TimeText}>{month}월 {day}일 {dayOfWeekText[dayOfWeek]}</Text>
            <Text style={styles.subText}>{time}</Text>
        </View>
    );
}
const styles = StyleSheet.create({
    timeMainBox: {
        marginTop: "10%",
        borderBottomWidth: 1,
        height: "8%",
        width: "86%",
        borderBottomColor: '#E5E5E5',
        flexDirection: 'row'
    },
    TimeText: {
        fontSize: 25,
        color: colors.black,
        fontWeight: '700'
    },
    subText: {
        fontSize: 15,
        marginTop: '1.5%',
        marginLeft: '2%',
        color: colors.black,
        fontWeight: "600"
    }
})
export default Time;
