import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text } from 'react-native';

import { fetchExposicoes, fetchGaleria } from '@/api/services';
import type { Exposicao, Galeria } from '@/api/types';
import { Badge, Card, LoadingScreen } from '@/components/ui';
import { colors, spacing } from '@/theme/colors';
import { formatDate, statusLabel } from '@/utils/format';

export default function GaleriaDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [galeria, setGaleria] = useState<Galeria | null>(null);
  const [exposicoes, setExposicoes] = useState<Exposicao[]>([]);

  useEffect(() => {
    const galeriaId = Number(id);
    Promise.all([fetchGaleria(galeriaId), fetchExposicoes()]).then(([g, exps]) => {
      setGaleria(g);
      setExposicoes(exps.filter((e) => e.galeria === galeriaId));
    });
  }, [id]);

  if (!galeria) return <LoadingScreen />;

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{galeria.nome}</Text>
      <Badge label={galeria.aberta ? 'Aberta ao publico' : 'Fechada'} tone={galeria.aberta ? 'success' : 'warning'} />

      <Card>
        <Text style={styles.label}>Endereco</Text>
        <Text style={styles.text}>{galeria.endereco}</Text>
      </Card>

      <Card>
        <Text style={styles.label}>Descricao</Text>
        <Text style={styles.text}>{galeria.descricao || 'Sem descricao.'}</Text>
      </Card>

      <Card>
        <Text style={styles.label}>Exposicoes nesta galeria ({exposicoes.length})</Text>
        {exposicoes.map((exp) => (
          <Text key={exp.id} style={styles.item}>
            {exp.titulo} · {statusLabel(exp.status)} · {formatDate(exp.data_inicio)}
          </Text>
        ))}
        {!exposicoes.length && <Text style={styles.muted}>Nenhuma exposicao vinculada.</Text>}
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  content: { padding: spacing.md, gap: spacing.md },
  title: { fontSize: 26, fontWeight: '800', color: colors.text },
  label: { fontSize: 13, fontWeight: '700', color: colors.accent, marginBottom: spacing.xs },
  text: { color: colors.text, lineHeight: 22 },
  item: { color: colors.textMuted, fontSize: 14, lineHeight: 22 },
  muted: { color: colors.textMuted, fontStyle: 'italic' },
});
