import { useState } from 'react';
import { View, Text, TextInput, Button, StyleSheet, ScrollView, Alert } from 'react-native';
import { router } from 'expo-router';
import axios from 'axios';

// Replace with your machine's local IP if testing on real device
// For emulator, 10.0.2.2 usually connects to localhost
const API_URL = 'http://10.0.2.2:8000/onboarding';

export default function Onboarding() {
    const [age, setAge] = useState('');
    const [weight, setWeight] = useState('');
    const [height, setHeight] = useState('');
    const [gender, setGender] = useState('male');
    const [goal, setGoal] = useState('weight_loss');

    const handleSubmit = async () => {
        if (!age || !weight || !height) {
            Alert.alert("Error", "Please fill in all fields");
            return;
        }

        try {
            const payload = {
                age: parseInt(age),
                weight: parseFloat(weight),
                height: parseFloat(height),
                gender,
                goal,
                activity_level: 1.2 // Default for now
            };

            const response = await axios.post(API_URL, payload);
            const plan = response.data;

            // Navigate to Plan Screen with data
            router.push({ pathname: '/plan', params: { plan: JSON.stringify(plan) } });

        } catch (error) {
            console.error(error);
            Alert.alert("Error", "Failed to generate plan. Ensure backend is running.");
        }
    };

    return (
        <ScrollView contentContainerStyle={styles.container}>
            <Text style={styles.label}>Age</Text>
            <TextInput style={styles.input} keyboardType="numeric" value={age} onChangeText={setAge} />

            <Text style={styles.label}>Weight (kg)</Text>
            <TextInput style={styles.input} keyboardType="numeric" value={weight} onChangeText={setWeight} />

            <Text style={styles.label}>Height (cm)</Text>
            <TextInput style={styles.input} keyboardType="numeric" value={height} onChangeText={setHeight} />

            <Text style={styles.label}>Gender (male/female)</Text>
            <TextInput style={styles.input} value={gender} onChangeText={setGender} />

            <Text style={styles.label}>Goal (weight_loss/muscle_gain/maintenance)</Text>
            <TextInput style={styles.input} value={goal} onChangeText={setGoal} />

            <Button title="Generate Meal Plan" onPress={handleSubmit} />
        </ScrollView>
    );
}

const styles = StyleSheet.create({
    container: {
        padding: 20,
        backgroundColor: '#fff',
    },
    label: {
        fontSize: 16,
        marginBottom: 5,
        marginTop: 10,
        fontWeight: '500',
    },
    input: {
        borderWidth: 1,
        borderColor: '#ddd',
        padding: 10,
        borderRadius: 5,
        marginBottom: 10,
    },
});
