import React, { useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useLocalSearchParams } from 'expo-router';
import Animated, { 
  useAnimatedStyle, 
  withSpring,
  withSequence,
  withDelay,
  useSharedValue,
  runOnJS
} from 'react-native-reanimated';
import ConfettiCannon from 'react-native-confetti-cannon';
import { Brain } from 'lucide-react-native';

const { width } = Dimensions.get('window');

export default function DietPlan() {
  const params = useLocalSearchParams();
  const prediction = params.prediction ? JSON.parse(params.prediction as string) : null;
  const scale = useSharedValue(0);
  const opacity = useSharedValue(0);
  const [showConfetti, setShowConfetti] = React.useState(false);

  useEffect(() => {
    scale.value = withSequence(
      withSpring(1.2),
      withDelay(100, withSpring(1))
    );
    opacity.value = withSpring(1);
    
    // Delay confetti slightly for better effect
    setTimeout(() => {
      setShowConfetti(true);
    }, 500);
  }, []);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
    opacity: opacity.value,
  }));

  if (!prediction) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>No diet plan data available</Text>
        </View>
      </SafeAreaView>
    );
  }

  // Extract just the diet name from the prediction
  const dietName = prediction.predicted_diet.replace('predicted_diet: ', '');

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.content}>
        {showConfetti && (
          <ConfettiCannon
            count={200}
            origin={{ x: width / 2, y: -10 }}
            autoStart={true}
            fadeOut={true}
          />
        )}
        
        <View style={styles.iconContainer}>
          <Brain size={64} color="#22c55e" />
        </View>

        <Text style={styles.title}>Your Recommended Diet Plan</Text>
        
        <Animated.View style={[styles.resultContainer, animatedStyle]}>
          <Text style={styles.dietText}>{dietName}</Text>
        </Animated.View>

        <Text style={styles.subtitle}>
          Based on your profile and preferences, this diet plan would be the most suitable for achieving your goals.
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 24,
  },
  iconContainer: {
    marginBottom: 24,
  },
  title: {
    fontSize: 28,
    fontFamily: 'Inter_700Bold',
    color: '#1a1a1a',
    textAlign: 'center',
    marginBottom: 24,
  },
  resultContainer: {
    backgroundColor: '#22c55e',
    paddingVertical: 20,
    paddingHorizontal: 40,
    borderRadius: 20,
    shadowColor: '#22c55e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 8,
    marginBottom: 24,
  },
  dietText: {
    fontSize: 32,
    fontFamily: 'Inter_700Bold',
    color: '#ffffff',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 16,
    fontFamily: 'Inter_400Regular',
    color: '#64748b',
    textAlign: 'center',
    maxWidth: 400,
    lineHeight: 24,
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  errorText: {
    fontSize: 16,
    fontFamily: 'Inter_400Regular',
    color: '#ef4444',
  },
});