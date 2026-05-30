import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { ScrollView, StyleSheet, Text } from 'react-native';

import { apiGet } from '@/api/client';
import { fetchObra } from '@/api/services';
import type { Certificado, ObraArte, PaginatedResponse } from '@/api/types';
import { Card, LoadingScreen } from '@/components/ui';
import { colors, spacing } from '@/theme/colors';
import { formatCurrency, formatDate } from '@/utils/format';

export default function ObraDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [obra, setObra] = useState<ObraArte | null>(null);
  const [certificado, setCertificado] = useState<Certificado | null>(null);

  useEffect(() => {
    const obraId = Number(id);
    fetchObra(obraId).then(setObra);
    apiGet<PaginatedResponse<Certificado>>('/certificados/', { obra: String(obraId) }).then((data) => {
      setCertificado(data.results[0] ?? null);
    });
  }, [id]);

  if (!obra) return <LoadingScreen />;

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{obra.titulo}</Text>
      <Text style={styles.value}>{formatCurrency(obra.valor_estimado)}</Text>

      <Card>
        <Text style={styles.label}>Tecnica</Text>
        <Text style={styles.text}>{obra.tecnica}</Text>
      </Card>

      <Card>
        <Text style={styles.label}>Ano de criacao</Text>
        <Text style={styles.text}>{obra.ano_criacao}</Text>
      </Card>

      {certificado && (
        <Card>
          <Text style={styles.label}>Certificado de autenticidade</Text>
          <Text style={styles.text}>Codigo: {certificado.codigo}</Text>
          <Text style={styles.text}>Emissao: {formatDate(certificado.data_emissao)}</Text>
          <Text style={styles.text}>Orgao: {certificado.orgao_responsavel}</Text>
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  content: { padding: spacing.md, gap: spacing.md },
  title: { fontSize: 26, fontWeight: '800', color: colors.text },
  value: { fontSize: 20, fontWeight: '700', color: colors.accent },
  label: { fontSize: 13, fontWeight: '700', color: colors.accent, marginBottom: spacing.xs },
  text: { color: colors.text, lineHeight: 22 },
});
