import React, { useEffect, useState } from "react";
import colors from "../../public/colors/colors";
import { Image, StyleSheet, Text, View } from "react-native";
import { TouchableOpacity } from "react-native-gesture-handler";
import * as config from '../config';
import DetailRecipe from "./DetailRecipe";
import OperationButton from "./button";

interface MenuInterface {
    dry_number: number,
    product_name: string,
    modify_date: string
}

const Menu = React.memo(() => {

    const server_ip = config.SERVER_URL;
    const [menuList, setMenuList] = useState<MenuInterface[]>([]);
    const [selectedButton, setSelectedButton] = useState<number>(0);
    const [startIndex, setStartIndex] = useState<number>(0);
    const [selectMenuNumber, setSelectMenuNumber] = useState<number>(0);

    const onPress = (key: number) => {
        setSelectedButton(key)
    }

    useEffect(() => {
        fetch(`http://${server_ip}/get_dry_menulist`)
            .then((response) => response.json())
            .then((drylist) => {
                const menuList = Array.from(drylist, (item: any) => ({
                    dry_number: item[0],
                    product_name: item[1],
                    modify_date: item[2],
                }));
                setMenuList(menuList);
                if (menuList.length > 0) {
                    setSelectMenuNumber(menuList[0].dry_number);
                }
            });
    }, []);

    const plus = () => {
        if (selectedButton < menuList.length - (menuList.length - (maxItems - 1))) {
            setSelectedButton((prev) => prev + 1);
        }
        else {
            setStartIndex((prev) => Math.min(prev + 1, menuList.length - maxItems));
        }
    };
    useEffect(() => {
        const selectedItem = menuList[startIndex + selectedButton];
        if (selectedItem) {
            setSelectMenuNumber(selectedItem.dry_number);
        }
    }, [selectedButton, startIndex]);
    

    const minus = () => {
        if (selectedButton > 0) {
            setSelectedButton((prev) => prev - 1);
        }
        else {
            setStartIndex((prev) => Math.max(0, prev - 1));
        }
    };


    const maxItems = 5;
    return (
        <>
            <View style={styles.menuBox}>
                <TouchableOpacity onPress={minus} style={styles.button}>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtn.png')} resizeMode="contain" />
                </TouchableOpacity>
                <View style={styles.menuMiddle}>
                    {menuList.slice(startIndex, startIndex + maxItems).map((item, idx) => (
                        <TouchableOpacity key={item.dry_number} onPress={() => { onPress(idx); setSelectMenuNumber(item.dry_number); }} style={selectedButton === idx ? styles.menuBtnAct : styles.menuBtn}>
                            <View style={styles.menulist}>
                                <Text style={selectedButton === idx ? styles.listText1 : styles.listText}>{item.product_name}</Text>
                            </View>
                        </TouchableOpacity>
                    ))}
                </View>
                <TouchableOpacity onPress={plus} style={styles.button}>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtnR.png')} resizeMode="contain" />
                </TouchableOpacity>
            </View>
            <DetailRecipe recipeNum={selectMenuNumber} />
            <OperationButton />
        </>
    );
})
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