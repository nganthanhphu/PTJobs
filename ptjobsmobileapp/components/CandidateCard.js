import React from "react";
import { View, StyleSheet } from "react-native";
import { Card, Avatar, Text, Icon } from "react-native-paper";

const CandidateCard = ({ candidate, onPress }) => {
    const isMale = candidate.gender.toLowerCase() === "nam";
    const genderIcon = isMale ? "gender-male" : "gender-female";
    const genderColor = isMale ? "#2563eb" : "#e11d48";

    return (
        <Card style={styles.card} onPress={onPress}>
            <Card.Content style={styles.content}>
                <View style={styles.row}>
                    <Avatar.Image
                        size={60}
                        source={{ uri: candidate.avatar }}
                        style={styles.avatar}
                    />

                    <View style={styles.info}>
                        <Text
                            variant="titleMedium"
                            style={styles.name}
                            numberOfLines={1}
                        >
                            {candidate.name}
                        </Text>

                        <Text variant="bodyMedium" style={styles.applyRow}>
                            Ứng tuyển:{" "}
                            <Text style={styles.jobHighlight}>
                                {candidate.applyJob}
                            </Text>
                        </Text>

                        <View style={styles.genderContainer}>
                            <Icon
                                source={genderIcon}
                                size={14}
                                color={genderColor}
                            />
                            <Text
                                style={[
                                    styles.genderText,
                                    { color: genderColor },
                                ]}
                            >
                                {candidate.gender}
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
        borderRadius: 10,
        backgroundColor: "#ffffff",
        elevation: 2,
        marginHorizontal: 4,
    },
    content: {
        paddingVertical: 12,
        paddingHorizontal: 16,
    },
    row: {
        flexDirection: "row",
        alignItems: "center",
    },
    avatar: {
        backgroundColor: "transparent",
    },
    info: {
        marginLeft: 16,
        flex: 1,
        justifyContent: "center",
        gap: 4,
    },
    name: {
        fontWeight: "bold",
        fontSize: 16,
        color: "#1f2937",
    },
    applyRow: {
        color: "#6b7280",
        fontSize: 13,
    },
    jobHighlight: {
        fontWeight: "600",
        color: "#059669",
    },
    genderContainer: {
        flexDirection: "row",
        alignItems: "center",
        marginTop: 2,
        backgroundColor: "#f3f4f6",
        alignSelf: "flex-start",
        paddingHorizontal: 6,
        paddingVertical: 2,
        borderRadius: 4,
        gap: 4,
    },
    genderText: {
        fontSize: 11,
        fontWeight: "500",
    },
});

export default CandidateCard;
