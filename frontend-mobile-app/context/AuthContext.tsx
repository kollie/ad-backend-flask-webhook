import React, { createContext, useContext, useState, useEffect } from 'react';
import { router, useSegments } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';
import axios from 'axios';

interface AuthContextType {
  signIn: (token: string, userId: number) => Promise<void>;
  signOut: () => Promise<void>;
  isAuthenticated: boolean;
  token: string | null;
  userId: number | null;
}

const storage = {
  async setItem(key: string, value: string) {
    if (Platform.OS === 'web') {
      localStorage.setItem(key, value);
      return;
    }
    return SecureStore.setItemAsync(key, value);
  },
  async getItem(key: string) {
    if (Platform.OS === 'web') {
      return localStorage.getItem(key);
    }
    return SecureStore.getItemAsync(key);
  },
  async removeItem(key: string) {
    if (Platform.OS === 'web') {
      localStorage.removeItem(key);
      return;
    }
    return SecureStore.deleteItemAsync(key);
  },
};

const AuthContext = createContext<AuthContextType>({
  signIn: async () => {},
  signOut: async () => {},
  isAuthenticated: false,
  token: null,
  userId: null,
});

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const [userId, setUserId] = useState<number | null>(null);
  const segments = useSegments();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const [storedToken, storedUserId] = await Promise.all([
          storage.getItem('token'),
          storage.getItem('userId'),
        ]);

        if (storedToken && storedUserId) {
          setToken(storedToken);
          setUserId(Number(storedUserId));
          axios.defaults.headers.common[
            'Authorization'
          ] = `Bearer ${storedToken}`;
          setIsAuthenticated(true);
        }
      } catch (error) {
        console.warn('Error checking authentication:', error);
      }
    };
    checkAuth();
  }, []);

  useEffect(() => {
    const inAuthGroup = segments[0] === '(auth)';

    if (!isAuthenticated && !inAuthGroup) {
      router.replace('/login');
    } else if (isAuthenticated && inAuthGroup) {
      router.replace('/');
    }
  }, [isAuthenticated, segments]);

  const signIn = async (token: string, userId: number) => {
    if (!token || !userId) {
      throw new Error('Token and user ID are required');
    }

    try {
      await Promise.all([
        storage.setItem('token', token),
        storage.setItem('userId', String(userId)),
      ]);

      setToken(token);
      setUserId(userId);
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      setIsAuthenticated(true);
    } catch (error) {
      console.error('Error storing authentication data:', error);
      throw new Error('Failed to sign in');
    }
  };

  const signOut = async () => {
    try {
      await Promise.all([
        storage.removeItem('token'),
        storage.removeItem('userId'),
      ]);
      setToken(null);
      setUserId(null);
      delete axios.defaults.headers.common['Authorization'];
      setIsAuthenticated(false);
    } catch (error) {
      console.error('Error removing authentication data:', error);
      throw new Error('Failed to sign out');
    }
  };

  return (
    <AuthContext.Provider
      value={{
        signIn,
        signOut,
        isAuthenticated,
        token,
        userId,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => useContext(AuthContext);
