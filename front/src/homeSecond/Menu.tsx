import React, { useEffect, useState, useCallback } from "react";
import { Alert, StyleSheet, Text, View } from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";
import * as config from '../config';
import DetailRecipe from "./DetailRecipe";
import OperationButton from "./button";
import { useSelector } from "react-redux";

const MAX_MENU_ITEMS = 5;
const INITIAL_SELECTED_BUTTON = 0;

interface MenuInterface {
    dry_number: number;
    product_name: string;
    modify_date: string;
}

const Menu = () => {
    
    const server_ip = config.SERVER_URL;
    const [menuList, setMenuList] = useState<MenuInterface[]>([]);
    const [selectedButton, setSelectedButton] = useState<number>(INITIAL_SELECTED_BUTTON);
    const [startIndex, setStartIndex] = useState<number>(0);
    const [selectMenuNumber, setSelectMenuNumber] = useState<number>(0);
    const dryer_number = useSelector((state: any) => state.counter.dryerNumber);
    const status = useSelector((state: any) => state.counter.status);

    const onPress = useCallback((idx: number) => {
        if (status === false) {
            setSelectedButton(idx);
        } else {
            Alert.alert("건조기동작중입니다. 정지 후 사용가능합니다");
        }
    }, [status]);

    useEffect(() => {
        const fetchMenuList = () => {
            fetch(`http://${server_ip}/get_dry_menulist?dryer_number=${dryer_number}`)
                .then(response => response.json())
                .then(drylist => {
                    const menuList = Array.from(drylist, (item: any[]) => ({
                        dry_number: item[0],
                        product_name: item[1],
                        modify_date: item[2],
                    }));
                    setMenuList(menuList);
                    setSelectMenuNumber(0)
                    // if (menuList.length > 0) {
                    //     setSelectMenuNumber(menuList[0].dry_number);
                    // }
                });
        };
        fetchMenuList();
    }, [dryer_number]);

    useEffect(() => {
        const selectedItem = menuList[startIndex + selectedButton];
        if (selectedItem) {
            setSelectMenuNumber(selectedItem.dry_number);
        }
    }, [selectedButton, startIndex, menuList]);

    return dryer_number !== null ? (
        <>
            <View style={styles.menuBox}>
                <View style={styles.menuMiddle}>
                    {menuList.slice(startIndex, startIndex + MAX_MENU_ITEMS).map((item, idx) => (
                        <TouchableOpacity
                            key={item.dry_number}
                            onPress={() => {
                                onPress(idx);
                            }}
                            style={selectedButton === idx ? styles.menuBtnAct : styles.menuBtn}
                        >
                            <View style={styles.menulist}>
                                <Text style={selectedButton === idx ? styles.listText1 : styles.listText}>
                                    {item.product_name}
                                </Text>
                            </View>
                        </TouchableOpacity>
                    ))}
                </View>
            </View>
            <DetailRecipe recipeNum={selectMenuNumber} />
            <OperationButton />
        </>
    ) : null;
};
const styles = StyleSheet.create({
    menuBox: {
        height: '20%',
        width: '90%',
        flexDirection: 'row',
        alignItems: 'center',
        marginTop: '2%'
    },
    menuMiddle: {
        height: '100%',
        width: "84%",
        flexDirection: 'row',
        marginLeft: '3.5%',
    },
    button: {
        height: '60%',
        width: '100%',
    },
    buttonImg: {
        marginTop: '60%',
        height: '31%',
    },
    menulist: {

    },
    menuBtn: {
        backgroundColor: "#FFFFFF",
        borderWidth: 1,
        borderColor: '#E5E5E5',
        height: 95,
        width: 75,
        borderRadius: 5,
        marginTop: 12,
        marginRight: 20,
        justifyContent: 'center',
        alignItems: 'center',
        elevation: 5,

    },
    menuBtnAct: {
        backgroundColor: "#753CEF",
        borderWidth: 1,
        borderColor: '#753CEF',
        height: 95,
        width: 75,
        borderRadius: 5,
        marginTop: 12,
        marginRight: 20,
        justifyContent: 'center',
        alignItems: 'center',
        elevation: 5,
    },
    listText1: {
        fontSize: 15,
        color: '#ffffff'
    },
    listText: {
        fontSize: 15,
        color: '#D0D0D4'
    }
})
export default Menu;