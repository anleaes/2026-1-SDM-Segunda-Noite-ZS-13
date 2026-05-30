import { Ionicons } from '@expo/vector-icons';
import { router } from 'expo-router';
import { useState } from 'react';
import {
  Alert,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';

import { Button, Input } from '@/components/ui';
import { useAuth } from '@/context/AuthContext';
import type { UserRole } from '@/api/types';
import { colors, radius, spacing } from '@/theme/colors';

const ROLES: { key: UserRole; label: string; icon: keyof typeof Ionicons.glyphMap }[] = [
  { key: 'visitante', label: 'Visitante', icon: 'person-outline' },
  { key: 'funcionario', label: 'Funcionario', icon: 'briefcase-outline' },
  { key: 'artista', label: 'Artista', icon: 'color-palette-outline' },
];

const DEMO_USERS = [
  { username: 'nathan.visitante', role: 'visitante' as UserRole },
  { username: 'nathan.funcionario', role: 'funcionario' as UserRole },
  { username: 'nathan.artista', role: 'artista' as UserRole },
];

export default function LoginScreen() {
  const { login } = useAuth();
  const [username, setUsername] = useState('nathan.visitante');
  const [role, setRole] = useState<UserRole>('visitante');
  const [loading, setLoading] = useState(false);

  async function handleLogin(selectedUsername?: string, selectedRole?: UserRole) {
    try {
      setLoading(true);
      await login(selectedUsername ?? username, selectedRole ?? role);
      router.replace('/(tabs)');
    } catch (error) {
      Alert.alert(
        'Erro ao entrar',
        error instanceof Error ? error.message : 'Verifique se o backend esta rodando.',
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe}>
      <KeyboardAvoidingView
        style={styles.flex}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}
      >
        <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
          <View style={styles.hero}>
            <View style={styles.logo}>
              <Ionicons name="easel-outline" size={40} color={colors.primary} />
            </View>
            <Text style={styles.title}>Museu & Galeria</Text>
            <Text style={styles.subtitle}>Sistema de gerenciamento SDM</Text>
          </View>

          <View style={styles.form}>
            <Input
              label="Usuario (login)"
              value={username}
              onChangeText={setUsername}
              placeholder="nathan.visitante"
            />

            <Text style={styles.label}>Tipo de perfil</Text>
            <View style={styles.roles}>
              {ROLES.map((item) => {
                const active = role === item.key;
                return (
                  <Pressable
                    key={item.key}
                    onPress={() => setRole(item.key)}
                    style={[styles.roleChip, active && styles.roleChipActive]}
                  >
                    <Ionicons
                      name={item.icon}
                      size={18}
                      color={active ? colors.text : colors.textMuted}
                    />
                    <Text style={[styles.roleText, active && styles.roleTextActive]}>
                      {item.label}
                    </Text>
                  </Pressable>
                );
              })}
            </View>

            <Button label="Entrar" onPress={() => handleLogin()} loading={loading} icon="log-in-outline" />
          </View>

          <View style={styles.demo}>
            <Text style={styles.demoTitle}>Acesso rapido (demo)</Text>
            {DEMO_USERS.map((demo) => (
              <Pressable
                key={demo.username}
                style={styles.demoItem}
                onPress={() => handleLogin(demo.username, demo.role)}
              >
                <Text style={styles.demoUser}>{demo.username}</Text>
                <Ionicons name="chevron-forward" size={16} color={colors.textMuted} />
              </Pressable>
            ))}
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: colors.bg },
  flex: { flex: 1 },
  container: { padding: spacing.lg, gap: spacing.lg },
  hero: { alignItems: 'center', gap: spacing.sm, paddingVertical: spacing.xl },
  logo: {
    width: 80,
    height: 80,
    borderRadius: radius.lg,
    backgroundColor: colors.bgCard,
    alignItems: 'center',
    justifyContent: 'center',
    borderWidth: 1,
    borderColor: colors.border,
  },
  title: { fontSize: 28, fontWeight: '800', color: colors.text },
  subtitle: { color: colors.textMuted, fontSize: 15 },
  form: { gap: spacing.md },
  label: { color: colors.textMuted, fontSize: 14, fontWeight: '500' },
  roles: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
  roleChip: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.xs,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
    borderRadius: radius.full,
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderColor: colors.border,
  },
  roleChipActive: { backgroundColor: colors.primary, borderColor: colors.primary },
  roleText: { color: colors.textMuted, fontWeight: '600' },
  roleTextActive: { color: colors.text },
  demo: {
    backgroundColor: colors.bgCard,
    borderRadius: radius.lg,
    padding: spacing.md,
    borderWidth: 1,
    borderColor: colors.border,
    gap: spacing.sm,
  },
  demoTitle: { color: colors.textMuted, fontSize: 13, fontWeight: '600', marginBottom: spacing.xs },
  demoItem: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  demoUser: { color: colors.text, fontSize: 15 },
});
