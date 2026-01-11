import React, { createContext, useState, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { API_URL } from '@env';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [userToken, setUserToken] = useState(null);
    const [userRole, setUserRole] = useState(null);
    const [userInfo, setUserInfo] = useState(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        checkLoginStatus();
    }, []);

    const checkLoginStatus = async () => {
        try {
            const token = await AsyncStorage.getItem('userToken');
            const role = await AsyncStorage.getItem('userRole');
            const info = await AsyncStorage.getItem('userInfo');

            if (token) {
                setUserToken(token);
                setUserRole(role);
                setUserInfo(info ? JSON.parse(info) : null);
            }
        } catch (error) {
            console.error('Error checking login status:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const login = async (email, password) => {
        try {
            const response = await axios.post(`${API_URL}/auth/login/`, {
                email,
                password,
            });

            const { token, user } = response.data;
            
            await AsyncStorage.setItem('userToken', token);
            await AsyncStorage.setItem('userRole', user.role);
            await AsyncStorage.setItem('userInfo', JSON.stringify(user));

            setUserToken(token);
            setUserRole(user.role);
            setUserInfo(user);

            return { success: true };
        } catch (error) {
            console.error('Login error:', error);
            return {
                success: false,
                message: error.response?.data?.message || 'Đăng nhập thất bại',
            };
        }
    };

    const register = async (userData) => {
        try {
            const response = await axios.post(`${API_URL}/auth/register/`, userData);

            const { token, user } = response.data;
            
            await AsyncStorage.setItem('userToken', token);
            await AsyncStorage.setItem('userRole', user.role);
            await AsyncStorage.setItem('userInfo', JSON.stringify(user));

            setUserToken(token);
            setUserRole(user.role);
            setUserInfo(user);

            return { success: true };
        } catch (error) {
            console.error('Register error:', error);
            return {
                success: false,
                message: error.response?.data?.message || 'Đăng ký thất bại',
            };
        }
    };

    const logout = async () => {
        try {
            await AsyncStorage.removeItem('userToken');
            await AsyncStorage.removeItem('userRole');
            await AsyncStorage.removeItem('userInfo');

            setUserToken(null);
            setUserRole(null);
            setUserInfo(null);
        } catch (error) {
            console.error('Logout error:', error);
        }
    };

    return (
        <AuthContext.Provider
            value={{
                userToken,
                userRole,
                userInfo,
                isLoading,
                login,
                register,
                logout,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
