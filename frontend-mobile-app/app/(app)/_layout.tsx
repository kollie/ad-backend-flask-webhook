import { Tabs } from 'expo-router';
import {
  Chrome as Home,
  User,
  ChartLine as LineChart,
  Book,
} from 'lucide-react-native';
import { BlurView } from 'expo-blur';
import { Platform, StyleSheet } from 'react-native';

export default function AppLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        // Pin the tab bar to the very bottom
        tabBarStyle: {
          ...styles.tabBar,
          // Ensures it's flush to the bottom with no extra white space
          bottom: 0,
        },
        tabBarBackground:
          Platform.OS === 'ios'
            ? () => <BlurView intensity={90} style={styles.blurBackground} />
            : undefined,
        tabBarActiveTintColor: '#16a34a', // Active tab color
        tabBarInactiveTintColor: '#94a3b8', // Inactive tab color
        tabBarLabelStyle: styles.tabBarLabel,
        tabBarItemStyle: styles.tabBarItem,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Predict',
          tabBarIcon: ({ color, size }) => (
            <LineChart size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="meals"
        options={{
          title: 'Meals',
          tabBarIcon: ({ color, size }) => <Book size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="dashboard"
        options={{
          title: 'Dashboard',
          tabBarIcon: ({ color, size }) => <Home size={size} color={color} />,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => <User size={size} color={color} />,
        }}
      />
    </Tabs>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    position: 'absolute',
    // bottom: 0 will remove the extra white space
    // (Instead of "Platform.OS === 'ios' ? 24 : 16")
    left: 16,
    right: 16,
    height: 64,
    borderRadius: 24,
    backgroundColor:
      Platform.OS === 'ios' ? 'rgba(255, 255, 255, 0.85)' : '#fff',
    borderTopWidth: 0,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 4,
  },
  blurBackground: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    borderRadius: 24,
  },
  tabBarLabel: {
    fontSize: 13,
    fontWeight: '600',
    marginBottom: Platform.OS === 'ios' ? 0 : 4,
  },
  tabBarItem: {
    justifyContent: 'center',
    alignItems: 'center',
  },
});
