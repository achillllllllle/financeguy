import { defineStore } from 'pinia';
import api from '@/api';

interface Category {
    id: number;
    name: string;
    description: string;
    is_general: boolean;
}

interface CategoryState {
    categories: Category[];
}

export const useCategoryStore = defineStore('categories', {
    state: (): CategoryState => ({
        categories: [],
    }),

    actions: {
        async fetchCategories() {
            try {
                const response = await api.get('/categories/');
                this.categories = response.data;
            } catch (error) {
                console.error('Failed to fetch categories:', error);
            }
        },

        async createCategory(category: Omit<Category, 'id'>) {
            try {
                const response = await api.post('/categories/', category);
                this.categories.push(response.data);
                return true;
            } catch (error) {
                console.error('Failed to create category:', error);
                return false;
            }
        },

        async updateCategory(categoryId: number, category: Partial<Category>) {
            try {
                const response = await api.put(`/categories/${categoryId}/`, category);
                const index = this.categories.findIndex(c => c.id === categoryId);
                if (index !== -1) {
                    this.categories[index] = response.data;
                }
                return true;
            } catch (error) {
                console.error('Failed to update category:', error);
                return false;
            }
        },

        async deleteCategory(categoryId: number) {
            try {
                await api.delete(`/categories/${categoryId}/`);
                this.categories = this.categories.filter(c => c.id !== categoryId);
                return true;
            } catch (error) {
                console.error('Failed to delete category:', error);
                return false;
            }
        },
    },
}); 