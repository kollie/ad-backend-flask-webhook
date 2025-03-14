import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  Platform,
  Image,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Picker } from '@react-native-picker/picker';
import { ChartLine as LineChart, Brain, ChevronDown } from 'lucide-react-native';
import { router } from 'expo-router';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';

const API_URL = 'https://kollie.pythonanywhere.com';
const ACTIVITY_LEVELS = ['Sedentary', 'Light', 'Moderate', 'Active', 'Very Active'];
const GOALS = ['Weight Loss', 'Maintenance', 'Muscle Gain'];
const DIETARY_PREFERENCES = ['Balanced', 'Low-carb', 'High-protein', 'Vegetarian', 'Vegan'];

const { width } = Dimensions.get('window');
const inputWidth = width > 768 ? 400 : width - 48;

export default function Home() {
  const { token } = useAuth();
  const [formData, setFormData] = useState({
    age: '',
    gender: 'Male',
    height: '',
    weight: '',
    activity_level: 'Moderate',
    goal: 'Maintenance',
    dietary_preference: 'Balanced',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async () => {
    if (!formData.age || !formData.height || !formData.weight) {
      setError('Please fill in all required fields');
      return;
    }

    try {
      setLoading(true);
      setError('');
      const response = await axios.post(`${API_URL}/predict_food`, formData, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        }
      });
      
      // Navigate to the diet plan screen with the prediction data
      router.push({
        pathname: '/diet-plan',
        params: { prediction: JSON.stringify(response.data) }
      });
    } catch (error) {
      setError('Failed to get prediction. Please try again.');
      console.error('Prediction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Image
            source={{ uri: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80' }}
            style={styles.headerImage}
          />
          <View style={styles.logoContainer}>
            <Brain size={40} color="#22c55e" />
            <Text style={styles.logoText}>Vitality AI</Text>
          </View>
          <Text style={styles.title}>Nutrition Prediction</Text>
          <Text style={styles.subtitle}>Get personalized meal recommendations powered by AI</Text>
        </View>

        <View style={styles.formContainer}>
          {error ? (
            <View style={styles.errorContainer}>
              <Text style={styles.errorText}>{error}</Text>
            </View>
          ) : null}

          <View style={styles.formSection}>
            <Text style={styles.sectionTitle}>Personal Information</Text>
            <View style={styles.inputGroup}>
              <Text style={styles.label}>Age</Text>
              <TextInput
                style={styles.input}
                value={formData.age}
                onChangeText={(value) => setFormData({ ...formData, age: value })}
                keyboardType="numeric"
                placeholder="Enter your age"
                placeholderTextColor="#94a3b8"
              />
            </View>

            <View style={styles.inputGroup}>
              <Text style={styles.label}>Gender</Text>
              <View style={styles.selectContainer}>
                <Picker
                  selectedValue={formData.gender}
                  onValueChange={(value) => setFormData({ ...formData, gender: value })}
                  style={[styles.picker, { color: '#1a1a1a' }]}>
                  <Picker.Item label="Male" value="Male" />
                  <Picker.Item label="Female" value="Female" />
                </Picker>
                <ChevronDown size={20} color="#64748b" style={styles.selectIcon} />
              </View>
            </View>

            <View style={styles.row}>
              <View style={[styles.inputGroup, styles.halfWidth]}>
                <Text style={styles.label}>Height (cm)</Text>
                <TextInput
                  style={styles.input}
                  value={formData.height}
                  onChangeText={(value) => setFormData({ ...formData, height: value })}
                  keyboardType="numeric"
                  placeholder="Height"
                  placeholderTextColor="#94a3b8"
                />
              </View>

              <View style={[styles.inputGroup, styles.halfWidth]}>
                <Text style={styles.label}>Weight (kg)</Text>
                <TextInput
                  style={styles.input}
                  value={formData.weight}
                  onChangeText={(value) => setFormData({ ...formData, weight: value })}
                  keyboardType="numeric"
                  placeholder="Weight"
                  placeholderTextColor="#94a3b8"
                />
              </View>
            </View>
          </View>

          <View style={styles.formSection}>
            <Text style={styles.sectionTitle}>Preferences</Text>
            <View style={styles.inputGroup}>
              <Text style={styles.label}>Activity Level</Text>
              <View style={styles.selectContainer}>
                <Picker
                  selectedValue={formData.activity_level}
                  onValueChange={(value) => setFormData({ ...formData, activity_level: value })}
                  style={[styles.picker, { color: '#1a1a1a' }]}>
                  {ACTIVITY_LEVELS.map((level) => (
                    <Picker.Item key={level} label={level} value={level} />
                  ))}
                </Picker>
                <ChevronDown size={20} color="#64748b" style={styles.selectIcon} />
              </View>
            </View>

            <View style={styles.inputGroup}>
              <Text style={styles.label}>Goal</Text>
              <View style={styles.selectContainer}>
                <Picker
                  selectedValue={formData.goal}
                  onValueChange={(value) => setFormData({ ...formData, goal: value })}
                  style={[styles.picker, { color: '#1a1a1a' }]}>
                  {GOALS.map((goal) => (
                    <Picker.Item key={goal} label={goal} value={goal} />
                  ))}
                </Picker>
                <ChevronDown size={20} color="#64748b" style={styles.selectIcon} />
              </View>
            </View>

            <View style={styles.inputGroup}>
              <Text style={styles.label}>Dietary Preference</Text>
              <View style={styles.selectContainer}>
                <Picker
                  selectedValue={formData.dietary_preference}
                  onValueChange={(value) => setFormData({ ...formData, dietary_preference: value })}
                  style={[styles.picker, { color: '#1a1a1a' }]}>
                  {DIETARY_PREFERENCES.map((pref) => (
                    <Picker.Item key={pref} label={pref} value={pref} />
                  ))}
                </Picker>
                <ChevronDown size={20} color="#64748b" style={styles.selectIcon} />
              </View>
            </View>
          </View>

          <TouchableOpacity
            style={[styles.button, loading && styles.buttonDisabled]}
            onPress={handleSubmit}
            disabled={loading}>
            <LineChart size={24} color="#fff" style={styles.buttonIcon} />
            <Text style={styles.buttonText}>
              {loading ? 'Analyzing...' : 'Get Personalized Plan'}
            </Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  scrollView: {
    flex: 1,
  },
  header: {
    position: 'relative',
    paddingTop: 120,
    paddingBottom: 32,
    paddingHorizontal: 24,
    backgroundColor: '#fff',
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
  },
  headerImage: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 200,
    opacity: 0.15,
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  logoText: {
    fontSize: 24,
    fontFamily: 'Inter_700Bold',
    color: '#22c55e',
    marginLeft: 12,
  },
  title: {
    fontSize: 32,
    fontFamily: 'Inter_700Bold',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    fontFamily: 'Inter_400Regular',
  },
  formContainer: {
    alignItems: 'center',
    padding: 24,
  },
  formSection: {
    width: inputWidth,
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 24,
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 20,
    fontFamily: 'Inter_600SemiBold',
    color: '#1a1a1a',
    marginBottom: 20,
  },
  errorContainer: {
    width: inputWidth,
    backgroundColor: '#fef2f2',
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
    borderWidth: 1,
    borderColor: '#fee2e2',
  },
  errorText: {
    color: '#ef4444',
    fontFamily: 'Inter_400Regular',
  },
  row: {
    flexDirection: 'row',
    marginHorizontal: -8,
  },
  halfWidth: {
    flex: 1,
    marginHorizontal: 8,
  },
  inputGroup: {
    marginBottom: 20,
  },
  label: {
    fontSize: 14,
    marginBottom: 8,
    color: '#334155',
    fontFamily: 'Inter_600SemiBold',
  },
  input: {
    backgroundColor: '#f8fafc',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 12,
    fontSize: 16,
    borderWidth: 2,
    borderColor: '#e2e8f0',
    fontFamily: 'Inter_400Regular',
    color: '#1a1a1a',
  },
  selectContainer: {
    position: 'relative',
    backgroundColor: '#f8fafc',
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#e2e8f0',
    overflow: 'hidden',
  },
  picker: {
    ...Platform.select({
      ios: {
        margin: -8,
      },
      android: {
        paddingHorizontal: 8,
      },
    }),
  },
  selectIcon: {
    position: 'absolute',
    right: 12,
    top: '50%',
    transform: [{ translateY: -10 }],
  },
  button: {
    width: inputWidth,
    backgroundColor: '#22c55e',
    padding: 16,
    borderRadius: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
    shadowColor: '#22c55e',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 12,
    elevation: 4,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonIcon: {
    marginRight: 12,
  },
  buttonText: {
    color: '#fff',
    fontSize: 18,
    fontFamily: 'Inter_600SemiBold',
  },
  predictionContainer: {
    width: inputWidth,
    marginTop: 24,
    padding: 24,
    backgroundColor: '#fff',
    borderRadius: 24,
    borderWidth: 1,
    borderColor: '#e2e8f0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  predictionTitle: {
    fontSize: 20,
    fontFamily: 'Inter_700Bold',
    color: '#1a1a1a',
    marginBottom: 16,
  },
  predictionText: {
    fontSize: 16,
    fontFamily: 'Inter_400Regular',
    color: '#334155',
    lineHeight: 24,
  },
});