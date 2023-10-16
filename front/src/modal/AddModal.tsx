import React, { useState, useCallback, useMemo } from 'react';
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
  addFn: (text: string, valiInput: boolean) => void;
  closeFn: () => void;
}

const AddModal = (props: propsType) => {

  const [inputValue, setInputValue] = useState('');
  const [valiInput, setValiInput] = useState<boolean>(true);

  const handleInputChange = useCallback((text: string) => {
    setInputValue(text);
    setValiInput(validateInput(text));
  }, []);

  const validateInput = (input: string) => {
    const trimmedInput = input.trim();
    const length = trimmedInput.length;
    return length <= 6;
  }


  return (
    <KeyboardAvoidingView  style={{height:200}} behavior="position" enabled>
      <View>
        <Modal visible={props.isvisible} animationType="fade" transparent>
          <View style={styles.modalContainer}>
            <View style={styles.modalInner}>
              <Text style={styles.modalTitle}>신규레시피입력</Text>
              <TextInput
                style={valiInput ? styles.input1 : styles.input}
                value={inputValue}
                onChangeText={handleInputChange}
                placeholder="레시피 이름을 입력하세요"
                placeholderTextColor="#DFDFDF"
              />
              <Text style={valiInput ? styles.subText1 : styles.subText}>공백포함 6자이내로 입력</Text>
              <View style={styles.modalButtonContainer}>
                <TouchableOpacity style={styles.submitButton} onPress={()=>{props.addFn(inputValue,valiInput); setInputValue('')}}>
                  <Text style={styles.text1}>입력 완료</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.closeButton} onPress={props.closeFn}>
                  <Text style={styles.text}>닫기</Text>
                </TouchableOpacity>
              </View>
            </View>
          </View>
        </Modal>
      </View>
    </KeyboardAvoidingView>
  )
}

export default AddModal

const styles = StyleSheet.create({
  subText: {
    marginLeft: 20,
    marginTop: 5,
    fontSize: 16,
    color: '#B3261E'
  },
  subText1: {
    marginLeft: 20,
    marginTop: 5,
    fontSize: 16,
    color: '#5C5C5C'
  },
  text1: {
    color: '#fff',
    fontSize: 20
  },
  submitButton: {
    borderColor: '#753CEF',
    backgroundColor: '#753CEF',
    borderWidth:2,
    borderRadius: 10,
    width: '45%',
    height: '65%',
    marginRight: 20,
    justifyContent: 'center',
    alignItems: 'center'
  },
  closeButton: {
    borderColor: '#B5B3B9',
    borderWidth:2,
    borderRadius: 10,
    width: '45%',
    height: '65%',
    marginRight: 20,
    marginLeft: 20,
    justifyContent: 'center',
    alignItems: 'center'
  },
  input: {
    borderRadius: 10,
    borderColor: '#B3261E',
    borderWidth: 1,
    width: '90%',
    height: '27%',
    marginLeft: 20,
  },
  input1: {
    borderRadius: 10,
    borderColor: '#E5E5E5',
    borderWidth: 1,
    width: '90%',
    height: '27%',
    marginLeft: 20,
  },
  modalInner: {
    backgroundColor: '#fff',
    width: '30%',
    height: '30%',
    marginBottom: '20%',
    justifyContent: 'center',
    borderRadius: 10,
    // alignItems: 'center'
  },

  modalContainer: {
    height: 760,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalBox: {
    width: '100%',
    height: '80%',
    backgroundColor: '#fff',
    borderRadius: 8,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
    color: 'black',
    marginLeft: 20,
  },
  modalMessage: {
    fontSize: 16,
    marginBottom: 16,
  },
  modalButtonContainer: {
    flexDirection: 'row-reverse',
    justifyContent: 'flex-end',
    marginTop: 16,
    marginLeft: 20, 
  },
  modalButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 4,
    backgroundColor: '#753CEF',
    marginLeft: 16,
  },
  text: {
    color: "#B5B3B9",
    fontSize: 20
  },
});