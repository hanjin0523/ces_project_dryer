import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useDispatch } from 'react-redux';
import { settingHum, settingTemp, settingTime } from '../reduxT/slice';
import { RadialSlider } from 'react-native-radial-slider';
import colors from '../../public/colors/colors';
import { useTimeConversion } from '../customHook/useCustomHook';

interface PropsType {
    select: string
}

const SliderButton = (props: PropsType) => {
    const dispatch = useDispatch()
    const [value, setValue] = useState(0);
    const time1 = useTimeConversion(value*360)

    useEffect(() => {
        setValue(0);
    }, [props.select]);

    console.log(value)

    const handleChange = (newValue: number) => {
        setValue(newValue);
        if (props.select === 'temp') {
            dispatch(settingTemp(newValue));
        } else if (props.select === 'hum') {
            dispatch(settingHum(newValue));
        } else if (props.select === 'time') {
            dispatch(settingTime(newValue * 360));
        }
    };

    return (
        <View style={styles.mainBox}>
            <View style={{ zIndex: -1, elevation: 20, position: "absolute", backgroundColor: '#FFFFFF', height: "72%", width: "45.3%", borderRadius: 100 }} />
            <RadialSlider
                style={{ zIndex: 3 }}
                step={2}
                variant={'radial-circle-slider'}
                value={value}
                valueStyle={{ fontSize: 60, color: "black", alignItems: "center", justifyContent: "center", marginTop: 20 }}
                min={0}
                max={80}
                onChange={handleChange}
                radius={130}
                isHideSubtitle={false}
                isHideTitle={false}
                subTitle=''
                unit={props.select === 'temp' ? '°C' : props.select === 'hum' ? '%' : ''}
                unitStyle={{ marginLeft: 0, fontWeight: "bold", marginTop: 35 }}
                thumbColor={'#FF7345'}
                thumbRadius={11}
                thumbBorderWidth={4}
                sliderWidth={8}
                linearGradient={[{ offset: '0%', color: '#FFD76F' },
                { offset: '100%', color: '#FF7345' }]}
            />
            <View style={props.select === 'time' ? { position: 'absolute', zIndex: 3, backgroundColor: 'white', height: 100, width: 180, justifyContent: "center", alignItems: "center" } : { position: 'absolute',display: 'none', zIndex: 0, backgroundColor: 'white', justifyContent: "center", alignItems: "center" }}>
                <Text style={{ fontSize: 38, color: "black", fontWeight: "900" }}>{time1}</Text>
            </View>
            <View style={{ width: "100%", position: "absolute", flexDirection: 'row' }}>
                <Text style={{ color: colors.black, fontSize: 15, marginLeft: "15%", fontWeight: "600" }}>
                    {props.select === 'temp' ? "20℃" : props.select === 'hum' ? "20%" : "02:00"}
                </Text>
                <Text style={{ color: colors.black, fontSize: 15, marginLeft: "57%", fontWeight: "600" }}>
                    {props.select === 'temp' ? "60℃" : props.select === 'hum' ? "60%" : "06:00"}
                </Text>
            </View>
            <Text style={{ color: colors.black, fontSize: 15, marginBottom: "63%", position: 'absolute', fontWeight: "600", }}>
                {props.select === 'temp' ? "40℃" : props.select === 'hum' ? "40%" : "04:00"}
            </Text>
        </View>
    );
};
export default SliderButton;
const styles = StyleSheet.create({
    mainBox: {
        justifyContent: 'center',
        alignItems: 'center',
        width: "100%",
        height: "50%",
        // borderWidth: 1,
    }

})