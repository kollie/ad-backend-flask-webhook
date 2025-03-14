import React from 'react';
import { View, Text, StyleSheet, ScrollView, Image, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Clock, Flame, Scale } from 'lucide-react-native';

const MEAL_SUGGESTIONS = [
  {
    id: 1,
    name: 'Quinoa Buddha Bowl',
    image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80',
    calories: 450,
    time: '25 min',
    weight: '380g',
    category: 'Lunch',
  },
  {
    id: 2,
    name: 'Berry Protein Smoothie',
    image: 'https://images.unsplash.com/photo-1623065422902-30a2d299bbe4?auto=format&fit=crop&w=800&q=80',
    calories: 280,
    time: '5 min',
    weight: '300ml',
    category: 'Breakfast',
  },
  {
    id: 3,
    name: 'Grilled Salmon Bowl',
    image: 'https://images.unsplash.com/photo-1467003909585-2f8a72700288?auto=format&fit=crop&w=800&q=80',
    calories: 520,
    time: '30 min',
    weight: '400g',
    category: 'Dinner',
  },
];

export default function Meals() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.title}>Meal Suggestions</Text>
          <Text style={styles.subtitle}>Healthy and delicious recipes curated for you</Text>
        </View>

        <View style={styles.content}>
          {MEAL_SUGGESTIONS.map((meal) => (
            <TouchableOpacity key={meal.id} style={styles.mealCard}>
              <Image source={{ uri: meal.image }} style={styles.mealImage} />
              <View style={styles.mealInfo}>
                <View style={styles.categoryBadge}>
                  <Text style={styles.categoryText}>{meal.category}</Text>
                </View>
                <Text style={styles.mealName}>{meal.name}</Text>
                <View style={styles.mealStats}>
                  <View style={styles.statItem}>
                    <Flame size={16} color="#ef4444" />
                    <Text style={styles.statText}>{meal.calories} cal</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Clock size={16} color="#6366f1" />
                    <Text style={styles.statText}>{meal.time}</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Scale size={16} color="#22c55e" />
                    <Text style={styles.statText}>{meal.weight}</Text>
                  </View>
                </View>
              </View>
            </TouchableOpacity>
          ))}
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
    padding: 24,
    backgroundColor: '#fff',
    borderBottomLeftRadius: 32,
    borderBottomRightRadius: 32,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 5,
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
  content: {
    padding: 24,
  },
  mealCard: {
    backgroundColor: '#fff',
    borderRadius: 24,
    marginBottom: 24,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  mealImage: {
    width: '100%',
    height: 200,
  },
  mealInfo: {
    padding: 20,
  },
  categoryBadge: {
    backgroundColor: '#f0fdf4',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
    alignSelf: 'flex-start',
    marginBottom: 12,
  },
  categoryText: {
    color: '#22c55e',
    fontSize: 14,
    fontFamily: 'Inter_600SemiBold',
  },
  mealName: {
    fontSize: 20,
    fontFamily: 'Inter_700Bold',
    color: '#1a1a1a',
    marginBottom: 12,
  },
  mealStats: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
  },
  statItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 20,
  },
  statText: {
    marginLeft: 6,
    color: '#64748b',
    fontSize: 14,
    fontFamily: 'Inter_400Regular',
  },
});