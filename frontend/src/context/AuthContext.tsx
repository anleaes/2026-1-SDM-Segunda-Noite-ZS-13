import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';

import { loginUser } from '@/api/services';
import type { AuthUser, UserRole } from '@/api/types';

const STORAGE_KEY = '@museu_auth_user';

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  login: (username: string, role: UserRole) => Promise<void>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    AsyncStorage.getItem(STORAGE_KEY)
      .then((raw) => {
        if (raw) setUser(JSON.parse(raw) as AuthUser);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (username: string, role: UserRole) => {
    const authUser = await loginUser(username.trim(), role);
    setUser(authUser);
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(authUser));
  }, []);

  const logout = useCallback(async () => {
    setUser(null);
    await AsyncStorage.removeItem(STORAGE_KEY);
  }, []);

  const value = useMemo(
    () => ({ user, loading, login, logout }),
    [user, loading, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth deve ser usado dentro de AuthProvider');
  return ctx;
}
