import { useLocalSearchParams } from 'expo-router';
import { useEffect, useState } from 'react';
import { Alert, ScrollView, StyleSheet, Text, View } from 'react-native';

import {
  comprarIngresso,
  criarAvaliacao,
  criarReserva,
  fetchExposicao,
  fetchExposicaoObras,
  fetchObra,
} from '@/api/services';
import type { Exposicao, ObraArte } from '@/api/types';
import { Badge, Button, Card, Input, LoadingScreen } from '@/components/ui';
import { useAuth } from '@/context/AuthContext';
import { colors, spacing } from '@/theme/colors';
import { formatDate, statusLabel } from '@/utils/format';

export default function ExposicaoDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const { user } = useAuth();
  const [exposicao, setExposicao] = useState<Exposicao | null>(null);
  const [obras, setObras] = useState<ObraArte[]>([]);
  const [nota, setNota] = useState('5');
  const [comentario, setComentario] = useState('Exposicao excelente!');
  const [loadingAction, setLoadingAction] = useState(false);

  useEffect(() => {
    const exposicaoId = Number(id);
    fetchExposicao(exposicaoId).then(setExposicao);
    fetchExposicaoObras(exposicaoId).then(async (links) => {
      const lista = await Promise.all(links.map((link) => fetchObra(link.obra)));
      setObras(lista);
    });
  }, [id]);

  async function runAction(action: () => Promise<void>, success: string) {
    try {
      setLoadingAction(true);
      await action();
      Alert.alert('Sucesso', success);
    } catch (error) {
      Alert.alert('Erro', error instanceof Error ? error.message : 'Nao foi possivel concluir.');
    } finally {
      setLoadingAction(false);
    }
  }

  if (!exposicao) return <LoadingScreen />;

  const isVisitante = user?.role === 'visitante';

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.title}>{exposicao.titulo}</Text>
        <Badge label={statusLabel(exposicao.status)} />
      </View>

      <Text style={styles.dates}>
        {formatDate(exposicao.data_inicio)} — {formatDate(exposicao.data_fim)}
      </Text>

      <Card>
        <Text style={styles.label}>Descricao</Text>
        <Text style={styles.text}>{exposicao.descricao}</Text>
      </Card>

      <Card>
        <Text style={styles.label}>Obras na exposicao ({obras.length})</Text>
        {obras.map((obra) => (
          <Text key={obra.id} style={styles.item}>• {obra.titulo} ({obra.ano_criacao})</Text>
        ))}
        {!obras.length && <Text style={styles.muted}>Nenhuma obra vinculada.</Text>}
      </Card>

      {isVisitante && user && (
        <Card>
          <Text style={styles.label}>Acoes do visitante</Text>
          <View style={styles.actions}>
            <Button
              label="Comprar ingresso (R$ 60)"
              icon="ticket-outline"
              loading={loadingAction}
              onPress={() =>
                runAction(
                  () => comprarIngresso(user.id, exposicao.id),
                  'Ingresso comprado com sucesso!',
                )
              }
            />
            <Button
              label="Reservar visita (4 pessoas)"
              variant="secondary"
              icon="calendar-outline"
              loading={loadingAction}
              onPress={() =>
                runAction(
                  () => criarReserva(user.id, exposicao.id, 4, '2026-08-15'),
                  'Reserva confirmada!',
                )
              }
            />
          </View>

          <Input label="Nota (1-5)" value={nota} onChangeText={setNota} keyboardType="numeric" />
          <Input label="Comentario" value={comentario} onChangeText={setComentario} />
          <Button
            label="Enviar avaliacao"
            variant="secondary"
            icon="star-outline"
            loading={loadingAction}
            onPress={() =>
              runAction(
                () => criarAvaliacao(user.id, exposicao.id, Number(nota), comentario),
                'Avaliacao registrada!',
              )
            }
          />
        </Card>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  content: { padding: spacing.md, gap: spacing.md, paddingBottom: spacing.xl },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', gap: spacing.sm },
  title: { flex: 1, fontSize: 24, fontWeight: '800', color: colors.text },
  dates: { color: colors.accent, fontSize: 14 },
  label: { fontSize: 13, fontWeight: '700', color: colors.accent, marginBottom: spacing.xs },
  text: { color: colors.text, lineHeight: 22 },
  item: { color: colors.textMuted, fontSize: 14, lineHeight: 22 },
  muted: { color: colors.textMuted, fontStyle: 'italic' },
  actions: { gap: spacing.sm, marginBottom: spacing.md },
});
