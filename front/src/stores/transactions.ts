import { defineStore } from 'pinia';
import api from '@/api';

interface Transaction {
    id: number;
    amount: number;
    description: string;
    type: 'income' | 'expense';
    date: string;
    category_id: number;
    is_recurrent: boolean;
    recurrence_frequency?: 'daily' | 'weekly' | 'monthly' | 'yearly';
    next_occurrence?: string;
    is_confirmed: boolean;
}

interface TransactionState {
    transactions: Transaction[];
    balance: number;
}

export const useTransactionStore = defineStore('transactions', {
    state: (): TransactionState => ({
        transactions: [],
        balance: 0,
    }),

    actions: {
        async fetchTransactions() {
            try {
                const response = await api.get('/transactions/');
                this.transactions = response.data;
                this.calculateBalance();
            } catch (error) {
                console.error('Failed to fetch transactions:', error);
            }
        },

        async createTransaction(transaction: Omit<Transaction, 'id' | 'date'>) {
            try {
                const response = await api.post('/transactions/', transaction);
                this.transactions.push(response.data);
                this.calculateBalance();
                return true;
            } catch (error) {
                console.error('Failed to create transaction:', error);
                return false;
            }
        },

        async fetchRecurrentTransactions() {
            try {
                const response = await api.get('/transactions/recurrent/');
                return response.data;
            } catch (error) {
                console.error('Failed to fetch recurrent transactions:', error);
                return [];
            }
        },

        async confirmTransaction(transactionId: number) {
            try {
                await api.put(`/transactions/${transactionId}/confirm/`);
                await this.fetchTransactions();
                return true;
            } catch (error) {
                console.error('Failed to confirm transaction:', error);
                return false;
            }
        },

        async fetchPendingTransactions() {
            try {
                const response = await api.get('/transactions/pending/');
                return response.data;
            } catch (error) {
                console.error('Failed to fetch pending transactions:', error);
                return [];
            }
        },

        calculateBalance() {
            this.balance = this.transactions.reduce((total, transaction) => {
                return total + (transaction.type === 'income' ? transaction.amount : -transaction.amount);
            }, 0);
        },
    },
}); 