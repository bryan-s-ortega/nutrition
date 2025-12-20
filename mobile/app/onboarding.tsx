import { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ScrollView, Alert, SafeAreaView, StatusBar, KeyboardAvoidingView, Platform } from 'react-native';
import { router } from 'expo-router';
import axios from 'axios';
import { Colors } from '../constants/Colors';


const API_URL = Platform.OS === 'web'
    ? 'http://localhost:8000/onboarding'
    : 'http://10.0.2.2:8000/onboarding';


export default function Onboarding() {
    const [age, setAge] = useState('');
    const [weight, setWeight] = useState('');
    const [height, setHeight] = useState('');
    const [gender, setGender] = useState('male');
    const [goal, setGoal] = useState('weight_loss');

    const handleSubmit = async () => {
        if (!age || !weight || !height) {
            Alert.alert("Missing Information", "Please fill in all fields to continue.");
            return;
        }

        try {
            const payload = {
                age: parseInt(age),
                weight: parseFloat(weight),
                height: parseFloat(height),
                gender,
                goal,
                activity_level: 1.2
            };

            const response = await axios.post(API_URL, payload);
            const plan = response.data;

            router.push({ pathname: '/plan', params: { plan: JSON.stringify(plan) } });

        } catch (error) {
            console.error(error);
            Alert.alert("Connection Error", "Failed to generate plan. Please ensure the backend server is running.");
        }
    };

    const SelectionBtn = ({ label, value, selectedValue, onSelect }) => (
        <TouchableOpacity
            style={[styles.selectBtn, selectedValue === value && styles.selectBtnActive]}
            onPress={() => onSelect(value)}
        >
            <Text style={[styles.selectBtnText, selectedValue === value && styles.selectBtnTextActive]}>
                {label}
            </Text>
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.safeArea}>
            <StatusBar barStyle="dark-content" backgroundColor={Colors.background} />
            <KeyboardAvoidingView
                behavior={Platform.OS === "ios" ? "padding" : "height"}
                style={styles.keyboardView}
            >
                <ScrollView contentContainerStyle={styles.container}>
                    <View style={styles.headerContainer}>
                        <Text style={styles.headerTitle}>Your Nutrition Journey</Text>
                        <Text style={styles.headerSubtitle}>Tell us about yourself to get a personalized plan.</Text>
                    </View>

                    <View style={styles.formSection}>
                        <Text style={styles.label}>Biometrics</Text>
                        <View style={styles.row}>
                            <View style={styles.halfInput}>
                                <Text style={styles.subLabel}>Age</Text>
                                <TextInput
                                    style={styles.input}
                                    keyboardType="numeric"
                                    value={age}
                                    onChangeText={setAge}
                                    placeholder="25"
                                    placeholderTextColor="#999"
                                />
                            </View>
                            <View style={styles.halfInput}>
                                <Text style={styles.subLabel}>Weight (kg)</Text>
                                <TextInput
                                    style={styles.input}
                                    keyboardType="numeric"
                                    value={weight}
                                    onChangeText={setWeight}
                                    placeholder="70"
                                    placeholderTextColor="#999"
                                />
                            </View>
                        </View>

                        <View style={styles.inputGroup}>
                            <Text style={styles.subLabel}>Height (cm)</Text>
                            <TextInput
                                style={styles.input}
                                keyboardType="numeric"
                                value={height}
                                onChangeText={setHeight}
                                placeholder="175"
                                placeholderTextColor="#999"
                            />
                        </View>

                        <Text style={styles.label}>Gender</Text>
                        <View style={styles.selectionRow}>
                            <SelectionBtn label="Male" value="male" selectedValue={gender} onSelect={setGender} />
                            <SelectionBtn label="Female" value="female" selectedValue={gender} onSelect={setGender} />
                        </View>

                        <Text style={styles.label}>Physical Objective</Text>
                        <View style={styles.selectionColumn}>
                            <SelectionBtn label="Weight Loss" value="weight_loss" selectedValue={goal} onSelect={setGoal} />
                            <SelectionBtn label="Maintenance" value="maintenance" selectedValue={goal} onSelect={setGoal} />
                            <SelectionBtn label="Muscle Gain" value="muscle_gain" selectedValue={goal} onSelect={setGoal} />
                        </View>
                    </View>

                    <TouchableOpacity style={styles.submitBtn} onPress={handleSubmit}>
                        <Text style={styles.submitBtnText}>Generate My Plan</Text>
                    </TouchableOpacity>

                </ScrollView>
            </KeyboardAvoidingView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    safeArea: {
        flex: 1,
        backgroundColor: Colors.background,
    },
    keyboardView: {
        flex: 1,
    },
    container: {
        padding: 24,
        paddingBottom: 40,
    },
    headerContainer: {
        marginBottom: 32,
        marginTop: 10,
    },
    headerTitle: {
        fontSize: 28,
        fontWeight: 'bold',
        color: Colors.primaryDark,
        marginBottom: 8,
    },
    headerSubtitle: {
        fontSize: 16,
        color: Colors.text.secondary,
        lineHeight: 22,
    },
    formSection: {
        marginBottom: 32,
    },
    label: {
        fontSize: 18,
        fontWeight: '600',
        color: Colors.primaryDark,
        marginBottom: 16,
        marginTop: 8,
    },
    subLabel: {
        fontSize: 14,
        color: Colors.text.secondary,
        marginBottom: 6,
    },
    input: {
        backgroundColor: Colors.surface,
        borderWidth: 1,
        borderColor: Colors.border,
        borderRadius: 12,
        padding: 14,
        fontSize: 16,
        color: Colors.text.primary,
    },
    row: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginBottom: 16,
    },
    halfInput: {
        width: '48%',
    },
    inputGroup: {
        marginBottom: 24,
    },
    selectionRow: {
        flexDirection: 'row',
        marginBottom: 24,
    },
    selectionColumn: {
        gap: 12,
    },
    selectBtn: {
        flex: 1,
        backgroundColor: Colors.surface,
        borderWidth: 1,
        borderColor: Colors.border,
        paddingVertical: 14,
        paddingHorizontal: 16,
        borderRadius: 12,
        alignItems: 'center',
        marginRight: 8,
    },
    selectBtnActive: {
        backgroundColor: Colors.primary,
        borderColor: Colors.primary,
    },
    selectBtnText: {
        fontSize: 16,
        color: Colors.text.primary,
        fontWeight: '500',
    },
    selectBtnTextActive: {
        color: Colors.surface,
        fontWeight: '700',
    },
    submitBtn: {
        backgroundColor: Colors.secondary,
        paddingVertical: 18,
        borderRadius: 16,
        alignItems: 'center',
        shadowColor: Colors.secondary,
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 5,
    },
    submitBtnText: {
        fontSize: 18,
        fontWeight: 'bold',
        color: Colors.primaryDark,
    },
});
