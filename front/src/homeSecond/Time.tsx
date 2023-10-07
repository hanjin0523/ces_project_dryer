import React, { useEffect, useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";

const Time = () => {

    const [time, setTime] = useState(new Date().toLocaleTimeString());
    const [date, setDate] = useState(new Date());

    useEffect(() => {
        const intervalId = setInterval(() => {
            setTime(new Date().toLocaleTimeString());
            setDate(new Date());
        }, 1000);

        return () => {
            clearInterval(intervalId);
        };
    }, []);

    const month = date.getMonth() + 1;
    const day = date.getDate();
    const dayOfWeek = date.getDay();

    const dayOfWeekText = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일'];


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
