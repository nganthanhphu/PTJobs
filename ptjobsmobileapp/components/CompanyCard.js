import React from "react";
import { View, StyleSheet } from "react-native";
import { Card, Avatar, Text } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";

const CompanyCard = ({ company, jobCount, onPress }) => {
  const navigation = useNavigation();
  
  const handlePress = () => {
      if (typeof onPress === 'function') {
          return onPress();
      }
      navigation.navigate('CompanyDetail', { company });
  };
  
    return (
        <Card style={styles.card} onPress={handlePress}>
            <Card.Content style={styles.content}>
                <View style={styles.logoContainer}>
                    <Avatar.Image size={80} source={{ uri: company.logo }} />
                </View>
                <Text
                    variant="titleMedium"
                    style={styles.name}
                    numberOfLines={1}
                >
                    {company.name}
                </Text>
                <View style={styles.jobCountBox}>
                    <Text style={styles.jobCountText}>
                        {jobCount} Job{jobCount !== 1 ? "s" : ""}
                    </Text>
                </View>
            </Card.Content>
        </Card>
    );
};

const styles = StyleSheet.create({
    card: {
        elevation: 3,
        borderRadius: 12,
        backgroundColor: "#ffffff",
        marginHorizontal: 8,
        marginVertical: 8,
        width: 140,
    },
    content: {
        alignItems: "center",
        paddingVertical: 16,
        paddingHorizontal: 12,
    },
    logoContainer: {
        marginBottom: 12,
    },
    name: {
        fontWeight: "600",
        textAlign: "center",
        marginBottom: 8,
        color: "#1f2937",
    },
    jobCountBox: {
        marginTop: 8,
        paddingVertical: 6,
        paddingHorizontal: 12,
        borderWidth: 1,
        borderColor: "#059669",
        borderRadius: 6,
        alignSelf: "center",
    },
    jobCountText: {
        fontSize: 12,
        fontWeight: "500",
        color: "#059669",
        textAlign: "center",
    },
});

export default CompanyCard;
