import React, { useState } from 'react';
import {
  View,
  Text,
  TouchableOpacity,
  TextInput,
  Modal,
  StyleSheet,
  KeyboardAvoidingView
} from 'react-native';

interface propsType {
  isvisible: boolean;
  closeFn: () => void;
  select: number;
}

const AddModal = (props: propsType) => {

  const [addInputValue, setAddInputValue] = useState('');
  const [valiInput, setValiInput] = useState<boolean>(true);
  
  const validateInput = (input:string) => {
    const trimmedInput = input.trim();
    const length = trimmedInput.length;
    return length <= 6;
  }



  return (
    <View>
        <Modal visible={props.isvisible} animationType="fade" transparent>
            <View style={styles.modalContainer}>
                <View style={styles.modalInner}>
                    <Text style={styles.modalTitle}>신규레시피입력</Text>
                    <TextInput
                    style={styles.input}
                    value={addInputValue}
                    onChangeText={(text) => setAddInputValue(text)}
                    placeholder="입력하세요"
                    />
                    <View style={{flexDirection:'row'}}>
                        <TouchableOpacity style={styles.submitButton} onPress={()=>{}}>
                        <Text style={styles.text1}>입력 완료</Text>
                        </TouchableOpacity>
                        <TouchableOpacity style={styles.closeButton} onPress={props.closeFn}>
                        <Text style={styles.text1}>닫기</Text>
                        </TouchableOpacity>
                    </View>
                </View>
            </View>
        </Modal>
    </View>
  )
}

export default AddModal

const styles = StyleSheet.create({
    text1: {
        color: '#fff'
    },
    submitButton: {
        backgroundColor: '#753CEF',
        width: 80,
        height: 40, 
        marginRight: 20,
        justifyContent: 'center',
        alignItems: 'center'
    },  
    closeButton: {
        backgroundColor: '#753CEF',
        width: 80,
        height: 40, 
        marginRight: 20,
        justifyContent: 'center',
        alignItems: 'center'
    },  
    input: {
        borderRadius: 10,
        borderBottomColor: 'black',
        borderWidth: 1,
    },
    modalInner: {
        backgroundColor: '#fff',
        width: '30%',
    },

    modalContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
    },
    modalBox: {
      width: '100%',
      backgroundColor: '#fff',
      padding: 16,
      borderRadius: 8,
    },
    modalTitle: {
      fontSize: 24,
      fontWeight: 'bold',
      marginBottom: 8,
    },
    modalMessage: {
      fontSize: 16,
      marginBottom: 16,
    },
    modalButtonContainer: {
      flexDirection: 'row',
      justifyContent: 'flex-end',
      marginTop: 16,
    },
    modalButton: {
      paddingHorizontal: 16,
      paddingVertical: 8,
      borderRadius: 4,
      backgroundColor: '#753CEF',
      marginLeft: 16,
    },
    text: {
      color:"#fff",
      fontSize:20
    },
  });