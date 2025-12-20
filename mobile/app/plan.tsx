import { View, Text, StyleSheet } from 'react-native';
import { useLocalSearchParams } from 'expo-router';

export default function Plan() {
    const { plan } = useLocalSearchParams();
    const parsedPlan = plan ? JSON.parse(plan as string) : null;

    if (!parsedPlan) {
        return (
            <View style={styles.container}>
                <Text>No plan data available.</Text>
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <Text style={styles.header}>{parsedPlan.name}</Text>

            <View style={styles.card}>
                <Text style={styles.metricLabel}>Total Calories</Text>
                <Text style={styles.metricValue}>{parsedPlan.calories} kcal</Text>
            </View>

            <View style={styles.row}>
                <View style={styles.stat}>
                    <Text style={styles.statLabel}>Protein</Text>
                    <Text style={styles.statValue}>{parsedPlan.protein}g</Text>
                </View>
                <View style={styles.stat}>
                    <Text style={styles.statLabel}>Carbs</Text>
                    <Text style={styles.statValue}>{parsedPlan.carbs}g</Text>
                </View>
                <View style={styles.stat}>
                    <Text style={styles.statLabel}>Fats</Text>
                    <Text style={styles.statValue}>{parsedPlan.fats}g</Text>
                </View>
            </View>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        backgroundColor: '#fff',
    },
    header: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        textAlign: 'center',
    },
    card: {
        backgroundColor: '#f0f0f0',
        padding: 20,
        borderRadius: 10,
        alignItems: 'center',
        marginBottom: 20,
    },
    metricLabel: {
        fontSize: 18,
        color: '#666',
    },
    metricValue: {
        fontSize: 32,
        fontWeight: 'bold',
        color: '#007AFF',
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    stat: {
        alignItems: 'center',
        flex: 1,
    },
    statLabel: {
        fontSize: 14,
        color: '#666',
    },
    statValue: {
        fontSize: 20,
        fontWeight: 'bold',
    },
});
