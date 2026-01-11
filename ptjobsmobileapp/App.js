import React from "react";
import CandidateTabNavigator from "./navigation/CandidateTabNavigator";
import CompanyTabNavigator from "./navigation/CompanyTabNavigator";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import JobDetail from './screens/common/JobDetail';
import CompanyDetail from "./screens/common/CompanyDetail";
import Notifications from "./screens/common/Notifications";
import PostDetail from "./screens/common/PostDetail";

const Stack = createNativeStackNavigator();

const App = () => {
    return (
        // <NavigationContainer>
        //     <Stack.Navigator screenOptions={{ headerShown: false }}>
        //         <Stack.Screen name="MainTabs" component={CandidateTabNavigator} />
        //         <Stack.Screen name="JobDetail" component={JobDetail} options={{ headerShown: false, title: 'Chi tiết tin tuyển dụng' }} />
        //         <Stack.Screen name="CompanyDetail" component={CompanyDetail} options={{ headerShown: false, title: 'Chi tiết Nhà tuyển dụng' }} />
        //         <Stack.Screen name="Notifications" component={Notifications} options={{ headerShown: false, title: 'Thông báo' }} />
        //     </Stack.Navigator>
        // </NavigationContainer>

        <NavigationContainer>
            <Stack.Navigator screenOptions={{ headerShown: false }}>
                <Stack.Screen name="CompanyTabs" component={CompanyTabNavigator} />
                <Stack.Screen name="Notifications" component={Notifications} options={{ headerShown: false, title: 'Thông báo' }} />
                <Stack.Screen name="PostDetail" component={PostDetail} options={{ headerShown: false, title: 'Chi tiết bài đăng' }} />
                <Stack.Screen name="JobDetail" component={JobDetail} options={{ headerShown: false }} />
            </Stack.Navigator>
        </NavigationContainer>
    );
};

export default App;
