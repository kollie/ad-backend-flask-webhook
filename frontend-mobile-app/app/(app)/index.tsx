import React, { useState, useEffect } from 'react';
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
  Keyboard,
  KeyboardAvoidingView,
  TouchableWithoutFeedback,
  StatusBar,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Picker } from '@react-native-picker/picker';
import {
  ChartLine as LineChart,
  Brain,
  ChevronDown,
  Dumbbell,
  Heart,
  Apple,
} from 'lucide-react-native';
import { router } from 'expo-router';
import axios from 'axios';
import { useAuth } from '@/context/AuthContext';

const API_URL = 'https://kollie.pythonanywhere.com';
const ACTIVITY_LEVELS = [
  'Sedentary',
  'Light',
  'Moderate',
  'Active',
  'Very Active',
];
const GOALS = ['Weight Loss', 'Maintenance', 'Muscle Gain'];
const DIETARY_PREFERENCES = [
  'Light',
  'Balanced',
  'Low-carb',
  'High-protein',
  'Vegetarian',
  'Vegan',
];

const { width, height } = Dimensions.get('window');
const inputWidth = width > 768 ? 400 : width - 48;

export default function Home() {
  const { token, userId } = useAuth();
  const [formData, setFormData] = useState({
    user_id: null,
    age: '',
    gender: 'Male',
    height: '',
    weight: '',
    activity_level: 'Moderate',
    goal: 'Maintenance',
    dietary_preference: 'Light',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [activeSection, setActiveSection] = useState('personal');

  useEffect(() => {
    if (userId) {
      setFormData((prev) => ({ ...prev, user_id: userId }));
    }
  }, [userId]);

  const trainModel = async () => {
    try {
      await axios.post(`${API_URL}/train_model`, null, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
    } catch (error) {
      console.error('Error training model:', error);
      // Continue with the flow even if training fails
    }
  };

  const getPrediction = async () => {
    try {
      const response = await axios.post(`${API_URL}/predict_food`, null, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error getting prediction:', error);
      throw error;
    }
  };

  const handleSubmit = async () => {
    if (!formData.age || !formData.height || !formData.weight) {
      setError('Please fill in all required fields');
      return;
    }

    if (!formData.user_id) {
      setError('User ID is required. Please try logging in again.');
      return;
    }

    try {
      setLoading(true);
      setError('');

      // Step 1: Submit diet data
      const dietResponse = await axios.post(`${API_URL}/diet`, formData, {
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${token}`,
        },
      });

      // Step 2: Train the model
      await trainModel();

      // Step 3: Get prediction
      const prediction = await getPrediction();

      // Step 4: Navigate to diet plan with prediction data
      router.push({
        pathname: 'diet-plan',
        params: { prediction: JSON.stringify(prediction) },
      });
    } catch (error) {
      setError('Failed to process your request. Please try again.');
      console.error('Prediction failed:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderSectionIndicator = () => (
    <View style={styles.sectionIndicator}>
      <TouchableOpacity
        style={[
          styles.indicatorDot,
          activeSection === 'personal' && styles.indicatorActive,
        ]}
        onPress={() => setActiveSection('personal')}
      >
        <Text
          style={[
            styles.indicatorText,
            activeSection === 'personal' && styles.indicatorTextActive,
          ]}
        >
          1
        </Text>
      </TouchableOpacity>
      <View style={styles.indicatorLine} />
      <TouchableOpacity
        style={[
          styles.indicatorDot,
          activeSection === 'preferences' && styles.indicatorActive,
        ]}
        onPress={() => setActiveSection('preferences')}
      >
        <Text
          style={[
            styles.indicatorText,
            activeSection === 'preferences' && styles.indicatorTextActive,
          ]}
        >
          2
        </Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="dark-content" backgroundColor="#fff" />
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.flex}
      >
        <TouchableWithoutFeedback onPress={Keyboard.dismiss}>
          <ScrollView
            contentContainerStyle={styles.scrollContainer}
            keyboardShouldPersistTaps="handled"
            showsVerticalScrollIndicator={false}
          >
            <View style={styles.header}>
              <Image
                source={{
                  uri: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061?auto=format&fit=crop&w=800&q=80',
                }}
                style={styles.headerImage}
              />
              <View style={styles.headerOverlay} />
              <View style={styles.logoContainer}>
                <Brain size={44} color="#22c55e" />
                <Text style={styles.logoText}>Vitality AI</Text>
              </View>
              <Text style={styles.title}>Nutrition Prediction</Text>
              <Text style={styles.subtitle}>
                Get personalized meal recommendations powered by AI
              </Text>
            </View>

            {renderSectionIndicator()}

            <View style={styles.formContainer}>
              {error ? (
                <View style={styles.errorContainer}>
                  <Text style={styles.errorText}>{error}</Text>
                </View>
              ) : null}

              {activeSection === 'personal' ? (
                <View style={styles.formSection}>
                  <View style={styles.sectionHeader}>
                    <Heart size={24} color="#22c55e" />
                    <Text style={styles.sectionTitle}>
                      Personal Information
                    </Text>
                  </View>

                  <View style={styles.inputGroup}>
                    <Text style={styles.label}>Age</Text>
                    <TextInput
                      style={styles.input}
                      value={formData.age}
                      onChangeText={(value) =>
                        setFormData({ ...formData, age: value })
                      }
                      keyboardType="numeric"
                      placeholder="Enter your age"
                      placeholderTextColor="#94a3b8"
                      maxLength={3}
                    />
                  </View>

                  <View style={styles.inputGroup}>
                    <Text style={styles.label}>Gender</Text>
                    <View style={styles.genderSelector}>
                      <TouchableOpacity
                        style={[
                          styles.genderOption,
                          formData.gender === 'Male' &&
                            styles.genderOptionSelected,
                        ]}
                        onPress={() =>
                          setFormData({ ...formData, gender: 'Male' })
                        }
                      >
                        <Text
                          style={[
                            styles.genderOptionText,
                            formData.gender === 'Male' &&
                              styles.genderOptionTextSelected,
                          ]}
                        >
                          Male
                        </Text>
                      </TouchableOpacity>
                      <TouchableOpacity
                        style={[
                          styles.genderOption,
                          formData.gender === 'Female' &&
                            styles.genderOptionSelected,
                        ]}
                        onPress={() =>
                          setFormData({ ...formData, gender: 'Female' })
                        }
                      >
                        <Text
                          style={[
                            styles.genderOptionText,
                            formData.gender === 'Female' &&
                              styles.genderOptionTextSelected,
                          ]}
                        >
                          Female
                        </Text>
                      </TouchableOpacity>
                    </View>
                  </View>

                  <View style={styles.row}>
                    <View style={[styles.inputGroup, styles.halfWidth]}>
                      <Text style={styles.label}>Height (cm)</Text>
                      <TextInput
                        style={styles.input}
                        value={formData.height}
                        onChangeText={(value) =>
                          setFormData({ ...formData, height: value })
                        }
                        keyboardType="numeric"
                        placeholder="Height"
                        placeholderTextColor="#94a3b8"
                        maxLength={3}
                      />
                    </View>

                    <View style={[styles.inputGroup, styles.halfWidth]}>
                      <Text style={styles.label}>Weight (kg)</Text>
                      <TextInput
                        style={styles.input}
                        value={formData.weight}
                        onChangeText={(value) =>
                          setFormData({ ...formData, weight: value })
                        }
                        keyboardType="numeric"
                        placeholder="Weight"
                        placeholderTextColor="#94a3b8"
                        maxLength={3}
                      />
                    </View>
                  </View>

                  <TouchableOpacity
                    style={styles.nextButton}
                    onPress={() => setActiveSection('preferences')}
                  >
                    <Text style={styles.nextButtonText}>Next</Text>
                    <ChevronDown
                      size={20}
                      color="#fff"
                      style={{ transform: [{ rotate: '-90deg' }] }}
                    />
                  </TouchableOpacity>
                </View>
              ) : (
                <View style={styles.formSection}>
                  <View style={styles.sectionHeader}>
                    <Dumbbell size={24} color="#22c55e" />
                    <Text style={styles.sectionTitle}>Fitness Goals</Text>
                  </View>

                  <View style={styles.inputGroup}>
                    <Text style={styles.label}>Activity Level</Text>
                    <View style={styles.selectContainer}>
                      <Picker
                        selectedValue={formData.activity_level}
                        onValueChange={(value) =>
                          setFormData({ ...formData, activity_level: value })
                        }
                        style={styles.picker}
                      >
                        {ACTIVITY_LEVELS.map((level) => (
                          <Picker.Item
                            key={level}
                            label={level}
                            value={level}
                            color="#1a1a1a"
                          />
                        ))}
                      </Picker>
                    </View>
                  </View>

                  <View style={styles.inputGroup}>
                    <Text style={styles.label}>Goal</Text>
                    <View style={styles.goalSelector}>
                      {GOALS.map((goal) => (
                        <TouchableOpacity
                          key={goal}
                          style={[
                            styles.goalOption,
                            formData.goal === goal && styles.goalOptionSelected,
                          ]}
                          onPress={() => setFormData({ ...formData, goal })}
                        >
                          <Text
                            style={[
                              styles.goalOptionText,
                              formData.goal === goal &&
                                styles.goalOptionTextSelected,
                            ]}
                          >
                            {goal}
                          </Text>
                        </TouchableOpacity>
                      ))}
                    </View>
                  </View>

                  <View style={styles.inputGroup}>
                    <Text style={styles.label}>Dietary Preference</Text>
                    <View style={styles.dietarySelector}>
                      {DIETARY_PREFERENCES.map((pref) => (
                        <TouchableOpacity
                          key={pref}
                          style={[
                            styles.dietaryOption,
                            formData.dietary_preference === pref &&
                              styles.dietaryOptionSelected,
                          ]}
                          onPress={() =>
                            setFormData({
                              ...formData,
                              dietary_preference: pref,
                            })
                          }
                        >
                          <Apple
                            size={20}
                            color={
                              formData.dietary_preference === pref
                                ? '#fff'
                                : '#64748b'
                            }
                          />
                          <Text
                            style={[
                              styles.dietaryOptionText,
                              formData.dietary_preference === pref &&
                                styles.dietaryOptionTextSelected,
                            ]}
                          >
                            {pref}
                          </Text>
                        </TouchableOpacity>
                      ))}
                    </View>
                  </View>

                  <View style={styles.buttonContainer}>
                    <TouchableOpacity
                      style={styles.backButton}
                      onPress={() => setActiveSection('personal')}
                    >
                      <ChevronDown
                        size={20}
                        color="#22c55e"
                        style={{ transform: [{ rotate: '90deg' }] }}
                      />
                      <Text style={styles.backButtonText}>Back</Text>
                    </TouchableOpacity>

                    <TouchableOpacity
                      style={[
                        styles.submitButton,
                        loading && styles.buttonDisabled,
                      ]}
                      onPress={handleSubmit}
                      disabled={loading}
                    >
                      {loading ? (
                        <ActivityIndicator color="#fff" />
                      ) : (
                        <>
                          <LineChart
                            size={24}
                            color="#fff"
                            style={styles.buttonIcon}
                          />
                          <Text style={styles.submitButtonText}>
                            Get Your Plan
                          </Text>
                        </>
                      )}
                    </TouchableOpacity>
                  </View>
                </View>
              )}
            </View>
          </ScrollView>
        </TouchableWithoutFeedback>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8fafc',
  },
  flex: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
  },
  header: {
    position: 'relative',
    paddingTop: 60,
    paddingBottom: 32,
    paddingHorizontal: 24,
    backgroundColor: '#fff',
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
    overflow: 'hidden',
  },
  headerImage: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 200,
  },
  headerOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 200,
    backgroundColor: 'rgba(255, 255, 255, 0.9)',
  },
  logoContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
  },
  logoText: {
    fontSize: 28,
    fontWeight: '800',
    color: '#22c55e',
    marginLeft: 12,
  },
  title: {
    fontSize: 36,
    fontWeight: '800',
    color: '#1a1a1a',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#64748b',
    fontWeight: '500',
    lineHeight: 24,
  },
  sectionIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 24,
  },
  indicatorDot: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#f1f5f9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  indicatorActive: {
    backgroundColor: '#22c55e',
  },
  indicatorText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#64748b',
  },
  indicatorTextActive: {
    color: '#fff',
  },
  indicatorLine: {
    width: 60,
    height: 2,
    backgroundColor: '#e2e8f0',
    marginHorizontal: 8,
  },
  formContainer: {
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingBottom: 24,
  },
  formSection: {
    width: inputWidth,
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 8,
    elevation: 2,
  },
  sectionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: '700',
    color: '#1a1a1a',
    marginLeft: 12,
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
    fontWeight: '500',
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
    fontWeight: '600',
  },
  input: {
    backgroundColor: '#f8fafc',
    paddingHorizontal: 16,
    paddingVertical: 14,
    borderRadius: 12,
    fontSize: 16,
    borderWidth: 2,
    borderColor: '#e2e8f0',
    fontWeight: '500',
    color: '#1a1a1a',
  },
  genderSelector: {
    flexDirection: 'row',
    backgroundColor: '#f8fafc',
    borderRadius: 12,
    padding: 4,
  },
  genderOption: {
    flex: 1,
    paddingVertical: 12,
    alignItems: 'center',
    borderRadius: 8,
  },
  genderOptionSelected: {
    backgroundColor: '#22c55e',
  },
  genderOptionText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#64748b',
  },
  genderOptionTextSelected: {
    color: '#fff',
  },
  selectContainer: {
    backgroundColor: '#f8fafc',
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#e2e8f0',
    overflow: 'hidden',
  },
  picker: {
    width: '100%',
  },
  goalSelector: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -4,
  },
  goalOption: {
    flex: 1,
    margin: 4,
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: '#f8fafc',
    alignItems: 'center',
  },
  goalOptionSelected: {
    backgroundColor: '#22c55e',
  },
  goalOptionText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#64748b',
  },
  goalOptionTextSelected: {
    color: '#fff',
  },
  dietarySelector: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -4,
  },
  dietaryOption: {
    flexDirection: 'row',
    alignItems: 'center',
    margin: 4,
    paddingVertical: 12,
    paddingHorizontal: 16,
    borderRadius: 12,
    backgroundColor: '#f8fafc',
  },
  dietaryOptionSelected: {
    backgroundColor: '#22c55e',
  },
  dietaryOptionText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#64748b',
    marginLeft: 8,
  },
  dietaryOptionTextSelected: {
    color: '#fff',
  },
  buttonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginTop: 24,
  },
  nextButton: {
    backgroundColor: '#22c55e',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 24,
    borderRadius: 16,
    marginTop: 24,
  },
  nextButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginRight: 8,
  },
  backButton: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 16,
    paddingHorizontal: 24,
  },
  backButtonText: {
    color: '#22c55e',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  submitButton: {
    backgroundColor: '#22c55e',
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 16,
    flex: 1,
    marginLeft: 16,
  },
  submitButtonText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonIcon: {
    marginRight: 8,
  },
});
