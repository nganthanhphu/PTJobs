import React, { useState } from "react";
import { View, ScrollView, StyleSheet } from "react-native";
import { Appbar, Searchbar, IconButton, Button } from "react-native-paper";
import JobCard from "../../components/JobCard.js";
import { useNavigation } from "@react-navigation/native";

const Jobs = () => {
    const navigation = useNavigation();
    const [searchQuery, setSearchQuery] = useState("");

    const mockJobs = [
        {
            id: 1,
            title: "Nhân viên tiếp tân",
            salary: "95 K/h",
            company: "KFC Q3",
            category: "Khách sạn",
            logo: "https://via.placeholder.com/60",
        },
        {
            id: 2,
            title: "Nhân viên tiếp tân",
            salary: "95 K/h",
            company: "KFC Q3",
            category: "Khách sạn",
            logo: "https://via.placeholder.com/60",
        },
    ];

    return (
        <View style={styles.screen}>
            <Appbar.Header>
                <Appbar.Content
                    title="PTJobs - Việc làm"
                    titleStyle={styles.appbarTitle}
                />
                <IconButton icon="bell-outline" size={24} onPress={() => navigation.navigate('Notifications')} />
                <IconButton
                    icon="account-circle-outline"
                    size={24}
                    onPress={() => {}}
                />
            </Appbar.Header>

            <ScrollView
                style={styles.container}
                showsVerticalScrollIndicator={false}
            >
                <View style={styles.searchFilterContainer}>
                    <Searchbar
                        placeholder="Tìm công việc"
                        onChangeText={setSearchQuery}
                        value={searchQuery}
                        style={styles.searchbar}
                        icon="magnify"
                    />
                    <Button
                        mode="contained"
                        style={styles.filterButton}
                        onPress={() => {}}
                    >
                        <IconButton icon="filter-variant" iconColor="white" />
                    </Button>
                </View>

                <View style={styles.section}>
                    {mockJobs.map((job) => (
                        <JobCard key={job.id} job={job} />
                    ))}
                </View>
            </ScrollView>
        </View>
    );
};

const styles = StyleSheet.create({
    screen: {
        flex: 1,
        backgroundColor: "#f5f5f5",
    },
    appbarTitle: {
        fontWeight: "bold",
        fontSize: 20,
    },
    container: {
        flex: 1,
        padding: 15,
    },
    searchFilterContainer: {
        flexDirection: "row",
        gap: 12,
        marginBottom: 20,
        alignItems: "center",
    },
    searchbar: {
        flex: 1,
        elevation: 1,
        backgroundColor: "#fff",
    },
    filterButton: {
        justifyContent: "center",
        height: 50,
        borderRadius: 25,
    },
    section: {
        marginBottom: 24,
    },
});

export default Jobs;
