import React, { useState } from "react";
import { View, ScrollView, StyleSheet } from "react-native";
import {
    Appbar,
    Avatar,
    Card,
    Text,
    Searchbar,
    IconButton,
} from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import JobCard from "../../components/JobCard.js";

const Home = () => {
    const navigation = useNavigation();

    const mockJobs = [
        {
            id: 1,
            title: "Nhân viên tiếp tân",
            salary: "25K/h",
            company: "KFC Quận 3",
            category: "Bán hàng",
            logo: "https://upload.wikimedia.org/wikipedia/en/thumb/5/57/KFC_logo-image.svg/1200px-KFC_logo-image.svg.png",
        },
        {
            id: 2,
            title: "Pha chế (Barista)",
            salary: "30K/h",
            company: "Highlands Coffee",
            category: "F&B",
            logo: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Highlands_Coffee_logo.svg/1200px-Highlands_Coffee_logo.svg.png",
        },
        {
            id: 3,
            title: "Giao hàng Part-time",
            salary: "50K/đơn",
            company: "ShopeeFood",
            category: "Giao vận",
            logo: "https://cdn.haitrieu.com/wp-content/uploads/2021/11/Logo-ShopeeFood-VN.png",
        },
    ];

    return (
        <View style={styles.screen}>
            <Appbar.Header style={styles.appbar}>
                <Appbar.Content
                    title="PTJobs - Trang chủ"
                    titleStyle={styles.appbarTitle}
                />
                <IconButton
                    icon="bell-outline"
                    size={24}
                    onPress={() => navigation.navigate("Notifications")}
                />
                <IconButton
                    icon="account-circle-outline"
                    size={24}
                    onPress={() => navigation.navigate("Profile")}
                />
            </Appbar.Header>

            <ScrollView
                style={styles.container}
                showsVerticalScrollIndicator={false}
            >
                <Card style={styles.greetingCard}>
                    <Card.Content style={styles.cardContent}>
                        <View style={styles.greetingContent}>
                            <Avatar.Icon
                                size={50}
                                icon="account-star"
                                style={{ backgroundColor: "#dcfce7" }}
                                color="#15803d"
                            />
                            <View style={{ flex: 1 }}>
                                <Text
                                    variant="titleMedium"
                                    style={{ fontWeight: "bold" }}
                                >
                                    Xin chào, Phi Hùng
                                </Text>
                            </View>
                        </View>
                    </Card.Content>
                </Card>

                <View style={styles.section}>
                    <View style={styles.sectionHeaderRow}>
                        <Text
                            variant="headlineSmall"
                            style={styles.sectionTitle}
                        >
                            Việc làm đề xuất
                        </Text>
                    </View>

                    {mockJobs.map((job) => (
                        <JobCard
                            key={job.id}
                            job={job}
                            onPress={() =>
                                navigation.navigate("JobDetail", {
                                    jobId: job.id,
                                })
                            }
                        />
                    ))}
                </View>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: "#f5f5f5",
    },
    appbar: {
        backgroundColor: "#fff",
        elevation: 0,
        borderBottomWidth: 1,
        borderBottomColor: "#e5e5e5",
    },
    appbarTitle: {
        fontWeight: "bold",
        fontSize: 18,
    },
    container: {
        flex: 1,
        padding: 15,
    },
    greetingCard: {
        marginBottom: 15,
        elevation: 2,
        borderRadius: 12,
        backgroundColor: "#fff",
    },
    cardContent: {
        paddingVertical: 16,
    },
    greetingContent: {
        flexDirection: "row",
        alignItems: "center",
        gap: 16,
    },
    searchbar: {
        marginBottom: 20,
        elevation: 1,
        backgroundColor: "#fff",
        borderRadius: 10,
    },
    section: {
        marginBottom: 24,
    },
    sectionHeaderRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 12,
    },
    sectionTitle: {
        fontWeight: "bold",
        fontSize: 18,
        color: "#1f2937",
    },
    viewAllText: {
        color: "#059669",
        fontWeight: "600",
    },
});

export default Home;
