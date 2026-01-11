import React, { useState } from "react";
import { View, FlatList, StyleSheet, TouchableOpacity } from "react-native";
import { Appbar, Avatar, Text, IconButton, Divider } from "react-native-paper";

const Notification = ({ navigation }) => {
    const [notifications, setNotifications] = useState([
        {
            id: 1,
            type: "application",
            title: "Hồ sơ đã được xem",
            content:
                "Nhà tuyển dụng Jollibee VN đã xem hồ sơ ứng tuyển vị trí 'Nhân viên thu ngân' của bạn.",
            time: "2 giờ trước",
            isRead: false,
        },
        {
            id: 2,
            type: "job",
            title: "Có việc làm mới phù hợp",
            content:
                "Dựa trên hồ sơ của bạn, có 3 công việc phục vụ mới tại Quận 3.",
            time: "5 giờ trước",
            isRead: false,
        },
        {
            id: 3,
            type: "system",
            title: "Cập nhật hồ sơ ngay",
            content:
                "Hãy thêm chứng chỉ tiếng Anh để tăng 30% cơ hội được nhận việc!",
            time: "1 ngày trước",
            isRead: true,
        },
        {
            id: 4,
            type: "application",
            title: "Lời mời phỏng vấn",
            content: "Highlands Coffee mời bạn phỏng vấn vào 9:00 AM ngày mai.",
            time: "2 ngày trước",
            isRead: true,
        },
        {
            id: 5,
            type: "system",
            title: "Chào mừng đến với PTJobs",
            content: "Chúc bạn tìm được công việc ưng ý nhé!",
            time: "1 tuần trước",
            isRead: true,
        },
    ]);

    const markAllAsRead = () => {
        const updated = notifications.map((n) => ({ ...n, isRead: true }));
        setNotifications(updated);
    };

    const getIconProps = (type) => {
        switch (type) {
            case "application":
                return {
                    icon: "file-document-check-outline",
                    color: "#2563eb",
                    bg: "#dbeafe",
                };
            case "job":
                return {
                    icon: "briefcase-search-outline",
                    color: "#059669",
                    bg: "#d1fae5",
                };
            case "system":
            default:
                return {
                    icon: "bell-outline",
                    color: "#d97706",
                    bg: "#fef3c7",
                };
        }
    };

    const renderItem = ({ item }) => {
        const { icon, color, bg } = getIconProps(item.type);

        return (
            <TouchableOpacity
                style={[
                    styles.itemContainer,
                    !item.isRead && styles.unreadItem,
                ]}
                onPress={() => console.log(`Open notification ${item.id}`)}
            >
                <View style={styles.row}>
                    <View style={[styles.iconBox, { backgroundColor: bg }]}>
                        <Avatar.Icon
                            size={40}
                            icon={icon}
                            color={color}
                            style={{ backgroundColor: "transparent" }}
                        />
                    </View>

                    <View style={styles.contentBox}>
                        <View style={styles.headerRow}>
                            <Text
                                variant="titleSmall"
                                style={[
                                    styles.title,
                                    !item.isRead && styles.boldTitle,
                                ]}
                            >
                                {item.title}
                            </Text>
                            <Text variant="labelSmall" style={styles.timeText}>
                                {item.time}
                            </Text>
                        </View>
                        <Text
                            variant="bodyMedium"
                            numberOfLines={2}
                            style={styles.description}
                        >
                            {item.content}
                        </Text>
                    </View>

                    {!item.isRead && <View style={styles.unreadDot} />}
                </View>
            </TouchableOpacity>
        );
    };

    return (
        <View style={styles.screen}>
            <Appbar.Header elevated style={styles.appbar}>
                <Appbar.BackAction onPress={() => navigation?.goBack()} />
                <Appbar.Content
                    title="Thông báo"
                    titleStyle={styles.headerTitle}
                />
                <Appbar.Action
                    icon="playlist-check"
                    onPress={markAllAsRead}
                    tooltip="Đánh dấu đã đọc"
                />
            </Appbar.Header>

            <FlatList
                data={notifications}
                renderItem={renderItem}
                keyExtractor={(item) => item.id.toString()}
                contentContainerStyle={styles.listContent}
                ItemSeparatorComponent={() => <Divider />}
                showsVerticalScrollIndicator={false}
            />
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
    listContent: {
        paddingBottom: 20,
    },
    itemContainer: {
        paddingVertical: 16,
        paddingHorizontal: 16,
        backgroundColor: "#fff",
    },
    unreadItem: {
        backgroundColor: "#f0f9ff",
    },
    row: {
        flexDirection: "row",
        alignItems: "flex-start",
    },
    iconBox: {
        width: 48,
        height: 48,
        borderRadius: 24,
        justifyContent: "center",
        alignItems: "center",
        marginRight: 16,
    },
    contentBox: {
        flex: 1,
        marginRight: 8,
    },
    headerRow: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
        marginBottom: 4,
    },
    title: {
        flex: 1,
        color: "#1f2937",
        marginRight: 8,
    },
    boldTitle: {
        fontWeight: "bold",
    },
    timeText: {
        color: "#9ca3af",
        fontSize: 11,
    },
    description: {
        color: "#4b5563",
        fontSize: 13,
    },
    unreadDot: {
        width: 10,
        height: 10,
        borderRadius: 5,
        backgroundColor: "#2563eb",
        marginTop: 6,
    },
});

export default Notification;
