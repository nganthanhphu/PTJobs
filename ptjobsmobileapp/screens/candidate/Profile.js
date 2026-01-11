import React, { useState } from "react";
import { View, ScrollView, StyleSheet } from "react-native";
import {
    Appbar,
    Avatar,
    Card,
    Text,
    SegmentedButtons,
} from "react-native-paper";
import { useNavigation } from "@react-navigation/native";

const Profile = () => {
    const navigation = useNavigation();
    const [value, setValue] = useState("cv");

    const user = {
        name: "Hoàng Phi Hùng",
        dob: "25/02/2005",
        address: "Tam Hung Ward, Ho Chi Minh City",
        avatar: "https://via.placeholder.com/150",
    };

    const renderContent = () => {
        switch (value) {
            case "cv":
                return (
                    <Text variant="bodyLarge">
                        Nội dung CV của Hùng hiển thị ở đây...
                    </Text>
                );
            case "jobs":
                return (
                    <Text variant="bodyLarge">
                        Danh sách các công việc đã ứng tuyển...
                    </Text>
                );
            case "following":
                return (
                    <Text variant="bodyLarge">
                        Các công ty đang theo dõi...
                    </Text>
                );
            case "info":
                return (
                    <Text variant="bodyLarge">
                        Thông tin chi tiết cá nhân...
                    </Text>
                );
            default:
                return null;
        }
    };

    return (
        <View style={styles.screen}>
            <Appbar.Header elevated>
                <Appbar.Content
                    title="PTJobs - Hồ sơ"
                    titleStyle={styles.appbarTitle}
                />
                <Appbar.Action
                    icon="bell-outline"
                    onPress={() => navigation.navigate("Notifications")}
                />
                <Appbar.Action
                    icon="account-circle-outline"
                    onPress={() => {}}
                />
            </Appbar.Header>
            <Card style={styles.profileCard}>
                <Card.Content style={styles.cardContentRow}>
                    <Avatar.Image size={80} source={{ uri: user.avatar }} />
                    <View style={styles.userInfo}>
                        <Text variant="headlineSmall" style={styles.userName}>
                            {user.name}
                        </Text>
                        <Text variant="bodyMedium" style={styles.userSubInfo}>
                            {user.dob}
                        </Text>
                        <Text variant="bodyMedium" style={styles.userSubInfo}>
                            {user.address}
                        </Text>
                    </View>
                </Card.Content>
            </Card>

            <View style={styles.tabContainer}>
                <SegmentedButtons
                    value={value}
                    onValueChange={setValue}
                    buttons={[
                        { value: "cv", label: "CV" },
                        { value: "jobs", label: "Việc làm" },
                        { value: "following", label: "Theo dõi" },
                        { value: "info", label: "Thông tin" },
                    ]}
                    density="small"
                />
            </View>
            <ScrollView contentContainerStyle={styles.scrollContent}>
                <Card style={styles.contentCard}>
                    <Card.Content>{renderContent()}</Card.Content>
                </Card>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: "#f5f5f5",
    },
    appbarTitle: {
        fontWeight: "bold",
        fontSize: 20,
    },
    scrollContent: {
        padding: 16,
    },
    profileCard: {
        marginBottom: 20,
        elevation: 2,
        borderRadius: 12,
        backgroundColor: "#fff",
    },
    cardContentRow: {
        flexDirection: "row",
        alignItems: "center",
        paddingVertical: 16,
    },
    userInfo: {
        marginLeft: 20,
        flex: 1,
    },
    userName: {
        fontWeight: "bold",
        marginBottom: 4,
    },
    userSubInfo: {
        color: "#6b7280",
        marginTop: 2,
    },
    tabContainer: {
        marginBottom: 16,
    },
    contentCard: {
        minHeight: 300,
        elevation: 1,
        borderRadius: 12,
        backgroundColor: "#fff",
        paddingVertical: 10,
    },
});

export default Profile;
