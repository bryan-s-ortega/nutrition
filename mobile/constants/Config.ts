// For web, localhost works fine.
// For Android Emulator, use 'http://10.0.2.2:8000'
// For iOS Simulator, use 'http://127.0.0.1:8000'
// For physical device, use your machine's LAN IP.

import { Platform } from 'react-native';

const getBaseUrl = () => {
    if (Platform.OS === 'web') {
        return 'http://localhost:8000';
    } else if (Platform.OS === 'android') {
        return 'http://10.0.2.2:8000';
    } else {
        return 'http://127.0.0.1:8000';
    }
}

export const API_URL = getBaseUrl();
