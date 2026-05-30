import { router } from 'expo-router';
import { useCallback, useEffect, useState } from 'react';
import { FlatList, RefreshControl, StyleSheet, Text } from 'react-native';

import { fetchObras } from '@/api/services';
import type { ObraArte } from '@/api/types';
import { Card, EmptyState, LoadingScreen, ScreenHeader } from '@/components/ui';
import { colors, spacing } from '@/theme/colors';
import { formatCurrency } from '@/utils/format';

export default function ObrasScreen() {
  const [items, setItems] = useState<ObraArte[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    setItems(await fetchObras());
  }, []);

  useEffect(() => {
    load().finally(() => setLoading(false));
  }, [load]);

  if (loading) return <LoadingScreen />;

  return (
    <FlatList
      style={styles.screen}
      data={items}
      keyExtractor={(item) => String(item.id)}
      contentContainerStyle={styles.list}
      ListHeaderComponent={<ScreenHeader title="Obras de Arte" subtitle="Acervo do museu" />}
      ListEmptyComponent={<EmptyState message="Nenhuma obra cadastrada." />}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={async () => {
            setRefreshing(true);
            await load();
            setRefreshing(false);
          }}
          tintColor={colors.primary}
        />
      }
      renderItem={({ item }) => (
        <Card onPress={() => router.push(`/obra/${item.id}`)}>
          <Text style={styles.title}>{item.titulo}</Text>
          <Text style={styles.meta}>{item.tecnica} · {item.ano_criacao}</Text>
          <Text style={styles.value}>{formatCurrency(item.valor_estimado)}</Text>
        </Card>
      )}
    />
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  list: { padding: spacing.md, gap: spacing.sm, flexGrow: 1 },
  title: { fontSize: 17, fontWeight: '700', color: colors.text },
  meta: { color: colors.textMuted, fontSize: 14 },
  value: { color: colors.accent, fontWeight: '700', fontSize: 15 },
});
