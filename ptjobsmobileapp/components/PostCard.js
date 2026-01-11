import React from "react";
import { View, StyleSheet } from "react-native";
import { Card, Text, Icon } from "react-native-paper";

const PostCard = ({ post, onPress }) => {
    return (
        <Card style={styles.card} onPress={onPress}>
            <Card.Content>
                <View style={styles.container}>
                    <View style={styles.infoColumn}>
                        <Text variant="titleMedium" style={styles.title}>
                            {post.title}
                        </Text>
                        <View style={styles.rowItem}>
                            <Icon
                                source="tag-outline"
                                size={16}
                                color="#6b7280"
                            />
                            <Text variant="bodySmall" style={styles.subText}>
                                {post.category}
                            </Text>
                        </View>
                        <View style={styles.rowItem}>
                            <Icon
                                source="calendar-clock-outline"
                                size={16}
                                color="#6b7280"
                            />
                            <Text variant="bodySmall" style={styles.subText}>
                                {post.createdAt} - {post.deadline}
                            </Text>
                        </View>
                    </View>

                    <View style={styles.statsColumn}>
                        <View style={styles.statsBox}>
                            <Text
                                variant="titleMedium"
                                style={styles.statsNumber}
                            >
                                {post.applied}
                            </Text>
                            <Text
                                variant="labelSmall"
                                style={styles.statsLabel}
                            >
                                Đã nộp
                            </Text>
                        </View>
                    </View>
                </View>
            </Card.Content>
        </Card>
    );
};

const styles = StyleSheet.create({
    card: {
        marginBottom: 12,
        borderRadius: 8,
        backgroundColor: "#fff",
        elevation: 2,
        marginHorizontal: 4,
    },
    container: {
        flexDirection: "row",
        justifyContent: "space-between",
        alignItems: "center",
    },
    infoColumn: {
        flex: 1,
        marginRight: 12,
        gap: 6, 
    },
    title: {
        fontWeight: "bold",
        fontSize: 16,
        color: "#1f2937",
    },
    rowItem: {
        flexDirection: "row",
        alignItems: "center",
        gap: 6,
    },
    subText: {
        color: "#4b5563",
        fontSize: 13,
    },
    statsColumn: {
        justifyContent: "center",
        alignItems: "center",
    },
    statsBox: {
        borderWidth: 1.5,
        borderColor: "#374151",
        borderRadius: 6,
        paddingVertical: 8,
        paddingHorizontal: 12,
        alignItems: "center",
        minWidth: 70,
        backgroundColor: "#f9fafb",
    },
    statsNumber: {
        fontWeight: "bold",
        fontSize: 18,
        color: "#111827",
    },
    statsLabel: {
        fontSize: 10,
        color: "#6b7280",
        marginTop: 2,
    },
});

export default PostCard;