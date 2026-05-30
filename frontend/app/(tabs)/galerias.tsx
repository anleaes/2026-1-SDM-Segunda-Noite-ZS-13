import { router } from 'expo-router';
import { useCallback, useEffect, useState } from 'react';
import { FlatList, RefreshControl, StyleSheet, Text, View } from 'react-native';

import { fetchGalerias } from '@/api/services';
import type { Galeria } from '@/api/types';
import { Badge, Card, EmptyState, LoadingScreen, ScreenHeader } from '@/components/ui';
import { colors, spacing } from '@/theme/colors';

export default function GaleriasScreen() {
  const [items, setItems] = useState<Galeria[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    setItems(await fetchGalerias());
  }, []);

  useEffect(() => {
    load().finally(() => setLoading(false));
  }, [load]);

  if (loading) return <LoadingScreen />;

  return (
    <View style={styles.screen}>
      <FlatList
        data={items}
        keyExtractor={(item) => String(item.id)}
        contentContainerStyle={styles.list}
        ListHeaderComponent={<ScreenHeader title="Galerias" subtitle="Museus e espacos expositivos" />}
        ListEmptyComponent={<EmptyState message="Nenhuma galeria encontrada." />}
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
          <Card onPress={() => router.push(`/galeria/${item.id}`)}>
            <View style={styles.row}>
              <Text style={styles.title}>{item.nome}</Text>
              <Badge label={item.aberta ? 'Aberta' : 'Fechada'} tone={item.aberta ? 'success' : 'warning'} />
            </View>
            <Text style={styles.address} numberOfLines={1}>{item.endereco}</Text>
            <Text style={styles.desc} numberOfLines={2}>{item.descricao}</Text>
          </Card>
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  list: { padding: spacing.md, gap: spacing.sm, flexGrow: 1 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: spacing.sm },
  title: { flex: 1, fontSize: 17, fontWeight: '700', color: colors.text },
  address: { color: colors.accent, fontSize: 13 },
  desc: { color: colors.textMuted, fontSize: 14, lineHeight: 20 },
});
