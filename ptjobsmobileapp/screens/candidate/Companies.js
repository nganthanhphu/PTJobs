import React, { useState } from "react";
import { View, FlatList, StyleSheet } from "react-native";
import { Appbar, Searchbar, IconButton } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import CompanyCard from "../../components/CompanyCard.js";

const Companies = () => {
    const navigation = useNavigation();
    const [searchQuery, setSearchQuery] = useState("");

    const mockCompanies = [
        {
            id: 1,
            name: "Jolibee VN",
            logo: "https://via.placeholder.com/80",
            jobCount: 3,
        },
        {
            id: 2,
            name: "Jolibee VN",
            logo: "https://via.placeholder.com/80",
            jobCount: 3,
        },
        {
            id: 3,
            name: "Jolibee VN",
            logo: "https://via.placeholder.com/80",
            jobCount: 3,
        },
        {
            id: 4,
            name: "Jolibee VN",
            logo: "https://via.placeholder.com/80",
            jobCount: 3,
        },
    ];

    return (
        <View style={styles.screen}>
            <Appbar.Header>
                <Appbar.Content
                    title="PTJobs - Công ty"
                    titleStyle={styles.appbarTitle}
                />
                <IconButton icon="bell-outline" size={24} onPress={() => navigation.navigate('Notifications')} />
                <IconButton
                    icon="account-circle-outline"
                    size={24}
                    onPress={() => {}}
                />
            </Appbar.Header>

            <FlatList
                data={mockCompanies}
                renderItem={({ item }) => (
                    <CompanyCard
                        company={item}
                        jobCount={item.jobCount}
                    />
                )}
                keyExtractor={(item) => item.id.toString()}
                numColumns={2}
                columnWrapperStyle={styles.row}
                ListHeaderComponent={
                    <Searchbar
                        placeholder="Tìm công ty"
                        onChangeText={setSearchQuery}
                        value={searchQuery}
                        style={styles.searchbar}
                        icon="magnify"
                    />
                }
                contentContainerStyle={styles.listContent}
                showsVerticalScrollIndicator={false}
            />
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
    row: {
        justifyContent: "space-between",
        paddingHorizontal: 25,
    },
    searchbar: {
        margin: 16,
        elevation: 1,
        backgroundColor: "#fff",
    },
    listContent: {
        paddingHorizontal: 8,
        paddingBottom: 16,
    },
});

export default Companies;
