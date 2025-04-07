import { defineStore } from 'pinia';
import api from '@/api';

interface Reminder {
    id: number;
    title: string;
    description: string;
    due_date: string;
    amount: number;
    is_paid: boolean;
}

interface ReminderState {
    reminders: Reminder[];
}

export const useReminderStore = defineStore('reminders', {
    state: (): ReminderState => ({
        reminders: [],
    }),

    actions: {
        async fetchReminders() {
            try {
                const response = await api.get('/reminders/');
                this.reminders = response.data;
            } catch (error) {
                console.error('Failed to fetch reminders:', error);
            }
        },

        async createReminder(reminder: Omit<Reminder, 'id' | 'is_paid'>) {
            try {
                const response = await api.post('/reminders/', reminder);
                this.reminders.push(response.data);
                return true;
            } catch (error) {
                console.error('Failed to create reminder:', error);
                return false;
            }
        },

        async updateReminder(reminderId: number, reminder: Partial<Reminder>) {
            try {
                const response = await api.put(`/reminders/${reminderId}/`, reminder);
                const index = this.reminders.findIndex(r => r.id === reminderId);
                if (index !== -1) {
                    this.reminders[index] = response.data;
                }
                return true;
            } catch (error) {
                console.error('Failed to update reminder:', error);
                return false;
            }
        },

        async deleteReminder(reminderId: number) {
            try {
                await api.delete(`/reminders/${reminderId}/`);
                this.reminders = this.reminders.filter(r => r.id !== reminderId);
                return true;
            } catch (error) {
                console.error('Failed to delete reminder:', error);
                return false;
            }
        },
    },
}); 