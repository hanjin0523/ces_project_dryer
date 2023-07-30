import React, { useCallback, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';

import { RadialSlider } from 'react-native-radial-slider';
import colors from '../../public/colors/colors';

interface PropsType{
    select: string
}

const SliderButton = (props: PropsType) => {
    const [temp, setTemp] = useState<number>(0)

    const handleChangeTemp = useCallback((value: any) => {
        setTemp(value);
    }, []);

    return(
        <View style={styles.mainBox}>
            <View style={{zIndex:0,elevation:20,position:"absolute", backgroundColor:'#FFFFFF', height:"72.36%", width:"45.3%", borderRadius: 100}}/>
            <RadialSlider
            style={{zIndex:2}}
            step={2}
            variant={'radial-circle-slider'}
            value={temp}
            valueStyle={{fontSize:60,color:"black",alignItems:"center",justifyContent:"center", marginTop:20}}
            min={0}
            max={80}
            onChange={handleChangeTemp}
            radius={130}
            isHideSubtitle={Boolean}
            isHideTitle={Boolean} 
            unit={'°C'}
            unitStyle={{marginLeft:0,fontWeight:"bold",marginTop:35}}
            thumbColor={'#FF7345'}
            thumbRadius={11}
            thumbBorderWidth={4}
            sliderWidth={8}
            linearGradient ={[ { offset: '0%', color:'#FFD76F' }, 
            { offset: '100%', color: '#FF7345' }]}
            />
            <View style={{width:"100%", position:"absolute"}}>
                <Text style={{color:colors.black, fontSize:15, marginLeft:"15%", fontWeight:"600"}}>
                    {props.select === 'temp' ? "20℃" : props.select === 'hum' ? "20%" : "02:00"}
                </Text>
                <Text style={{color:colors.black, fontSize:15, marginLeft:"79%", position:'absolute', fontWeight:"600"}}>
                    {props.select === 'temp' ? "60℃" : props.select === 'hum' ? "60%" : "06:00"}
                </Text>
            </View>
                <Text style={{color:colors.black, fontSize:15, marginBottom:"63%", position:'absolute', fontWeight:"600"}}>
                    {props.select === 'temp' ? "40℃" : props.select === 'hum' ? "40%" : "04:00"}
                </Text>
        </View>
    );
}
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