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
import CandidateCard from "../../components/CandidateCard.js";

const Home = () => {
    const navigation = useNavigation();
    const [searchQuery, setSearchQuery] = useState("");

    const mockCandidates = [
        {
            id: 1,
            name: "Lê Văn Hùng",
            gender: "Nam",
            applyJob: "Nhân viên phục vụ",
            avatar: "https://via.placeholder.com/150",
        },
        {
            id: 2,
            name: "Trần Thị Ngọc",
            gender: "Nữ",
            applyJob: "Thu ngân",
            avatar: "https://via.placeholder.com/150",
        },
        {
            id: 3,
            name: "Nguyễn Minh Tuấn",
            gender: "Nam",
            applyJob: "Bảo vệ ca đêm",
            avatar: "https://via.placeholder.com/150",
        },
    ];

    return (
        <View style={styles.screen}>
            <Appbar.Header style={styles.appbar}>
                <Appbar.Content
                    title="PTJobs - Nhà tuyển dụng"
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
                    onPress={() => navigation.navigate("CompanyProfile")}
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
                                icon="briefcase-account"
                                style={{ backgroundColor: "#e0f2fe" }}
                                color="#0284c7"
                            />
                            <View style={{ flex: 1 }}>
                                <Text
                                    variant="titleMedium"
                                    style={{ fontWeight: "bold" }}
                                >
                                    Xin chào, Jollibee VN
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
                            Hồ sơ mới nhận
                        </Text>
                    </View>

                    {mockCandidates.map((candidate) => (
                        <CandidateCard
                            key={candidate.id}
                            candidate={candidate}
                            onPress={() =>
                                console.log(
                                    "Xem chi tiết ứng viên:",
                                    candidate.id
                                )
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
        color: "#2563eb",
        fontWeight: "600",
    },
});

export default Home;
