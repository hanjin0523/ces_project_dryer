import React, { useCallback, useEffect, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { useDispatch, useSelector } from 'react-redux';
import { settingHum, settingTemp, settingTime } from '../reduxT/slice';
import { RadialSlider } from 'react-native-radial-slider';
import colors from '../../public/colors/colors';

interface PropsType {
    select: string
}

const SliderButton = React.memo((props: PropsType) => {
    const dispatchTemp = useDispatch()
    // const dispatchTime = useDispatch()
    const [temp, setTemp] = useState(0)
    const [hum, setHum] = useState(0)
    const [time, setTime] = useState('')
    
    useEffect(()=>{
        setTemp(0)
        setHum(0)
        setTime('')
    },[props.select])

    const handleChange = (value: any) => {
        if (props.select === 'temp') {
            dispatchTemp(settingTemp(value))
            setTemp(value)
        }
        if (props.select === 'hum') {
            dispatchTemp(settingHum(value))
            setHum(value)
        }
        if(props.select === 'time') {
            dispatchTemp(settingTime(value*360))
            setTime(timeConversion(value*100))
        }
    }


    const timeConversion = (seconds: number) => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        return `${hours}: ${minutes}: ${second}`;
    }
    
    return (
        <View style={styles.mainBox}>
            <View style={{ zIndex: -1, elevation: 20, position: "absolute", backgroundColor: '#FFFFFF', height: "72%", width: "45.3%", borderRadius: 100 }} />
            <RadialSlider
                style={{ zIndex: 2 }}
                step={2}
                variant={'radial-circle-slider'}
                value={0}
                valueStyle={{ fontSize: 60, color: "black", alignItems: "center", justifyContent: "center", marginTop: 20 }}
                min={0}
                max={80}
                onChange={handleChange}
                radius={130}
                isHideSubtitle={Boolean}
                isHideTitle={Boolean}
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
})
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