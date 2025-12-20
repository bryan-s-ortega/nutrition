import { View, Text, StyleSheet, ScrollView, TouchableOpacity, SafeAreaView, StatusBar } from 'react-native';
import { useLocalSearchParams, router } from 'expo-router';
import { Colors } from '../constants/Colors';

export default function Plan() {
    const { plan } = useLocalSearchParams();
    const parsedPlan = plan ? JSON.parse(plan as string) : null;

    if (!parsedPlan) {
        return (
            <SafeAreaView style={styles.safeArea}>
                <View style={styles.container}>
                    <Text style={styles.errorText}>No plan data available.</Text>
                    <TouchableOpacity style={styles.secondaryBtn} onPress={() => router.back()}>
                        <Text style={styles.secondaryBtnText}>Go Back</Text>
                    </TouchableOpacity>
                </View>
            </SafeAreaView>
        );
    }

    const MacroCard = ({ label, value, color, totalCals }) => {
        // Approximate calories from macro for visual bar length relative to total (just for visual balance)
        // Protein/Carbs = 4cal/g, Fat = 9cal/g
        let calFromMacro = 0;
        if (label === 'Protein' || label === 'Carbs') calFromMacro = value * 4;
        if (label === 'Fats') calFromMacro = value * 9;

        const percentage = Math.min((calFromMacro / totalCals) * 100, 100);

        return (
            <View style={styles.macroCard}>
                <View style={styles.macroHeader}>
                    <Text style={styles.macroLabel}>{label}</Text>
                    <Text style={[styles.macroValue, { color }]}>{value}g</Text>
                </View>
                <View style={styles.progressBarBackground}>
                    <View style={[styles.progressBarFill, { width: `${percentage}%`, backgroundColor: color }]} />
                </View>
                <Text style={styles.macroCalText}>{Math.round(calFromMacro)} kcal</Text>
            </View>
        );
    };

    return (
        <SafeAreaView style={styles.safeArea}>
            <StatusBar barStyle="dark-content" />
            <ScrollView contentContainerStyle={styles.container}>
                <View style={styles.header}>
                    <Text style={styles.title}>Your Daily Target</Text>
                    <Text style={styles.subtitle}>{parsedPlan.name}</Text>
                </View>

                <View style={styles.mainCard}>
                    <Text style={styles.mainCardLabel}>Total Calories</Text>
                    <Text style={styles.mainCardValue}>{parsedPlan.calories}</Text>
                    <Text style={styles.unit}>kcal / day</Text>
                </View>

                <View style={styles.macrosContainer}>
                    <Text style={styles.sectionTitle}>Macro Distribution</Text>
                    <MacroCard
                        label="Protein"
                        value={parsedPlan.protein}
                        color="#E76F51"
                        totalCals={parsedPlan.calories}
                    />
                    <MacroCard
                        label="Carbs"
                        value={parsedPlan.carbs}
                        color="#E9C46A"
                        totalCals={parsedPlan.calories}
                    />
                    <MacroCard
                        label="Fats"
                        value={parsedPlan.fats}
                        color="#2A9D8F"
                        totalCals={parsedPlan.calories}
                    />
                </View>

                <TouchableOpacity style={styles.resetBtn} onPress={() => router.back()}>
                    <Text style={styles.resetBtnText}>Recalculate Plan</Text>
                </TouchableOpacity>
            </ScrollView>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    safeArea: {
        flex: 1,
        backgroundColor: Colors.background,
    },
    container: {
        padding: 24,
    },
    header: {
        alignItems: 'center',
        marginBottom: 32,
        marginTop: 10,
    },
    title: {
        fontSize: 22,
        color: Colors.text.secondary,
        fontWeight: '500',
    },
    subtitle: {
        fontSize: 26,
        color: Colors.primaryDark,
        fontWeight: 'bold',
        marginTop: 4,
    },
    mainCard: {
        backgroundColor: Colors.primaryDark,
        borderRadius: 24,
        padding: 40,
        alignItems: 'center',
        marginBottom: 32,
        shadowColor: Colors.primaryDark,
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.25,
        shadowRadius: 16,
        elevation: 8,
    },
    mainCardLabel: {
        color: 'rgba(255,255,255,0.8)',
        fontSize: 18,
        fontWeight: '500',
        marginBottom: 8,
    },
    mainCardValue: {
        color: '#fff',
        fontSize: 56,
        fontWeight: 'bold',
    },
    unit: {
        color: Colors.accent,
        fontSize: 18,
        fontWeight: '600',
        marginTop: 4,
    },
    macrosContainer: {
        marginBottom: 32,
    },
    sectionTitle: {
        fontSize: 20,
        fontWeight: 'bold',
        color: Colors.primaryDark,
        marginBottom: 16,
    },
    macroCard: {
        backgroundColor: Colors.surface,
        borderRadius: 16,
        padding: 20,
        marginBottom: 16,
        borderWidth: 1,
        borderColor: Colors.border,
    },
    macroHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'flex-end',
        marginBottom: 12,
    },
    macroLabel: {
        fontSize: 18,
        fontWeight: '600',
        color: Colors.text.primary,
    },
    macroValue: {
        fontSize: 24,
        fontWeight: 'bold',
    },
    progressBarBackground: {
        height: 10,
        backgroundColor: Colors.border,
        borderRadius: 5,
        overflow: 'hidden',
        marginBottom: 8,
    },
    progressBarFill: {
        height: '100%',
        borderRadius: 5,
    },
    macroCalText: {
        fontSize: 14,
        color: Colors.text.secondary,
        textAlign: 'right',
    },
    resetBtn: {
        paddingVertical: 16,
        borderRadius: 16,
        borderWidth: 1,
        borderColor: Colors.primaryDark,
        alignItems: 'center',
        marginBottom: 20,
    },
    resetBtnText: {
        fontSize: 16,
        fontWeight: '600',
        color: Colors.primaryDark,
    },
    errorText: {
        fontSize: 18,
        color: Colors.danger,
        textAlign: 'center',
        marginBottom: 20,
    },
    secondaryBtn: {
        padding: 12,
        backgroundColor: Colors.secondary,
        borderRadius: 8,
    },
    secondaryBtnText: {
        color: Colors.primaryDark,
        fontWeight: 'bold',
    },
});
