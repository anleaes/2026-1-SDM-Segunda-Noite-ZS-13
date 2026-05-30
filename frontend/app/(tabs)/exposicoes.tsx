import { router } from 'expo-router';
import { useCallback, useEffect, useState } from 'react';
import { FlatList, RefreshControl, StyleSheet, Text, View } from 'react-native';

import { fetchExposicoes } from '@/api/services';
import type { Exposicao } from '@/api/types';
import { Badge, Card, EmptyState, LoadingScreen, ScreenHeader } from '@/components/ui';
import { colors, spacing } from '@/theme/colors';
import { formatDate, statusLabel } from '@/utils/format';

export default function ExposicoesScreen() {
  const [items, setItems] = useState<Exposicao[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    setItems(await fetchExposicoes());
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
      ListHeaderComponent={<ScreenHeader title="Exposicoes" subtitle="Mostras e eventos" />}
      ListEmptyComponent={<EmptyState message="Nenhuma exposicao encontrada." />}
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
        <Card onPress={() => router.push(`/exposicao/${item.id}`)}>
          <View style={styles.row}>
            <Text style={styles.title}>{item.titulo}</Text>
            <Badge label={statusLabel(item.status)} />
          </View>
          <Text style={styles.dates}>
            {formatDate(item.data_inicio)} — {formatDate(item.data_fim)}
          </Text>
          <Text style={styles.desc} numberOfLines={2}>{item.descricao}</Text>
        </Card>
      )}
    />
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  list: { padding: spacing.md, gap: spacing.sm, flexGrow: 1 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: spacing.sm },
  title: { flex: 1, fontSize: 17, fontWeight: '700', color: colors.text },
  dates: { color: colors.accent, fontSize: 13 },
  desc: { color: colors.textMuted, fontSize: 14, lineHeight: 20 },
});
