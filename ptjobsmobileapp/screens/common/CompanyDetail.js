import React, { useState } from "react";
import { View, ScrollView, StyleSheet, Image, FlatList } from "react-native";
import {
    Appbar,
    Avatar,
    Text,
    SegmentedButtons,
    Card,
    Divider,
    List,
} from "react-native-paper";
import JobCard from "../../components/JobCard.js";

const CompanyDetail = ({ route, navigation }) => {
    const [tabValue, setTabValue] = useState("info");

    const company = {
        name: "Jolibee VN",
        email: "jolibee@mail.com",
        address: "Tam Hiep Ward, HCM City",
        logo: "https://upload.wikimedia.org/wikipedia/en/thumb/8/84/Jollibee_2011_logo.svg/1200px-Jollibee_2011_logo.svg.png",
        description:
            "Jollibee là chuỗi nhà hàng thức ăn nhanh lớn nhất Philippines, hoạt động mạng lưới hơn 1.400 cửa hàng trên toàn thế giới.",
        images: [
            "https://via.placeholder.com/300x200",
            "https://via.placeholder.com/300x200",
            "https://via.placeholder.com/300x200",
        ],
        reviews: [
            {
                id: 1,
                user: "Nguyễn Văn A",
                rating: 5,
                content: "Môi trường thân thiện, sếp vui tính.",
            },
            {
                id: 2,
                user: "Trần Thị B",
                rating: 4,
                content: "Lương ổn, nhưng giờ giấc hơi gắt.",
            },
        ],
    };

    const mockJobs = [
        {
            id: 1,
            title: "Nhân viên phục vụ",
            salary: "25K/h",
            company: "Jollibee VN",
            category: "Phục vụ",
            logo: company.logo,
        },
        {
            id: 2,
            title: "Quản lý cửa hàng",
            salary: "12tr/tháng",
            company: "Jollibee VN",
            category: "Quản lý",
            logo: company.logo,
        },
    ];

    const renderContent = () => {
        switch (tabValue) {
            case "info":
                return (
                    <View style={styles.tabContent}>
                        <Text
                            variant="titleMedium"
                            style={styles.sectionHeader}
                        >
                            Giới thiệu
                        </Text>
                        <Text style={styles.textDescription}>
                            {company.description}
                        </Text>

                        <Divider style={styles.divider} />

                        <Text
                            variant="titleMedium"
                            style={styles.sectionHeader}
                        >
                            Liên hệ
                        </Text>
                        <List.Item
                            title={company.email}
                            left={(props) => (
                                <List.Icon {...props} icon="email-outline" />
                            )}
                        />
                        <List.Item
                            title={company.address}
                            left={(props) => (
                                <List.Icon
                                    {...props}
                                    icon="map-marker-outline"
                                />
                            )}
                        />
                    </View>
                );
            case "images":
                return (
                    <View style={styles.imageContainer}>
                        {company.images.map((img, index) => (
                            <Image
                                key={index}
                                source={{ uri: img }}
                                style={styles.companyImage}
                            />
                        ))}
                    </View>
                );
            case "reviews":
                return (
                    <View style={styles.tabContent}>
                        {company.reviews.map((review) => (
                            <Card key={review.id} style={styles.reviewCard}>
                                <Card.Content>
                                    <View style={styles.reviewHeader}>
                                        <Avatar.Icon size={30} icon="account" />
                                        <Text style={styles.reviewUser}>
                                            {review.user}
                                        </Text>
                                        <Text style={styles.reviewRating}>
                                            ⭐ {review.rating}
                                        </Text>
                                    </View>
                                    <Text style={styles.reviewText}>
                                        "{review.content}"
                                    </Text>
                                </Card.Content>
                            </Card>
                        ))}
                    </View>
                );
            case "jobs":
                return (
                    <View style={styles.tabContent}>
                        {mockJobs.map((job) => (
                            <JobCard key={job.id} job={job} />
                        ))}
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
                    title="Chi tiết NTD"
                    titleStyle={styles.headerTitle}
                />
            </Appbar.Header>

            <ScrollView
                contentContainerStyle={styles.scrollContent}
                showsVerticalScrollIndicator={false}
            >
                <Card style={styles.infoCard}>
                    <Card.Content style={styles.cardContentRow}>
                        <Avatar.Image
                            size={80}
                            source={{ uri: company.logo }}
                            style={styles.avatar}
                        />
                        <View style={styles.infoCol}>
                            <Text
                                variant="headlineSmall"
                                style={styles.companyName}
                            >
                                {company.name}
                            </Text>
                            <Text
                                variant="bodyMedium"
                                style={styles.contactText}
                            >
                                📧 {company.email}
                            </Text>
                            <Text
                                variant="bodyMedium"
                                style={styles.contactText}
                            >
                                📍 {company.address}
                            </Text>
                        </View>
                    </Card.Content>
                </Card>

                <View style={styles.tabContainer}>
                    <SegmentedButtons
                        value={tabValue}
                        onValueChange={setTabValue}
                        buttons={[
                            { value: "info", label: "Thông tin" },
                            { value: "images", label: "Hình ảnh" },
                            { value: "reviews", label: "Đánh giá" },
                            { value: "jobs", label: "Việc làm" },
                        ]}
                        density="small"
                        style={styles.segmentedButton}
                    />
                </View>

                <View style={styles.contentContainer}>{renderContent()}</View>
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
    },
    headerTitle: {
        fontWeight: "bold",
        fontSize: 18,
    },
    scrollContent: {
        paddingBottom: 20,
    },
    infoCard: {
        margin: 16,
        borderRadius: 12,
        backgroundColor: "#fff",
        elevation: 2,
    },
    cardContentRow: {
        flexDirection: "row",
        alignItems: "center",
        paddingVertical: 16,
    },
    avatar: {
        backgroundColor: "transparent",
    },
    infoCol: {
        flex: 1,
        marginLeft: 16,
        justifyContent: "center",
    },
    companyName: {
        fontWeight: "bold",
        marginBottom: 6,
        fontSize: 22,
        color: "#1f2937",
    },
    contactText: {
        color: "#4b5563",
        marginBottom: 2,
        fontSize: 13,
    },
    tabContainer: {
        paddingHorizontal: 16,
        marginBottom: 16,
    },
    segmentedButton: {
        backgroundColor: "#fff",
    },
    contentContainer: {
        paddingHorizontal: 16,
        minHeight: 300,
    },
    tabContent: {
        marginTop: 4,
    },
    sectionHeader: {
        fontWeight: "bold",
        marginBottom: 8,
        color: "#1f2937",
    },
    textDescription: {
        lineHeight: 22,
        color: "#374151",
        textAlign: "justify",
    },
    divider: {
        marginVertical: 16,
    },
    imageContainer: {
        marginTop: 4,
    },
    companyImage: {
        width: "100%",
        height: 200,
        borderRadius: 8,
        marginBottom: 12,
        backgroundColor: "#e5e7eb",
    },
    reviewCard: {
        marginBottom: 12,
        backgroundColor: "#fff",
    },
    reviewHeader: {
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 8,
    },
    reviewUser: {
        fontWeight: "bold",
        marginLeft: 8,
        flex: 1,
    },
    reviewRating: {
        fontWeight: "bold",
        color: "#d97706",
    },
    reviewText: {
        color: "#4b5563",
        fontStyle: "italic",
    },
});

export default CompanyDetail;
