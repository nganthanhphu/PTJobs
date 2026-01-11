import React from "react";
import { View, StyleSheet } from "react-native";
import { useNavigation } from '@react-navigation/native';
import { Avatar, Card, Text } from "react-native-paper";

const JobCard = ({ job, onPress }) => {
    const navigation = useNavigation();

    const handlePress = () => {
        if (typeof onPress === 'function') {
            return onPress();
        }
        navigation.navigate('JobDetail', { job });
    };

    return (
        <Card style={styles.card} onPress={handlePress}>
            <Card.Content>
                <View style={styles.row}>
                    <Avatar.Image size={60} source={{ uri: job.logo }} />
                    <View style={styles.details}>
                        <Text variant="titleMedium">{job.title}</Text>
                        <Text variant="bodySmall" style={styles.salary}>
                            {job.salary}
                        </Text>
                        <Text variant="bodySmall">
                            {job.company} - {job.category}
                        </Text>
                    </View>
                </View>
            </Card.Content>
        </Card>
    );
};

const styles = StyleSheet.create({
    card: {
        marginBottom: 16,
        elevation: 3,
        borderRadius: 12,
        backgroundColor: "#ffffff",
    },
    row: {
        flexDirection: "row",
        alignItems: "center",
        gap: 16,
    },
    details: {
        flex: 1,
        justifyContent: "center",
        gap: 6,
    },
    salary: {
        color: "#059669",
        fontWeight: "600",
        fontSize: 15,
    },
});

export default JobCard;
