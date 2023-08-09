import { createSlice } from "@reduxjs/toolkit";
import { combineReducers } from "@reduxjs/toolkit";

export const counterSlice = createSlice({
    name: 'counter',
    initialState:{
        heatRay: false,
        blowing: false,
        setTime: '',
        operTime: '',
        setTemp: 0,
        setHum: 0,
        setTimeValue: '00:00'
    },
    reducers: {
        heatRayOper: (state) => {
            state.heatRay = !state.heatRay
        },
        decrement: (state) => {
            state.blowing = !state.blowing
        },
        settingTimer: (state, time) => {
            state.setTime = time['payload']
        },
        initTime: (state) => {
            state.operTime = ''
        },
        operationTimer: (state, time) => {
            state.operTime = time['payload']
        },
        operationStartTimer: (state) => {
            state.operTime = state.operTime - 1;
        },
        settingTemp: (state, value) => {
            state.setTemp = value['payload']
        },
        settingHum: (state, value) => {
            state.setHum = value['payload']
        },
        settingTime: (state, value) => {
            state.setTimeValue = value['payload']
        },
        initTemp: (state) => {
            state.setTemp = '0'
        },
        initHum: (state) => {
            state.setHum = '0'
        },
        initTimeValue: (state) => {
            state.setTimeValue = ''
        },
        detailSettingTemp: (state, temp) => {
            state.setTemp = temp['payload']
        },
        detailSettingHum: (state, hum) => {
            state.setHum = hum['payload']
        },
        detailSettingTime: (state, time) => {
            state.setTimeValue = time['payload']
        }
    },
})
export const { 
            initTemp,
            initHum,
            initTimeValue,
            heatRayOper, 
            decrement, 
            settingTimer, 
            initTime, 
            operationTimer, 
            operationStartTimer,
            settingTemp,
            settingHum,
            settingTime,
            detailSettingTemp,
            detailSettingHum,
            detailSettingTime} = counterSlice.actions;
export default counterSlice.reducer;
