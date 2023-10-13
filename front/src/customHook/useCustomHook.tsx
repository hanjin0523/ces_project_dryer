import { useState, useEffect } from "react";

export function useTimeConversion_ko(seconds: number): string {
    const [time, setTime] = useState('');

    useEffect(() => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        setTime(`${hours}시간 ${minutes}분 ${second}초`);
    }, [seconds]);

    return time;
}

export function useTimeConversion(seconds: number): string {
    const [time, setTime] = useState('');

    useEffect(() => {
        const hours = Math.floor(seconds / 3600) < 10 ? '0' + Math.floor(seconds / 3600) : Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60) < 10 ? '0' + Math.floor((seconds % 3600) / 60) : Math.floor((seconds % 3600) / 60);
        const second = seconds % 60 < 10 ? '0' + seconds % 60 : seconds % 60;

        setTime(`${hours}:${minutes}:${second}`);
    }, [seconds]);

    return time;
}


export function useDateAndTime() {
    const [date, setDate] = useState(new Date());
    const [time, setTime] = useState(new Date().toLocaleTimeString());

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

    return {
        date,
        time,
        month,
        day,
        dayOfWeek,
        dayOfWeekText,
    };
}