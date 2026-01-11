import React, { useState, useEffect } from "react";
import { View, ScrollView, StyleSheet, Alert } from "react-native";
import {
    Appbar,
    Avatar,
    Button,
    SegmentedButtons,
    TextInput,
    Text,
    Card,
    Divider,
    Chip,
} from "react-native-paper";

const PostDetail = ({ navigation, route }) => {
    const { postId } = route.params || {};

  const [tabValue, setTabValue] = useState("detail");
  
    const [postData, setPostData] = useState({
        id: postId || 1,
        title: "Nhân viên thu ngân",
        company: "Jollibee VN - Tam Phong Ward",
        salary: "35K/h",
        deadline: "12/01/2026",
        createdAt: "01/01/2026",
        description:
            "Thực hiện thanh toán, in hóa đơn, kiểm tra tiền mặt cuối ca. Giữ gìn vệ sinh khu vực quầy.",
        category: "Lao động phổ thông",
        quantity: "10",
        applied: 6,
    });

    const reviews = [
        {
            id: 1,
            user: "Hoàng Phi Hùng",
            date: "11/01/2026",
            rating: 5,
            comment: "Việc nhẹ, lương cao, quản lý nice!",
        },
        {
            id: 2,
            user: "Nguyễn Văn A",
            date: "10/01/2026",
            rating: 4,
            comment: "Giờ giấc hơi gắt một chút.",
        },
    ];

    const candidates = [
        {
            id: 1,
            name: "Hoàng Phi Hùng",
            avatar: "https://via.placeholder.com/150",
        },
        {
            id: 2,
            name: "Trần Thị B",
            avatar: "https://via.placeholder.com/150",
        },
    ];

    const renderDetailTab = () => (
        <View style={styles.tabContent}>
            <TextInput
                label="Tiêu đề"
                mode="outlined"
                value={postData.title}
                onChangeText={(text) =>
                    setPostData({ ...postData, title: text })
                }
                style={styles.input}
            />
            <TextInput
                label="Danh mục"
                mode="outlined"
                value={postData.category}
                style={styles.input}
                right={<TextInput.Icon icon="menu-down" />}
            />
            <TextInput
                label="Mô tả"
                mode="outlined"
                value={postData.description}
                multiline
                numberOfLines={6}
                style={styles.input}
            />
            <TextInput
                label="Mức lương"
                mode="outlined"
                value={postData.salary}
                style={styles.input}
            />
            <View style={styles.rowInputs}>
                <TextInput
                    label="Hạn tuyển"
                    mode="outlined"
                    value={postData.deadline}
                    style={[styles.input, styles.halfInput]}
                    right={<TextInput.Icon icon="calendar" />}
                />
                <TextInput
                    label="Số lượng"
                    mode="outlined"
                    value={postData.quantity}
                    style={[styles.input, styles.halfInput]}
                    keyboardType="numeric"
                />
            </View>

            <View style={styles.actionFooter}>
                <Button
                    mode="outlined"
                    textColor="#dc2626"
                    style={[styles.actionBtn, { borderColor: "#dc2626" }]}
                    onPress={() =>
                        Alert.alert("Cảnh báo", "Bạn muốn xóa tin này?")
                    }
                >
                    Xóa tin
                </Button>
                <Button
                    mode="contained"
                    style={[styles.actionBtn, { backgroundColor: "#1f2937" }]}
                    onPress={() =>
                        Alert.alert("Thành công", "Đã cập nhật tin!")
                    }
                >
                    Cập nhật tin
                </Button>
            </View>
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
                                icon="account"
                                style={{ backgroundColor: "#e5e7eb" }}
                            />
                            <View style={{ marginLeft: 12, flex: 1 }}>
                                <Text style={{ fontWeight: "bold" }}>
                                    {rv.user}
                                </Text>
                                <View
                                    style={{
                                        flexDirection: "row",
                                        justifyContent: "space-between",
                                    }}
                                >
                                    <Text
                                        style={{
                                            fontSize: 12,
                                            color: "#6b7280",
                                        }}
                                    >
                                        {rv.date}
                                    </Text>
                                </View>
                            </View>
                        </View>
                        <Divider style={{ marginVertical: 8 }} />
                        <Text style={{ fontStyle: "italic", color: "#374151" }}>
                            "{rv.comment}"
                        </Text>
                        <View style={{ alignItems: "flex-end", marginTop: 8 }}>
                            <Chip
                                icon="reply"
                                style={{ height: 28 }}
                                textStyle={{ fontSize: 10, marginVertical: -4 }}
                            >
                                Phản hồi
                            </Chip>
                        </View>
                    </Card.Content>
                </Card>
            ))}
        </View>
    );

    const renderCandidateTab = () => (
        <View style={styles.tabContent}>
            {candidates.map((cd) => (
                <Card key={cd.id} style={styles.candidateCard} onPress={() => navigation.navigate("CandidateDetail", { candidateId: cd.id })}>
                    <Card.Content>
                        <View style={styles.candidateRow}>
                            <Avatar.Image
                                size={50}
                                source={{ uri: cd.avatar }}
                            />
                            <Text
                                variant="titleMedium"
                                style={{
                                    fontWeight: "bold",
                                    marginLeft: 12,
                                    flex: 1,
                                }}
                            >
                                {cd.name}
                            </Text>
                        </View>

                        <View style={styles.candidateActions}>
                            <Button
                                mode="outlined"
                                compact
                                style={{ flex: 1, marginRight: 4 }}
                            >
                                CV
                            </Button>
                            <Button
                                mode="contained"
                                compact
                                buttonColor="#059669"
                                style={{ flex: 1.5, marginHorizontal: 4 }}
                            >
                                Tuyển dụng
                            </Button>
                            <Button
                                mode="contained"
                                compact
                                buttonColor="#dc2626"
                                style={{ flex: 1 }}
                            >
                                Từ chối
                            </Button>
                        </View>
                    </Card.Content>
                </Card>
            ))}
        </View>
    );

    return (
        <View style={styles.screen}>
            <Appbar.Header elevated style={styles.appbar}>
                <Appbar.BackAction onPress={() => navigation.goBack()} />
                <Appbar.Content
                    title="Chi tiết tin tuyển dụng"
                    titleStyle={styles.headerTitle}
                />
            </Appbar.Header>

            <ScrollView
                showsVerticalScrollIndicator={false}
                contentContainerStyle={styles.scrollContent}
            >
                <Card style={styles.topCard}>
                    <Card.Content style={styles.topCardContent}>
                        <View style={styles.topRow}>
                            <Avatar.Icon
                                size={64}
                                icon="briefcase"
                                style={{ backgroundColor: "#f3f4f6" }}
                                color="#333"
                            />
                            <View style={styles.topInfo}>
                                <Text
                                    variant="titleMedium"
                                    style={styles.jobTitle}
                                >
                                    {postData.title}
                                </Text>
                                <Text
                                    variant="bodySmall"
                                    style={styles.companyText}
                                >
                                    {postData.company}
                                </Text>
                                <Text
                                    variant="titleMedium"
                                    style={styles.salaryText}
                                >
                                    {postData.salary}
                                </Text>
                            </View>
                        </View>
                        <View style={styles.dateBox}>
                            <Text style={styles.dateText}>
                                {postData.deadline}
                            </Text>
                        </View>
                    </Card.Content>
                </Card>

                <View style={styles.segmentContainer}>
                    <SegmentedButtons
                        value={tabValue}
                        onValueChange={setTabValue}
                        buttons={[
                            { value: "detail", label: "Chi tiết" },
                            { value: "review", label: "Đánh giá" },
                            { value: "candidate", label: "Ứng viên" },
                        ]}
                        density="medium"
                    />
                </View>

                {tabValue === "detail" && renderDetailTab()}
                {tabValue === "review" && renderReviewTab()}
                {tabValue === "candidate" && renderCandidateTab()}
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: "#fff",
    },
    appbar: {
        backgroundColor: "#fff",
    },
    headerTitle: {
        fontWeight: "bold",
        fontSize: 18,
    },
    scrollContent: {
        paddingBottom: 30,
    },
    topCard: {
        margin: 16,
        backgroundColor: "#fff",
        borderRadius: 12,
        elevation: 2,
        borderWidth: 1,
        borderColor: "#e5e7eb",
    },
    topCardContent: {
        position: "relative",
        paddingVertical: 16,
    },
    topRow: {
        flexDirection: "row",
        alignItems: "center",
    },
    topInfo: {
        marginLeft: 16,
        flex: 1,
        paddingRight: 80,
    },
    jobTitle: {
        fontWeight: "bold",
        fontSize: 18,
        color: "#1f2937",
    },
    companyText: {
        color: "#6b7280",
        marginVertical: 2,
    },
    salaryText: {
        fontWeight: "bold",
        color: "#059669",
        marginTop: 4,
    },
    dateBox: {
        position: "absolute",
        right: 16,
        bottom: 16,
        borderWidth: 1.5,
        borderColor: "#374151",
        paddingHorizontal: 8,
        paddingVertical: 4,
        transform: [{ rotate: "-3deg" }],
        backgroundColor: "#fff",
    },
    dateText: {
        fontWeight: "bold",
        fontSize: 14,
        color: "#1f2937",
    },
    segmentContainer: {
        paddingHorizontal: 16,
        marginBottom: 16,
    },
    tabContent: {
        paddingHorizontal: 16,
    },
    input: {
        marginBottom: 12,
        backgroundColor: "#fff",
    },
    rowInputs: {
        flexDirection: "row",
        gap: 12,
    },
    halfInput: {
        flex: 1,
    },
    actionFooter: {
        flexDirection: "row",
        marginTop: 16,
        gap: 12,
    },
    actionBtn: {
        flex: 1,
        borderRadius: 8,
    },
    reviewCard: {
        marginBottom: 12,
        backgroundColor: "#fff",
        borderWidth: 1,
        borderColor: "#f3f4f6",
    },
    reviewHeader: {
        flexDirection: "row",
        alignItems: "center",
    },
    candidateCard: {
        marginBottom: 12,
        backgroundColor: "#fff",
        borderWidth: 1,
        borderColor: "#f3f4f6",
    },
    candidateRow: {
        flexDirection: "row",
        alignItems: "center",
        marginBottom: 12,
    },
    candidateActions: {
        flexDirection: "row",
        justifyContent: "space-between",
    },
});

export default PostDetail;
