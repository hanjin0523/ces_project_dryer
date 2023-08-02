import React, { useState, useEffect } from "react";
import colors from "../../public/colors/colors";
import { StyleSheet, View, Image, Text } from "react-native";
import * as config from '../config';
import { TouchableOpacity } from "react-native-gesture-handler";
import DeleteButton from "../modal/DeleteModal";
import ModifyModal from "../modal/ModifyModal";
import AddModal from "../modal/AddModal";

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

    const deleteModalClose = () => {
        setDelModalVisible(false)
    }
    const modifyModalClose = () => {
        setModifyModalVisible(false)
    }
    const addModalClose = () => {
        setAddModalVisible(false)
    }

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


    const maxItems = 3;
    return (
        <>
            <View style={styles.menuBox}>
                <DeleteButton 
                    isvisible={delModalVisible}
                    closeFn={deleteModalClose} 
                />
                <ModifyModal 
                    isvisible={modifyModalVisible}
                    closeFn={modifyModalClose}
                />
                <AddModal 
                    isvisible={addModalVisible}
                    closeFn={addModalClose}
                    select={selectMenuNumber}
                />
                <TouchableOpacity onPress={minus} style={styles.button}>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtn.png')} resizeMode="contain" />
                </TouchableOpacity>
                <View style={styles.menuMiddle}>
                    {menuList.slice(startIndex, startIndex + maxItems).map((item, idx) => (
                        <TouchableOpacity key={item.dry_number} onPress={() => { onPress(idx); setSelectMenuNumber(item.dry_number); }} onLongPress={() => setDelModalVisible(true)} onPressIn={()=>onPress(idx)} style={selectedButton === idx ? styles.menuBtnAct : styles.menuBtn}>
                            <View style={styles.menulist}>
                                <Text style={selectedButton === idx ? styles.listText1 : styles.listText}>{item.product_name}</Text>
                            </View>
                            <TouchableOpacity style={{ marginTop: '35%', width: '2%'}} onPress={()=>setModifyModalVisible(true)} >
                                <Image source={require('../../public/images/content/create_24px.png')} resizeMode="contain"/>
                            </TouchableOpacity>
                        </TouchableOpacity>
                    ))}
                    <TouchableOpacity style={styles.addMenu} onPress={() => setAddModalVisible(true)}>
                        <Image style={{height: '35%'}} source={require('../../public/images/addRecipe.png')} resizeMode="contain"/>
                    </TouchableOpacity>
                </View>
                <TouchableOpacity onPress={plus} style={styles.button}>
                    <Image style={styles.buttonImg} source={require('../../public/images/listbtnR.png')} resizeMode="contain" />
                </TouchableOpacity>
            </View>
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
        marginRight: 25,
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