import { Link } from 'expo-router';
import { View, Text, StyleSheet, Button } from 'react-native';

export default function Home() {
    return (
        <View style={styles.container}>
            <Text style={styles.title}>Nutrition App</Text>
            <Text style={styles.subtitle}>Achieve your physical goals with AI-driven meal plans.</Text>

            <Link href="/onboarding" asChild>
                <Button title="Get Started" />
            </Link>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
        backgroundColor: '#fff',
    },
    title: {
        fontSize: 32,
        fontWeight: 'bold',
        marginBottom: 10,
    },
    subtitle: {
        fontSize: 16,
        textAlign: 'center',
        marginBottom: 30,
        color: '#666',
    },
});
