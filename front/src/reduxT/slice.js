import { createSlice } from "@reduxjs/toolkit";
import { combineReducers } from "@reduxjs/toolkit";

export const counterSlice = createSlice({
    name: 'counter',
    initialState:{
        heatRay: false,
        blowing: false,
        setTime: '',
        operTime: '',
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
        }
    },
})
export const { heatRayOper, decrement, settingTimer, initTime, operationTimer, operationStartTimer} = counterSlice.actions;
export default counterSlice.reducer;
