import { createSlice } from "@reduxjs/toolkit";
import { combineReducers } from "@reduxjs/toolkit";

export const counterSlice = createSlice({
    name: 'counter',
    initialState:{
        dryerNumber: 0,
        heatRay: false,
        blowing: false,
        dehumidifier: false,
        setTime: '',
        operTime: '',
        setTemp: 0,
        setHum: 0,
        setTimeValue: '00:00',
        status: false
    },
    reducers: {
        selectDryer: (state, value) => {
            state.dryerNumber = value['payload']
        },
        heatRayOper: (state, value) => {
            state.heatRay = value['payload']
        },
        decrement: (state, value) => {
            state.blowing = value['payload']
        },
        dehumidifierControl: (state, value) => {
            state.dehumidifier = value['payload']
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
            state.setTime = ''
        },
        detailSettingTemp: (state, temp) => {
            state.setTemp = temp['payload']
        },
        detailSettingHum: (state, hum) => {
            state.setHum = hum['payload']
        },
        detailSettingTime: (state, time) => {
            state.setTimeValue = time['payload']
        },
        settingStatus: (state, status) => {
            state.status = status['payload']
        }
    },
})
export const { 
            selectDryer,
            initTemp,
            initHum,
            initTimeValue,
            heatRayOper, 
            decrement,
            dehumidifierControl, 
            settingTimer, 
            initTime, 
            operationTimer, 
            operationStartTimer,
            settingTemp,
            settingHum,
            settingTime,
            detailSettingTemp,
            detailSettingHum,
            detailSettingTime,
            settingStatus} = counterSlice.actions;
export default counterSlice.reducer;
