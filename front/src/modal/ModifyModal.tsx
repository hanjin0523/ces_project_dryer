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
import colors from "../../public/colors/colors";

interface propsType {
  isvisible: boolean;
  closeFn: () => void;
}

const ModifyModal = (props: propsType) => {
  const [inputValue, setInputValue] = useState('');



  return (
    <KeyboardAvoidingView style={styles.container} behavior="position" enabled>
    <View>
      <Modal visible={props.isvisible} animationType="fade" transparent>
        <View style={styles.modalContainer}>
          <View style={styles.modalInner}>
            <Text style={styles.modalTitle}>레시피이름변경</Text>
            <TextInput
              style={styles.input}
              value={inputValue}
              onChangeText={(text) => setInputValue(text)}
              placeholder="레시피 이름을 입력하세요"
              placeholderTextColor="#E5E5E5"
            />
            <View style={styles.modalButtonContainer}>
              <TouchableOpacity style={styles.submitButton} onPress={() => { }}>
                <Text style={styles.text1}>입력 완료</Text>
              </TouchableOpacity>
              <TouchableOpacity style={styles.closeButton} onPress={props.closeFn}>
                <Text style={styles.text2}>닫기</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
    </KeyboardAvoidingView>
  );
};
export default ModifyModal;
const styles = StyleSheet.create({
  container: {
    height: 200
  },
  text1: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '700'
  },
  text2: {
    color: '#B5B3B9',
    fontSize: 18,
    fontWeight: '700'
  },
  submitButton: {
    backgroundColor: '#753CEF',
    width: '45%',
    height: '65%',
    marginLeft: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
  },
  closeButton: {
    backgroundColor: '#FFFFFF',
    width: '45%',
    height: '65%',
    marginLeft: 20,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 10,
    borderColor: '#B5B3B9',
    borderWidth: 2,
  },
  input: {
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
    justifyContent: 'center',
    marginTop: '-20%',
    borderRadius: 10,
    // alignItems: 'center',
  },

  modalContainer: {
    // flex: 1,
    height: 760,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalBox: {
    width: '100%',
    height: '90%',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 10,
  },
  modalTitle: {
    fontSize: 27,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 10,
    marginLeft: 20,
  },
  modalMessage: {
    fontSize: 16,
    marginBottom: 16,
  },
  modalButtonContainer: {
    flexDirection: 'row-reverse',
    justifyContent: 'center',
    marginTop: 20,
    marginLeft: 20,
  },
  modalButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 4,
    backgroundColor: '#753CEF',
    marginLeft: 16,
    width: '50%',
    height: '30%'
  },
  text: {
    color: "#fff",
    fontSize: 20
  },
});

