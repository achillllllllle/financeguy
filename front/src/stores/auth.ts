import { defineStore } from 'pinia';
import api from '@/api';

interface User {
    id: number;
    email: string;
    username: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
}

export const useAuthStore = defineStore('auth', {
    state: (): AuthState => ({
        user: null,
        token: null,
    }),

    getters: {
        isAuthenticated: (state) => !!state.token,
    },

    actions: {
        async login(email: string, password: string) {
            try {
                const response = await api.post('/token', { email, password });
                const { access_token } = response.data;
                this.token = access_token;
                localStorage.setItem('token', access_token);
                await this.fetchUser();
                return true;
            } catch (error) {
                console.error('Login failed:', error);
                return false;
            }
        },

        async register(email: string, username: string, password: string) {
            try {
                await api.post('/users/', { email, username, password });
                return true;
            } catch (error) {
                console.error('Registration failed:', error);
                return false;
            }
        },

        async fetchUser() {
            try {
                const response = await api.get('/users/me');
                this.user = response.data;
            } catch (error) {
                console.error('Failed to fetch user:', error);
                this.logout();
            }
        },

        logout() {
            this.user = null;
            this.token = null;
            localStorage.removeItem('token');
        },
    },
}); 