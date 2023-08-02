import * as React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import MyDrawer from './front/src/sideMenu/MyDrawer'
import store from './front/src/reduxT/store';
import { Provider } from 'react-redux';


export default function App() {
  return (
    <Provider store={store}>
      <NavigationContainer>
        <MyDrawer />
      </NavigationContainer>
    </Provider>
  );
}