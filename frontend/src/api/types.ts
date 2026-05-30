export type UserRole = 'visitante' | 'funcionario' | 'artista';

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface Usuario {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  telefone: string;
  cpf: string;
  data_nascimento?: string;
}

export interface Visitante extends Usuario {
  data_cadastro: string;
}

export interface Funcionario extends Usuario {
  cargo: string;
  salario: string;
  data_admissao: string;
  galeria: number | null;
}

export interface Artista extends Usuario {
  nacionalidade: string;
  estilo_artistico: string;
}

export interface Galeria {
  id: number;
  nome: string;
  descricao: string;
  endereco: string;
  aberta: boolean;
}

export interface CategoriaObra {
  id: number;
  nome: string;
  descricao: string;
}

export interface ObraArte {
  id: number;
  titulo: string;
  tecnica: string;
  ano_criacao: number;
  valor_estimado: string;
  categoria: number;
}

export interface Certificado {
  id: number;
  obra: number;
  codigo: string;
  data_emissao: string;
  orgao_responsavel: string;
}

export interface Exposicao {
  id: number;
  titulo: string;
  descricao: string;
  data_inicio: string;
  data_fim: string;
  status: 'planejada' | 'em_andamento' | 'encerrada';
  galeria: number;
}

export interface ExposicaoObra {
  id: number;
  exposicao: number;
  obra: number;
  data_entrada: string;
  posicao_sala: string;
  iluminacao_especial: string;
  status_conservacao: string;
  estilo_obra: string;
}

export interface Ingresso {
  id: number;
  visitante: number;
  exposicao: number;
  tipo: string;
  valor: string;
  data_compra: string;
  status: string;
}

export interface Reserva {
  id: number;
  visitante: number;
  exposicao: number;
  data_reserva: string;
  quantidade_pessoas: number;
  status: string;
}

export interface Avaliacao {
  id: number;
  visitante: number;
  exposicao: number;
  nota: number;
  comentario: string;
  data_avaliacao: string;
}

export interface Restauracao {
  id: number;
  obra: number;
  funcionario: number;
  data_inicio: string;
  data_fim: string | null;
  descricao: string;
  custo: string;
}

export interface AuthUser {
  id: number;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  role: UserRole;
}
