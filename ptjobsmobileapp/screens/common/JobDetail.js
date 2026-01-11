import React, { useState } from "react";
import { View, ScrollView, StyleSheet } from "react-native";
import {
    Appbar,
    Avatar,
    Text,
    Button,
    SegmentedButtons,
    Chip,
    Divider,
    Card,
} from "react-native-paper";

const JobDetail = ({ route, navigation }) => {
    const job = {
        title: "Nhân viên thu ngân",
        company: "Jollibee VN",
        location: "Tan Phong Ward",
        salary: "35K/h",
        deadline: "15/01/2026",
        logo: "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Jollibee_2011_logo.svg/1200px-Jollibee_2011_logo.svg.png",
    };

    const [tabValue, setTabValue] = useState("detail");

    const renderContent = () => {
        switch (tabValue) {
            case "detail":
                return (
                    <View>
                        <Text
                            variant="titleMedium"
                            style={styles.sectionHeader}
                        >
                            Mô tả công việc
                        </Text>
                        <Text style={styles.textContent}>
                            - Thực hiện thanh toán cho khách hàng.{"\n"}- Kiểm
                            tra tiền mặt và báo cáo doanh thu cuối ca.{"\n"}-
                            Giữ gìn vệ sinh khu vực quầy thu ngân.{"\n"}- Hỗ trợ
                            các bộ phận khác khi cửa hàng đông khách.
                        </Text>

                        <Text
                            variant="titleMedium"
                            style={styles.sectionHeader}
                        >
                            Yêu cầu
                        </Text>
                        <Text style={styles.textContent}>
                            - Sinh viên năm 1, 2 có thể làm xoay ca.{"\n"}-
                            Trung thực, nhanh nhẹn, cẩn thận.{"\n"}- Có kinh
                            nghiệm thu ngân là một lợi thế.
                        </Text>
                    </View>
                );
            case "review":
                return (
                    <View style={styles.placeholderBox}>
                        <Text
                            style={{
                                textAlign: "center",
                                color: "#666",
                                marginTop: 8,
                            }}
                        >
                            "Môi trường làm việc thân thiện, quản lý dễ tính..."
                        </Text>
                    </View>
                );
            case "company":
                return (
                    <View style={styles.placeholderBox}>
                        <Text variant="bodyLarge">
                            Giới thiệu về Jollibee VN...
                        </Text>
                    </View>
                );
            default:
                return null;
        }
    };

    return (
        <View style={styles.screen}>
            <Appbar.Header elevated style={styles.appbar}>
                <Appbar.BackAction onPress={() => navigation?.goBack()} />
                <Appbar.Content
                    title="Chi tiết tin tuyển dụng"
                    titleStyle={styles.headerTitle}
                />
            </Appbar.Header>

            <ScrollView
                contentContainerStyle={styles.scrollContent}
                showsVerticalScrollIndicator={false}
            >
                <Card style={styles.infoCard}>
                    <Card.Content>
                        <View style={styles.headerRow}>
                            <Avatar.Image
                                size={70}
                                source={{ uri: job.logo }}
                                style={styles.logo}
                            />
                            <View style={styles.infoCol}>
                                <Text
                                    variant="titleLarge"
                                    style={styles.jobTitle}
                                >
                                    {job.title}
                                </Text>
                                <Text
                                    variant="bodyMedium"
                                    style={styles.companyName}
                                >
                                    {job.company} - {job.location}
                                </Text>
                                <View style={styles.metaRow}>
                                    <Text
                                        variant="titleMedium"
                                        style={styles.salary}
                                    >
                                        {job.salary}
                                    </Text>
                                    <View style={styles.deadlineBadge}>
                                        <Text style={styles.deadlineText}>
                                            {job.deadline}
                                        </Text>
                                    </View>
                                </View>
                            </View>
                        </View>
                    </Card.Content>
                </Card>

                <View style={styles.tabContainer}>
                    <SegmentedButtons
                        value={tabValue}
                        onValueChange={setTabValue}
                        buttons={[
                            { value: "detail", label: "Chi tiết" },
                            { value: "review", label: "Đánh giá" },
                            { value: "company", label: "Công ty" },
                        ]}
                        density="medium"
                        style={styles.tabs}
                    />
                </View>

                <View style={styles.contentContainer}>{renderContent()}</View>
            </ScrollView>

            <View style={styles.footer}>
                <Button
                    mode="contained"
                    onPress={() => console.log("Applied!")}
                    style={styles.applyButton}
                    contentStyle={{ height: 50 }}
                    labelStyle={{ fontSize: 18, fontWeight: "bold" }}
                >
                    Apply Now!
                </Button>
            </View>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: "#f8f9fa",
    },
    appbar: {
        backgroundColor: "#fff",
    },
    headerTitle: {
        fontSize: 18,
        fontWeight: "bold",
    },
    scrollContent: {
        paddingBottom: 100,
    },
    infoCard: {
        margin: 16,
        borderRadius: 16,
        backgroundColor: "#fff",
        elevation: 2,
    },
    headerRow: {
        flexDirection: "row",
        alignItems: "flex-start",
    },
    logo: {
        backgroundColor: "transparent",
        marginRight: 16,
    },
    infoCol: {
        flex: 1,
        justifyContent: "center",
    },
    jobTitle: {
        fontWeight: "bold",
        fontSize: 20,
        marginBottom: 4,
        color: "#1f2937",
    },
    companyName: {
        color: "#6b7280",
        marginBottom: 8,
    },
    metaRow: {
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-between",
        marginTop: 4,
    },
    salary: {
        color: "#059669",
        fontWeight: "bold",
        fontSize: 18,
    },
    deadlineBadge: {
        borderWidth: 1,
        borderColor: "#374151",
        paddingHorizontal: 8,
        paddingVertical: 4,
        borderRadius: 6,
        transform: [{ rotate: "-2deg" }],
    },
    deadlineText: {
        fontSize: 12,
        fontWeight: "600",
        color: "#374151",
    },
    tabContainer: {
        paddingHorizontal: 16,
        marginBottom: 16,
    },
    tabs: {
        backgroundColor: "#fff",
    },
    contentContainer: {
        paddingHorizontal: 16,
        paddingBottom: 20,
        minHeight: 200,
    },
    sectionHeader: {
        fontWeight: "bold",
        marginTop: 16,
        marginBottom: 8,
        color: "#111",
    },
    textContent: {
        lineHeight: 24,
        color: "#4b5563",
        fontSize: 15,
        textAlign: "justify",
    },
    placeholderBox: {
        padding: 20,
        alignItems: "center",
        justifyContent: "center",
        backgroundColor: "#eee",
        borderRadius: 8,
        marginTop: 10,
    },
    footer: {
        position: "absolute",
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: "#fff",
        padding: 16,
        elevation: 8,
        borderTopWidth: 1,
        borderTopColor: "#e5e7eb",
    },
    applyButton: {
        borderRadius: 30,
        backgroundColor: "#1f2937",
    },
});

export default JobDetail;
