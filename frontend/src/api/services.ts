import { apiGet, apiPost, unwrapList } from './client';
import type {
  Artista,
  AuthUser,
  Avaliacao,
  Exposicao,
  ExposicaoObra,
  Funcionario,
  Galeria,
  Ingresso,
  ObraArte,
  PaginatedResponse,
  Reserva,
  Restauracao,
  UserRole,
  Visitante,
} from './types';

export async function loginUser(username: string, role: UserRole): Promise<AuthUser> {
  const endpoints: Record<UserRole, string> = {
    visitante: '/visitantes/',
    funcionario: '/funcionarios/',
    artista: '/artistas/',
  };

  const data = await apiGet<PaginatedResponse<Visitante | Funcionario | Artista>>(
    endpoints[role],
    { search: username },
  );

  const user = data.results.find((item) => item.username === username);
  if (!user) {
    throw new Error('Usuario nao encontrado. Rode seed_demo no backend.');
  }

  return {
    id: user.id,
    username: user.username,
    first_name: user.first_name,
    last_name: user.last_name,
    email: user.email,
    role,
  };
}

export const fetchGalerias = () =>
  apiGet<PaginatedResponse<Galeria>>('/galerias/').then((d) => d.results);

export const fetchGaleria = (id: number) => apiGet<Galeria>(`/galerias/${id}/`);

export const fetchObras = (search?: string) =>
  apiGet<PaginatedResponse<ObraArte>>('/obras/', search ? { search } : undefined).then(
    (d) => d.results,
  );

export const fetchObra = (id: number) => apiGet<ObraArte>(`/obras/${id}/`);

export const fetchExposicoes = (search?: string) =>
  apiGet<PaginatedResponse<Exposicao>>('/exposicoes/', search ? { search } : undefined).then(
    (d) => d.results,
  );

export const fetchExposicao = (id: number) => apiGet<Exposicao>(`/exposicoes/${id}/`);

export const fetchExposicaoObras = (exposicaoId: number) =>
  apiGet<PaginatedResponse<ExposicaoObra>>('/exposicao-obras/', {
    exposicao: String(exposicaoId),
  }).then((d) => d.results);

export const fetchIngressosVisitante = (visitanteId: number) =>
  apiGet<PaginatedResponse<Ingresso>>('/ingressos/', {
    visitante: String(visitanteId),
  }).then((d) => d.results);

export const fetchReservasVisitante = (visitanteId: number) =>
  apiGet<PaginatedResponse<Reserva>>('/reservas/', {
    visitante: String(visitanteId),
  }).then((d) => d.results);

export const fetchAvaliacoesVisitante = (visitanteId: number) =>
  apiGet<PaginatedResponse<Avaliacao>>('/avaliacoes/', {
    visitante: String(visitanteId),
  }).then((d) => d.results);

export const fetchRestauracoesFuncionario = (funcionarioId: number) =>
  apiGet<PaginatedResponse<Restauracao>>('/restauracoes/', {
    funcionario: String(funcionarioId),
  }).then((d) => d.results);

export const comprarIngresso = (visitanteId: number, exposicaoId: number) =>
  apiPost<Ingresso>('/ingressos/', {
    visitante: visitanteId,
    exposicao: exposicaoId,
    tipo: 'inteira',
    valor: '60.00',
    status: 'ativo',
  });

export const criarReserva = (
  visitanteId: number,
  exposicaoId: number,
  quantidade: number,
  dataReserva: string,
) =>
  apiPost<Reserva>('/reservas/', {
    visitante: visitanteId,
    exposicao: exposicaoId,
    quantidade_pessoas: quantidade,
    data_reserva: dataReserva,
    status: 'confirmada',
  });

export const criarAvaliacao = (
  visitanteId: number,
  exposicaoId: number,
  nota: number,
  comentario: string,
) =>
  apiPost<Avaliacao>('/avaliacoes/', {
    visitante: visitanteId,
    exposicao: exposicaoId,
    nota,
    comentario,
  });

export async function fetchDashboardCounts() {
  const [galerias, obras, exposicoes] = await Promise.all([
    apiGet<PaginatedResponse<Galeria>>('/galerias/'),
    apiGet<PaginatedResponse<ObraArte>>('/obras/'),
    apiGet<PaginatedResponse<Exposicao>>('/exposicoes/'),
  ]);

  return {
    galerias: galerias.count,
    obras: obras.count,
    exposicoes: exposicoes.count,
  };
}

export { unwrapList };
