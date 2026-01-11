import React, { useState } from "react";
import { View, ScrollView, StyleSheet, Image } from "react-native";
import {
    Appbar,
    Avatar,
    Card,
    Text,
    SegmentedButtons,
    Chip,
    Divider,
    List,
    Button,
} from "react-native-paper";

const CandidateDetail = ({ navigation, route }) => {
    const { candidateId } = route.params || {};
    const [tabValue, setTabValue] = useState("cv");

    const candidate = {
        id: candidateId || 1,
        name: "Hoàng Phi Hùng",
        dob: "25/02/2005",
        phone: "0706 823 664",
        email: "hung.hoang@student.ou.edu.vn",
        gender: "Nam",
        avatar: "https://via.placeholder.com/150",
        address: "Go Vap Dist, HCMC",
        intro: "Sinh viên năm 3 Khoa học máy tính. Nhanh nhẹn, trung thực, có xe máy riêng. Mong muốn tìm việc làm thêm trang trải học phí.",
        skills: [
            "Tiếng Anh (Cơ bản)",
            "Tin học văn phòng",
            "Giao tiếp tốt",
            "Chịu khó",
        ],
        education: "Đại học Mở TP.HCM (2023 - Nay)",
    };

    const workHistory = [
        {
            id: 1,
            title: "Phục vụ bàn",
            company: "KFC Quang Trung",
            duration: "3 tháng",
            desc: "Order món, dọn dẹp vệ sinh.",
        },
        {
            id: 2,
            title: "Shipper",
            company: "ShopeeFood",
            duration: "6 tháng",
            desc: "Giao hàng khu vực Gò Vấp.",
        },
    ];

    const reviews = [
        {
            id: 1,
            employer: "KFC Quang Trung",
            rating: 5,
            comment: "Hùng làm việc rất chăm chỉ, đi làm đúng giờ.",
        },
        {
            id: 2,
            employer: "Cafe Mộc",
            rating: 4,
            comment: "Nhiệt tình nhưng đôi khi còn quên order.",
        },
    ];

    const renderCVTab = () => (
      <View style={styles.tabContent}>
        <Text>Hiển thị pdf</Text>
        </View>
    );

    const renderReviewTab = () => (
        <View style={styles.tabContent}>
            {reviews.map((rv) => (
                <Card key={rv.id} style={styles.reviewCard}>
                    <Card.Content>
                        <View style={styles.reviewHeader}>
                            <Avatar.Icon
                                size={40}
                                icon="store"
                                style={{ backgroundColor: "#e0f2fe" }}
                                color="#0284c7"
                            />
                            <View style={{ marginLeft: 12, flex: 1 }}>
                                <Text style={{ fontWeight: "bold" }}>
                                    {rv.employer}
                                </Text>
                            </View>
                        </View>
                        <Text style={styles.reviewComment}>"{rv.comment}"</Text>
                    </Card.Content>
                </Card>
            ))}
        </View>
    );

    const renderHistoryTab = () => (
        <View style={styles.tabContent}>
            {workHistory.map((job, index) => (
                <View key={job.id}>
                    <List.Item
                        title={job.title}
                        description={`${job.company} • ${job.duration}\n${job.desc}`}
                        descriptionNumberOfLines={3}
                        left={(props) => (
                            <List.Icon
                                {...props}
                                icon="briefcase-clock-outline"
                            />
                        )}
                    />
                    {index < workHistory.length - 1 && <Divider />}
                </View>
            ))}
        </View>
    );

    return (
        <View style={styles.screen}>
            <Appbar.Header style={styles.appbar}>
                <Appbar.BackAction onPress={() => navigation.goBack()} />
                <Appbar.Content
                    title="Chi tiết ứng viên"
                    titleStyle={styles.headerTitle}
                />
            </Appbar.Header>

            <ScrollView
                contentContainerStyle={styles.scrollContent}
                showsVerticalScrollIndicator={false}
            >
                <Card style={styles.identityCard}>
                    <Card.Content>
                        <View style={styles.identityRow}>
                            <Avatar.Image
                                size={80}
                                source={{ uri: candidate.avatar }}
                            />

                            <View style={styles.identityInfo}>
                                <Text
                                    variant="titleLarge"
                                    style={styles.nameText}
                                >
                                    {candidate.name}
                                </Text>
                                <Text
                                    variant="bodyMedium"
                                    style={styles.infoText}
                                >
                                    {candidate.dob}
                                </Text>
                                <Text
                                    variant="bodyMedium"
                                    style={styles.phoneText}
                                >
                                    {candidate.phone}
                                </Text>
                            </View>

                            <View style={styles.genderBox}>
                                <Text style={styles.genderText}>
                                    {candidate.gender}
                                </Text>
                            </View>
                        </View>
                    </Card.Content>
                </Card>

                {/* Tabs */}
                <View style={styles.tabContainer}>
                    <SegmentedButtons
                        value={tabValue}
                        onValueChange={setTabValue}
                        buttons={[
                            { value: "cv", label: "CV" },
                            { value: "review", label: "Đánh giá" },
                            { value: "history", label: "Công việc" },
                        ]}
                        density="medium"
                    />
                </View>

                <Card style={styles.contentCard}>
                    <Card.Content>
                        {tabValue === "cv" && renderCVTab()}
                        {tabValue === "review" && renderReviewTab()}
                        {tabValue === "history" && renderHistoryTab()}
                    </Card.Content>
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
    appbar: {
        backgroundColor: "#fff",
        elevation: 0,
    },
    headerTitle: {
        fontWeight: "bold",
        fontSize: 18,
    },
    scrollContent: {
        padding: 16,
    },
    identityCard: {
        marginBottom: 16,
        backgroundColor: "#fff",
        borderRadius: 12,
        elevation: 2,
    },
    identityRow: {
        flexDirection: "row",
        alignItems: "flex-start",
    },
    identityInfo: {
        flex: 1,
        marginLeft: 16,
        paddingRight: 8,
    },
    nameText: {
        fontWeight: "bold",
        fontSize: 20,
        marginBottom: 4,
    },
    infoText: {
        color: "#4b5563",
        fontSize: 15,
    },
    phoneText: {
        fontWeight: "bold",
        fontSize: 16,
        marginTop: 4,
        color: "#1f2937",
    },
    genderBox: {
        borderWidth: 1.5,
        borderColor: "#1f2937",
        paddingHorizontal: 8,
        paddingVertical: 2,
        borderRadius: 4,
        backgroundColor: "#fff",
    },
    genderText: {
        fontWeight: "bold",
        fontSize: 12,
    },
    tabContainer: {
        marginBottom: 16,
    },
    contentCard: {
        backgroundColor: "#fff",
        borderRadius: 12,
        minHeight: 300,
        elevation: 1,
    },
    tabContent: {
        paddingVertical: 8,
    },
    sectionTitle: {
        fontWeight: "bold",
        marginBottom: 8,
        color: "#1f2937",
    },
    textContent: {
        lineHeight: 22,
        color: "#4b5563",
        textAlign: "justify",
    },
    divider: {
        marginVertical: 16,
    },
    chipContainer: {
        flexDirection: "row",
        flexWrap: "wrap",
        gap: 8,
    },
    skillChip: {
        backgroundColor: "#f3f4f6",
    },
    footerActions: {
        flexDirection: "row",
        gap: 12,
        marginTop: 24,
    },
    reviewCard: {
        marginBottom: 12,
        backgroundColor: "#f9fafb",
        elevation: 0,
        borderWidth: 1,
        borderColor: "#e5e7eb",
    },
    reviewHeader: {
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 8,
    },
    reviewComment: {
        fontStyle: "italic",
        color: "#4b5563",
    },
});

export default CandidateDetail;