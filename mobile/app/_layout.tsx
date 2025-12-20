import { Stack } from 'expo-router/stack';

export default function Layout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Welcome' }} />
      <Stack.Screen name="onboarding" options={{ title: 'Setup Profile' }} />
      <Stack.Screen name="plan" options={{ title: 'Your Meal Plan' }} />
    </Stack>
  );
}
