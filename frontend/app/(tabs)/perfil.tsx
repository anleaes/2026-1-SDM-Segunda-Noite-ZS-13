import { router } from 'expo-router';
import { useCallback, useEffect, useState } from 'react';
import { Alert, ScrollView, StyleSheet, Text, View } from 'react-native';

import {
  fetchAvaliacoesVisitante,
  fetchIngressosVisitante,
  fetchReservasVisitante,
  fetchRestauracoesFuncionario,
} from '@/api/services';
import type { Avaliacao, Ingresso, Reserva, Restauracao } from '@/api/types';
import { Button, Card, LoadingScreen, ScreenHeader } from '@/components/ui';
import { useAuth } from '@/context/AuthContext';
import { colors, spacing } from '@/theme/colors';
import { formatCurrency, formatDate, roleLabel, statusLabel } from '@/utils/format';

export default function PerfilScreen() {
  const { user, logout } = useAuth();
  const [ingressos, setIngressos] = useState<Ingresso[]>([]);
  const [reservas, setReservas] = useState<Reserva[]>([]);
  const [avaliacoes, setAvaliacoes] = useState<Avaliacao[]>([]);
  const [restauracoes, setRestauracoes] = useState<Restauracao[]>([]);
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    if (!user) return;
    if (user.role === 'visitante') {
      const [ing, res, av] = await Promise.all([
        fetchIngressosVisitante(user.id),
        fetchReservasVisitante(user.id),
        fetchAvaliacoesVisitante(user.id),
      ]);
      setIngressos(ing);
      setReservas(res);
      setAvaliacoes(av);
    }
    if (user.role === 'funcionario') {
      setRestauracoes(await fetchRestauracoesFuncionario(user.id));
    }
  }, [user]);

  useEffect(() => {
    load().finally(() => setLoading(false));
  }, [load]);

  async function handleLogout() {
    await logout();
    router.replace('/login');
  }

  if (loading || !user) return <LoadingScreen />;

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <ScreenHeader title="Meu perfil" subtitle={roleLabel(user.role)} />

      <Card>
        <Text style={styles.name}>{user.first_name} {user.last_name}</Text>
        <Text style={styles.meta}>@{user.username}</Text>
        <Text style={styles.meta}>{user.email}</Text>
      </Card>

      {user.role === 'visitante' && (
        <>
          <Section title={`Ingressos (${ingressos.length})`}>
            {ingressos.map((item) => (
              <Text key={item.id} style={styles.item}>
                Exposicao #{item.exposicao} · {item.tipo} · {formatCurrency(item.valor)}
              </Text>
            ))}
            {!ingressos.length && <Text style={styles.empty}>Nenhum ingresso ainda.</Text>}
          </Section>

          <Section title={`Reservas (${reservas.length})`}>
            {reservas.map((item) => (
              <Text key={item.id} style={styles.item}>
                {formatDate(item.data_reserva)} · {item.quantidade_pessoas} pessoas · {statusLabel(item.status)}
              </Text>
            ))}
            {!reservas.length && <Text style={styles.empty}>Nenhuma reserva ainda.</Text>}
          </Section>

          <Section title={`Avaliacoes (${avaliacoes.length})`}>
            {avaliacoes.map((item) => (
              <Text key={item.id} style={styles.item}>
                {'★'.repeat(item.nota)} · {item.comentario}
              </Text>
            ))}
            {!avaliacoes.length && <Text style={styles.empty}>Nenhuma avaliacao ainda.</Text>}
          </Section>
        </>
      )}

      {user.role === 'funcionario' && (
        <Section title={`Restauracoes (${restauracoes.length})`}>
          {restauracoes.map((item) => (
            <Text key={item.id} style={styles.item}>
              Obra #{item.obra} · {formatCurrency(item.custo)} · {item.descricao}
            </Text>
          ))}
          {!restauracoes.length && <Text style={styles.empty}>Nenhuma restauracao registrada.</Text>}
        </Section>
      )}

      {user.role === 'artista' && (
        <Card>
          <Text style={styles.cardText}>
            Como artista, explore suas obras na aba Obras e veja em quais exposicoes elas estao.
          </Text>
        </Card>
      )}

      <Button
        label="Sair"
        variant="secondary"
        icon="log-out-outline"
        onPress={() =>
          Alert.alert('Sair', 'Deseja encerrar a sessao?', [
            { text: 'Cancelar', style: 'cancel' },
            { text: 'Sair', style: 'destructive', onPress: handleLogout },
          ])
        }
      />
    </ScrollView>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <Card>
      <Text style={styles.sectionTitle}>{title}</Text>
      <View style={styles.sectionBody}>{children}</View>
    </Card>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.bg },
  content: { padding: spacing.md, gap: spacing.md, paddingBottom: spacing.xl },
  name: { fontSize: 20, fontWeight: '700', color: colors.text },
  meta: { color: colors.textMuted, fontSize: 14 },
  sectionTitle: { fontSize: 15, fontWeight: '700', color: colors.text },
  sectionBody: { gap: spacing.sm },
  item: { color: colors.textMuted, fontSize: 14, lineHeight: 20 },
  empty: { color: colors.textMuted, fontStyle: 'italic', fontSize: 14 },
  cardText: { color: colors.textMuted, lineHeight: 22 },
});
