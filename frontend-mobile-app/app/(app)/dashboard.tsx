import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { ChartLine as LineChart, ChartBar as BarChart, Target, Utensils, Scale, Activity } from 'lucide-react-native';

export default function Dashboard() {
  return (
    <SafeAreaView style={styles.container}>
      <ScrollView style={styles.scrollView}>
        <View style={styles.header}>
          <Text style={styles.title}>Dashboard</Text>
          <Text style={styles.subtitle}>Track your nutrition progress</Text>
        </View>

        <View style={styles.content}>
          <View style={styles.statsGrid}>
            <View style={[styles.statCard, styles.statCardGreen]}>
              <Target size={24} color="#22c55e" />
              <Text style={styles.statValue}>1,850</Text>
              <Text style={styles.statLabel}>Daily Goal (cal)</Text>
            </View>
            <View style={[styles.statCard, styles.statCardBlue]}>
              <Utensils size={24} color="#6366f1" />
              <Text style={styles.statValue}>1,640</Text>
              <Text style={styles.statLabel}>Consumed (cal)</Text>
            </View>
            <View style={[styles.statCard, styles.statCardPurple]}>
              <Scale size={24} color="#8b5cf6" />
              <Text style={styles.statValue}>68.5</Text>
              <Text style={styles.statLabel}>Weight (kg)</Text>
            </View>
            <View style={[styles.statCard, styles.statCardRed]}>
              <Activity size={24} color="#ef4444" />
              <Text style={styles.statValue}>320</Text>
              <Text style={styles.statLabel}>Burned (cal)</Text>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Weekly Progress</Text>
            <View style={styles.card}>
              <View style={styles.chartHeader}>
                <Text style={styles.chartTitle}>Calorie Intake</Text>
                <LineChart size={20} color="#64748b" />
              </View>
              {/* Placeholder for actual chart */}
              <View style={styles.chartPlaceholder}>
                <Text style={styles.placeholderText}>Chart coming soon</Text>
              </View>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Nutrition Breakdown</Text>
            <View style={styles.card}>
              <View style={styles.chartHeader}>
                <Text style={styles.chartTitle}>Macronutrients</Text>
                <BarChart size={20} color="#64748b" />
              </View>
              <View style={styles.macroStats}>
                <View style={styles.macroItem}>
                  <View style={[styles.macroDot, { backgroundColor: '#22c55e' }]} />
                  <Text style={styles.macroLabel}>Protein</Text>
                  <Text style={styles.macroValue}>25%</Text>
                </View>
                <View style={styles.macroItem}>
                  <View style={[styles.macroDot, { backgroundColor: '#6366f1' }]} />
                  <Text style={styles.macroLabel}>Carbs</Text>
                  <Text style={styles.macroValue}>50%</Text>
                </View>
                <View style={styles.macroItem}>
                  <View style={[styles.macroDot, { backgroundColor: '#ef4444' }]} />
                  <Text style={styles.macroLabel}>Fats</Text>
                  <Text style={styles.macroValue}>25%</Text>
                </View>
              </View>
            </View>
          </View>
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
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    marginHorizontal: -8,
  },
  statCard: {
    width: '50%',
    padding: 8,
  },
  statCardGreen: {
    backgroundColor: '#f0fdf4',
    borderRadius: 20,
    padding: 20,
  },
  statCardBlue: {
    backgroundColor: '#eef2ff',
    borderRadius: 20,
    padding: 20,
  },
  statCardPurple: {
    backgroundColor: '#f5f3ff',
    borderRadius: 20,
    padding: 20,
  },
  statCardRed: {
    backgroundColor: '#fef2f2',
    borderRadius: 20,
    padding: 20,
  },
  statValue: {
    fontSize: 24,
    fontFamily: 'Inter_700Bold',
    color: '#1a1a1a',
    marginTop: 12,
  },
  statLabel: {
    fontSize: 14,
    fontFamily: 'Inter_400Regular',
    color: '#64748b',
    marginTop: 4,
  },
  section: {
    marginTop: 32,
  },
  sectionTitle: {
    fontSize: 20,
    fontFamily: 'Inter_600SemiBold',
    color: '#1a1a1a',
    marginBottom: 16,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 3,
  },
  chartHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  chartTitle: {
    fontSize: 16,
    fontFamily: 'Inter_600SemiBold',
    color: '#1a1a1a',
  },
  chartPlaceholder: {
    height: 200,
    backgroundColor: '#f8fafc',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  placeholderText: {
    color: '#64748b',
    fontFamily: 'Inter_400Regular',
  },
  macroStats: {
    marginTop: 16,
  },
  macroItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  macroDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  macroLabel: {
    flex: 1,
    fontSize: 16,
    fontFamily: 'Inter_400Regular',
    color: '#1a1a1a',
  },
  macroValue: {
    fontSize: 16,
    fontFamily: 'Inter_600SemiBold',
    color: '#1a1a1a',
  },
});