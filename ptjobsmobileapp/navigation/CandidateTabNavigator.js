import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import Home from '../screens/candidate/Home';
import Jobs from '../screens/candidate/Jobs';
import Companys from '../screens/candidate/Companies';
import Chat from '../screens/common/Chat';
import Profile from '../screens/candidate/Profile';

const Tab = createBottomTabNavigator();

const CandidateTabNavigator = () => {
    return (
        <Tab.Navigator>
            <Tab.Screen
                name="Home"
                component={Home}
                options={{
                    title: "Trang chủ",
                    headerShown: false,
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="home" color={color} size={size} />
                    ),
                }}
            />
            <Tab.Screen
                name="Jobs"
                component={Jobs}
                options={{
                    title: "Tìm việc",
                    headerShown: false,
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="search" color={color} size={size} />
                    ),
                }}
            />
            <Tab.Screen
                name="Companys"
                component={Companys}
                options={{
                    title: "Công ty",
                    headerShown: false,
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="business" color={color} size={size} />
                    ),
                }}
            />
            <Tab.Screen
                name="Chat"
                component={Chat}
                options={{
                    title: "Tin nhắn",
                    headerShown: false,
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="chatbubbles" color={color} size={size} />
                    ),
                }}
            />
            <Tab.Screen
                name="Profile"
                component={Profile}
                options={{
                    title: "Hồ sơ",
                    headerShown: false,
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="person" color={color} size={size} />
                    ),
                }}
            />
        </Tab.Navigator>
    );
};

export default CandidateTabNavigator;
