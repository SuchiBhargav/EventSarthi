import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Planner, AuthState } from '@/types';
import api from '@/services/api';
import { toast } from 'react-hot-toast';

interface AuthContextType extends AuthState {
  login: (phone: string, password: string) => Promise<void>;
  logout: () => void;
  register: (data: any) => Promise<void>;
  updatePlanner: (planner: Planner) => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    planner: null,
    token: null,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing token on mount
    const token = localStorage.getItem('auth_token');
    if (token) {
      loadPlanner();
    } else {
      setIsLoading(false);
    }
  }, []);

  const loadPlanner = async () => {
    try {
      const planner = await api.getCurrentPlanner();
      setAuthState({
        isAuthenticated: true,
        planner,
        token: localStorage.getItem('auth_token'),
      });
    } catch (error) {
      localStorage.removeItem('auth_token');
      setAuthState({
        isAuthenticated: false,
        planner: null,
        token: null,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (phone: string, password: string) => {
    try {
      const response = await api.login(phone, password);
      const { access_token, planner } = response;
      
      localStorage.setItem('auth_token', access_token);
      setAuthState({
        isAuthenticated: true,
        planner,
        token: access_token,
      });
      
      toast.success('Login successful!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Login failed');
      throw error;
    }
  };

  const register = async (data: any) => {
    try {
      const response = await api.register(data);
      const { access_token, planner } = response;
      
      localStorage.setItem('auth_token', access_token);
      setAuthState({
        isAuthenticated: true,
        planner,
        token: access_token,
      });
      
      toast.success('Registration successful!');
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Registration failed');
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('auth_token');
    setAuthState({
      isAuthenticated: false,
      planner: null,
      token: null,
    });
    toast.success('Logged out successfully');
  };

  const updatePlanner = (planner: Planner) => {
    setAuthState((prev) => ({
      ...prev,
      planner,
    }));
  };

  return (
    <AuthContext.Provider
      value={{
        ...authState,
        login,
        logout,
        register,
        updatePlanner,
        isLoading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Made with Bob
