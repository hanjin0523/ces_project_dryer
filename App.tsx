import { NavigationContainer } from '@react-navigation/native';
import MyDrawer from './front/src/sideMenu/MyDrawer'
import store from './front/src/reduxT/store';
import { Provider } from 'react-redux';
import React, { useEffect } from 'react';


const App = () => {
  
  useEffect(() => {
    console.log('App.tsx')
  }, [])

  return (
    <Provider store={store}>
      <NavigationContainer>
        <MyDrawer />
      </NavigationContainer>
    </Provider>
  );
}
export default App;
