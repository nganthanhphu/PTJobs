import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { Ionicons } from "@expo/vector-icons";
import Home from "../screens/company/Home";
import Posts from "../screens/company/Posts";
import Chat from "../screens/common/Chat";
import Profile from "../screens/company/Profile";

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
                name="Posts"
                component={Posts}
                options={{
                    title: "Tin tuyển dụng",
                    headerShown: false,
                    tabBarIcon: ({ color, size }) => (
                        <Ionicons name="newspaper-outline" color={color} size={size} />
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
                        <Ionicons
                            name="chatbubbles"
                            color={color}
                            size={size}
                        />
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
