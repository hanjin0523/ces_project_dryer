import React, { useState, useCallback } from 'react';
import { View, Text, Modal, StyleSheet, TouchableOpacity } from 'react-native';
import colors from "../../public/colors/colors";

interface propsType {
  isvisible: boolean;
  closeFn: () => void;
  deleteFn: () => void;
}

const DeleteButton = (props: propsType) => {

  return (
    <View>
      <Modal visible={props.isvisible} transparent>
        <View style={styles.modalContainer}>
          <View style={styles.modalBox}>
            <Text style={styles.modalTitle}>레시피 삭제</Text>
            <Text style={styles.modalMessage}>정말 레시피를 삭제 하시겠습니까?(삭제시 복구가 불가능합니다)</Text>

            <View style={styles.modalButtonContainer}>
              <TouchableOpacity style={styles.modalButton} onPress={props.deleteFn}>
                <Text style={styles.text}>네.삭제해주세요</Text>
              </TouchableOpacity>

              <TouchableOpacity style={styles.modalButtonCancel} onPress={props.closeFn}>
                <Text style={styles.text1}>취소</Text>
              </TouchableOpacity>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
};
export default DeleteButton;

const styles = StyleSheet.create({
  text: {
    color: "#fff",
    fontSize: 18
  },
  text1: {
    color: "#B5B3B9",
    fontSize: 20
  },
  modalContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
  },
  modalBox: {
    width: '25%',
    backgroundColor: '#fff',
    padding: 16,
    borderRadius: 8,
  },
  modalTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: colors.black,
    marginBottom: 8,
    textAlign: 'center'
  },
  modalMessage: {
    fontSize: 16,
    marginBottom: 16,
    color: colors.black,
  },
  modalButtonContainer: {
    flexDirection: 'row-reverse',
    justifyContent: 'flex-end',
    marginTop: 16,
  },
  modalButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 4,
    backgroundColor: '#753CEF',
    marginLeft: 16,
    height: '100%'
  },
  modalButtonCancel: {
    backgroundColor: '#FFFFFF',
    borderWidth: 2,
    borderColor: '#B5B3B9',
    borderRadius: 5,
    width: '45%',
    justifyContent:'center',
    alignItems: 'center'
  },
  modalButtonText: {
    color: '#B5B3B9',
    fontSize: 16,
    fontWeight: 'bold',
  },
});
