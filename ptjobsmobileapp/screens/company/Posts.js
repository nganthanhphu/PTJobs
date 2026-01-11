import React, { useState } from "react";
import { View, ScrollView, StyleSheet, Alert } from "react-native";
import {
    Appbar,
    TextInput,
    Button,
    SegmentedButtons,
} from "react-native-paper";
import PostCard from "../../components/PostCard.js";
import { useNavigation } from "@react-navigation/native";

const Posts = () => {
    const [tabValue, setTabValue] = useState("create");
    const navigation = useNavigation();

    const [postData, setPostData] = useState({
        title: "",
        category: "",
        description: "",
        salary: "",
        deadline: "",
        quantity: "",
    });


    const [myPosts, setMyPosts] = useState([
        {
            id: 1,
            title: "Nhân viên thu ngân",
            category: "Lao động phổ thông",
            createdAt: "01/01/2026",
            deadline: "12/01/2026",
            applied: 6,
            quantity: 10,
            status: "Active",
        },
        {
            id: 2,
            title: "Bảo vệ giữ xe",
            category: "An ninh / Bảo vệ",
            createdAt: "05/01/2026",
            deadline: "20/01/2026",
            applied: 10,
            quantity: 10, // Đã đủ
            status: "Closed",
        },
    ]);

    const handlePost = () => {
        if (!postData.title || !postData.salary) {
            Alert.alert("Thông báo", "Vui lòng điền đầy đủ thông tin!");
            return;
        }
        Alert.alert("Thành công", "Tin tuyển dụng đã được đăng!");
        setPostData({
            title: "",
            category: "",
            description: "",
            salary: "",
            deadline: "",
            quantity: "",
        });
        setTabValue("manage");
    };

    const renderCreatePost = () => (
        <View style={styles.formContainer}>
            <TextInput
                label="Tiêu đề công việc"
                mode="outlined"
                value={postData.title}
                onChangeText={(text) =>
                    setPostData({ ...postData, title: text })
                }
                style={styles.input}
                placeholder="Ví dụ: Nhân viên phục vụ..."
            />

            <TextInput
                label="Danh mục"
                mode="outlined"
                value={postData.category}
                onChangeText={(text) =>
                    setPostData({ ...postData, category: text })
                }
                style={styles.input}
                right={<TextInput.Icon icon="menu-down" />}
            />

            <TextInput
                label="Mô tả công việc"
                mode="outlined"
                value={postData.description}
                onChangeText={(text) =>
                    setPostData({ ...postData, description: text })
                }
                style={styles.input}
                multiline
                numberOfLines={5}
                placeholder="Mô tả chi tiết nhiệm vụ, yêu cầu..."
            />

            <TextInput
                label="Mức lương (VNĐ/h)"
                mode="outlined"
                value={postData.salary}
                onChangeText={(text) =>
                    setPostData({ ...postData, salary: text })
                }
                style={styles.input}
                keyboardType="numeric"
            />

            <View style={styles.rowInputs}>
                <TextInput
                    label="Hạn ứng tuyển"
                    mode="outlined"
                    value={postData.deadline}
                    onChangeText={(text) =>
                        setPostData({ ...postData, deadline: text })
                    }
                    style={[styles.input, styles.halfInput]}
                    right={<TextInput.Icon icon="calendar" />}
                    placeholder="dd/mm/yyyy"
                />
                <TextInput
                    label="Số lượng"
                    mode="outlined"
                    value={postData.quantity}
                    onChangeText={(text) =>
                        setPostData({ ...postData, quantity: text })
                    }
                    style={[styles.input, styles.halfInput]}
                    keyboardType="numeric"
                />
            </View>

            <Button
                mode="contained"
                onPress={handlePost}
                style={styles.submitButton}
                contentStyle={{ height: 50 }}
            >
                Đăng tin tuyển dụng
            </Button>
        </View>
    );

    const renderManagePosts = () => (
        <View style={styles.listContainer}>
            {myPosts.map((post) => (
                <PostCard
                    key={post.id}
                    post={post}
                    onPress={() => navigation.navigate("PostDetail", { postId: post.id })}
                />
            ))}
        </View>
    );

    return (
        <View style={styles.screen}>
            <Appbar.Header style={styles.appbar}>
                <Appbar.Content
                    title="Dashboard PTJobs"
                    titleStyle={styles.headerTitle}
                />
                <Appbar.Action
                    icon="bell-outline"
                    onPress={() => navigation.navigate("Notifications")}
                />
                <Appbar.Action
                    icon="account-circle-outline"
                    onPress={() => navigation.navigate("Profile")}
                />
            </Appbar.Header>

            <View style={styles.tabContainer}>
                <SegmentedButtons
                    value={tabValue}
                    onValueChange={setTabValue}
                    buttons={[
                        {
                            value: "create",
                            label: "Tạo bài đăng",
                            icon: "pencil-plus",
                        },
                        {
                            value: "manage",
                            label: "Quản lý bài đăng",
                            icon: "clipboard-list-outline",
                        },
                    ]}
                    density="medium"
                />
            </View>

            <ScrollView
                contentContainerStyle={styles.scrollContent}
                showsVerticalScrollIndicator={false}
            >
                {tabValue === "create"
                    ? renderCreatePost()
                    : renderManagePosts()}
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
        elevation: 0,
        borderBottomWidth: 1,
        borderBottomColor: "#f0f0f0",
    },
    headerTitle: {
        fontWeight: "bold",
        fontSize: 20,
    },
    tabContainer: {
        padding: 16,
        backgroundColor: "#fff",
    },
    scrollContent: {
        paddingBottom: 20,
    },
    formContainer: {
        paddingHorizontal: 16,
    },
    input: {
        marginBottom: 16,
        backgroundColor: "#fff",
    },
    rowInputs: {
        flexDirection: "row",
        justifyContent: "space-between",
        gap: 12,
    },
    halfInput: {
        flex: 1,
    },
    submitButton: {
        marginTop: 8,
        borderRadius: 8,
        backgroundColor: "#1f2937",
    },
    listContainer: {
        paddingHorizontal: 16,
    },
});

export default Posts;
