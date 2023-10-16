import React, { useState, useEffect, useCallback } from "react";
import { StyleSheet, View, Image, Text, Alert } from "react-native";
import * as config from '../config';
import { TouchableOpacity } from "react-native-gesture-handler";
import DeleteButton from "../modal/DeleteModal";
import ModifyModal from "../modal/ModifyModal";
import AddModal from "../modal/AddModal";
import RecipeDetailSetting from "./RecipeDetailSetting";
import { useSelector } from "react-redux";

interface MenuInterface {
    dry_number: number,
    product_name: string,
    modify_date: string
}

const RecipeList = React.memo(() => {
    const server_ip = config.SERVER_URL;
    const [menuList, setMenuList] = useState<MenuInterface[]>([]);
    const [selectedButton, setSelectedButton] = useState<number>(0);
    const [startIndex, setStartIndex] = useState<number>(0);
    const [selectMenuNumber, setSelectMenuNumber] = useState<number>(0);
    const [delModalVisible, setDelModalVisible] = useState<boolean>(false);
    const [modifyModalVisible, setModifyModalVisible] = useState<boolean>(false);
    const [addModalVisible, setAddModalVisible] = useState<boolean>(false);
    const dryer_number = useSelector((state: any) => state.counter.dryerNumber);

    const toggleModal = (modalType: string) => {
        
        switch (modalType) {
            case 'delete':
                setDelModalVisible(!delModalVisible);
                break;
            case 'modify':
                setModifyModalVisible(!modifyModalVisible);
                break;
            case 'add':
                setAddModalVisible(!addModalVisible);
                break;
            default:
                break;
        }
    }


    const performDryNameAction = (actionType: string, text: string, valiInput = false) => {

        switch (actionType) {
            case 'add':
                addDryName(text, valiInput);
                break;
            case 'delete':
                deleteDryName(selectMenuNumber);
                break;
            case 'modify':
                modifyDryName(text, valiInput);
                break;
            default:
                return;
        }
    }

    const addDryName = (text: string, valiInput: boolean) => {
        console.log(valiInput,"valiInput")
        if (valiInput) {
            fetch(`http://${server_ip}/add_dry_name/`, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    inputName: text,
                    dryerNumber: dryer_number,
                }),
            })
                .then(() => setAddModalVisible(false));
        } else {
            Alert.alert("공백포함 6자이내를 확인해주세요.");
        }
    };

    const deleteDryName = (selectNum: number) => {
        fetch(`http://${server_ip}/delete_dry_name/`, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                selectNum: selectNum,
                dryerNumber: dryer_number,
            }),
        })
            .then(() => setDelModalVisible(false));
    };

    const modifyDryName = (text: string, valiInput: boolean) => {
        if (valiInput && text !== null) {
            fetch(`http://${server_ip}/modify_dry_name/`, {
                method: 'PATCH',
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    selectNum: selectMenuNumber,
                    inputName: text,
                    dryerNumber: dryer_number,
                }),
            })
                .then(() => setModifyModalVisible(false));
        } else {
            Alert.alert("공백포함 6자이내를 확인해주세요.");
        }
    };


    const onPress = (key: number) => {
        setSelectedButton(key)
    }

    useEffect(() => {
        if (delModalVisible === false && modifyModalVisible === false && addModalVisible === false) {
            fetch(`http://${server_ip}/get_dry_menulist?dryer_number=${dryer_number}`)
                .then((response) => response.json())
                .then((drylist) => {
                    const menuList = Array.from(drylist, (item: any) => ({
                        dry_number: item[0],
                        product_name: item[1],
                        modify_date: item[2],
                    }));
                    setMenuList(menuList);
                    if (selectMenuNumber === 0) {
                        setSelectMenuNumber(menuList[0].dry_number);
                    }
                })
        };
    }, [addModalVisible, delModalVisible, modifyModalVisible, dryer_number]);

    useEffect(() => {
        const selectedItem = menuList[startIndex + selectedButton];
        if (selectedItem) {
            setSelectMenuNumber(selectedItem.dry_number);
        }
    }, [selectedButton, startIndex]);

    const changeButton = (type: string) => {
        if (type === 'plus') {
            if (selectedButton < menuList.length - (menuList.length - (maxItems - 1))) {
                setSelectedButton((prev) => prev + 1);
            }
            else {
                setStartIndex((prev) => Math.min(prev + 1, menuList.length - maxItems));
            }
        } else if (type === 'minus') {
            if (selectedButton > 0) {
                setSelectedButton((prev) => prev - 1);
            }
            else {
                setStartIndex((prev) => Math.max(0, prev - 1));
            }
        }
    };



    const maxItems = 3;
    return (
        <View style={styles.bigBox}>
            <View style={styles.menuBox}>
                <DeleteButton
                    isvisible={delModalVisible}
                    closeFn={() => toggleModal('delete')}
                    deleteFn={() => performDryNameAction('delete', "null")}
                />
                <ModifyModal
                    isvisible={modifyModalVisible}
                    closeFn={() => toggleModal('modify')}
                    modifyFn={(text, valiInput) => performDryNameAction('modify', text, valiInput)}
                />
                <AddModal
                    isvisible={addModalVisible}
                    closeFn={() => toggleModal('add')}
                    addFn={(text, valiInput) => performDryNameAction('add', text, valiInput)}
                />
                <TouchableOpacity onPress={() => changeButton('minus')} style={styles.button}>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtn.png')} resizeMode="contain" />
                </TouchableOpacity>
                <View style={styles.menuMiddle}>
                    {menuList.slice(startIndex, startIndex + maxItems).map((item, idx) => (
                        <TouchableOpacity key={item.dry_number} onPress={() => { onPress(idx); setSelectMenuNumber(item.dry_number); }} onLongPress={() => { onPress(idx); setSelectMenuNumber(item.dry_number); setDelModalVisible(true); }} style={selectedButton === idx ? styles.menuBtnAct : styles.menuBtn}>
                            <View style={styles.menulist}>
                                <Text style={selectedButton === idx ? styles.listText1 : styles.listText}>{item.product_name}</Text>
                            </View>
                            <TouchableOpacity style={{ marginTop: '35%', width: '2%' }} onPress={() => { onPress(idx); setSelectMenuNumber(item.dry_number); setModifyModalVisible(true); }} >
                                <Image style={{ height: 15, width: 15 }} source={require('../../public/images/content/create_24px.png')} resizeMode="cover" />
                            </TouchableOpacity>
                        </TouchableOpacity>
                    ))}
                    <TouchableOpacity style={styles.addMenu} onPress={() => setAddModalVisible(true)}>
                        <Image style={{ height: '35%' }} source={require('../../public/images/addRecipe.png')} resizeMode="contain" />
                    </TouchableOpacity>
                </View>
                <TouchableOpacity onPress={() => changeButton('plus')} style={styles.button}>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtnR.png')} resizeMode="contain" />
                </TouchableOpacity>
            </View>
            <RecipeDetailSetting select={selectMenuNumber} />
        </View>
    );
})
const styles = StyleSheet.create({
    bigBox: {
        // borderWidth: 1,
        height: '75%',
        alignItems: 'center'
    },
    menuBox: {
        // borderWidth: 1,
        height: '25%',
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
        marginRight: 25,
        marginLeft: 5,
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
        marginRight: 22,
        marginLeft: 5,
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
    },
    addMenu: {
        borderWidth: 1,
        width: 75,
        height: 95,
        marginTop: 12,
        borderRadius: 5,
        borderStyle: 'dashed',
        borderColor: '#E6E6E6',
        backgroundColor: 'rgba(239, 234, 255, 0.43)',
        alignItems: 'center',
        justifyContent: 'center'
    }
})
export default RecipeList;