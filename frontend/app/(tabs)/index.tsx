import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { useCallback, useEffect, useState } from 'react';
import { RefreshControl, ScrollView, StyleSheet, Text, View } from 'react-native';

import { fetchDashboardCounts } from '@/api/services';
import { Card, LoadingScreen, ScreenHeader } from '@/components/ui';
import { useAuth } from '@/context/AuthContext';
import { colors, radius, spacing } from '@/theme/colors';
import { roleLabel } from '@/utils/format';

export default function HomeScreen() {
  const { user } = useAuth();
  const [counts, setCounts] = useState({ galerias: 0, obras: 0, exposicoes: 0 });
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    const data = await fetchDashboardCounts();
    setCounts(data);
  }, []);

  useEffect(() => {
    load().finally(() => setLoading(false));
  }, [load]);

  async function onRefresh() {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  }

  if (loading) return <LoadingScreen />;

  const shortcuts = [
    { label: 'Galerias', count: counts.galerias, route: '/(tabs)/galerias', icon: 'business' as const },
    { label: 'Obras', count: counts.obras, route: '/(tabs)/obras', icon: 'image' as const },
    { label: 'Exposicoes', count: counts.exposicoes, route: '/(tabs)/exposicoes', icon: 'calendar' as const },
  ];

  return (
    <ScrollView
      style={styles.screen}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
    >
      <ScreenHeader
        title={`Ola, ${user?.first_name || user?.username}!`}
        subtitle={`Perfil: ${roleLabel(user?.role ?? '')}`}
      />

      <View style={styles.stats}>
        {shortcuts.map((item) => (
          <Card key={item.label} onPress={() => router.push(item.route)} style={styles.statCard}>
            <Ionicons name={item.icon} size={24} color={colors.primary} />
            <Text style={styles.statNumber}>{item.count}</Text>
            <Text style={styles.statLabel}>{item.label}</Text>
          </Card>
        ))}
      </View>

      <Card>
        <Text style={styles.cardTitle}>Sobre o app</Text>
        <Text style={styles.cardText}>
          App mobile conectado a API Django do projeto Museu & Galeria. Explore galerias, obras e
          exposicoes. Como visitante, compre ingressos, faca reservas e avalie exposicoes.
        </Text>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  content: { padding: spacing.md, gap: spacing.md },
  stats: { flexDirection: 'row', gap: spacing.sm },
  statCard: { flex: 1, alignItems: 'center', paddingVertical: spacing.lg },
  statNumber: { fontSize: 24, fontWeight: '800', color: colors.text },
  statLabel: { color: colors.textMuted, fontSize: 12 },
  cardTitle: { fontSize: 16, fontWeight: '700', color: colors.text },
  cardText: { color: colors.textMuted, lineHeight: 22, fontSize: 14 },
});
