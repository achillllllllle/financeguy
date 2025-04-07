<template>
  <div class="space-y-6">
    <!-- Formulaire d'ajout de transaction -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
          Ajouter une transaction
        </h3>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">
                Description
              </label>
              <input
                type="text"
                id="description"
                v-model="newTransaction.description"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              />
            </div>

            <div>
              <label for="amount" class="block text-sm font-medium text-gray-700">
                Montant
              </label>
              <div class="mt-1 relative rounded-md shadow-sm">
                <input
                  type="number"
                  id="amount"
                  v-model="newTransaction.amount"
                  step="0.01"
                  class="block w-full rounded-md border-gray-300 pr-12 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  required
                />
                <div class="absolute inset-y-0 right-0 flex items-center pr-3">
                  <span class="text-gray-500 sm:text-sm">€</span>
                </div>
              </div>
            </div>

            <div>
              <label for="type" class="block text-sm font-medium text-gray-700">
                Type
              </label>
              <select
                id="type"
                v-model="newTransaction.type"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              >
                <option value="income">Revenu</option>
                <option value="expense">Dépense</option>
              </select>
            </div>

            <div>
              <label for="category" class="block text-sm font-medium text-gray-700">
                Catégorie
              </label>
              <select
                id="category"
                v-model="newTransaction.category_id"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              >
                <option v-for="category in categories" :key="category.id" :value="category.id">
                  {{ category.name }}
                </option>
              </select>
            </div>

            <div>
              <label for="date" class="block text-sm font-medium text-gray-700">
                Date
              </label>
              <input
                type="date"
                id="date"
                v-model="newTransaction.date"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              />
            </div>

            <div class="flex items-center">
              <input
                id="is_recurrent"
                v-model="newTransaction.is_recurrent"
                type="checkbox"
                class="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
              />
              <label for="is_recurrent" class="ml-2 block text-sm text-gray-900">
                Transaction récurrente
              </label>
            </div>
          </div>

          <div v-if="newTransaction.is_recurrent" class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label for="frequency" class="block text-sm font-medium text-gray-700">
                Fréquence
              </label>
              <select
                id="frequency"
                v-model="newTransaction.recurrence_frequency"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              >
                <option value="daily">Quotidienne</option>
                <option value="weekly">Hebdomadaire</option>
                <option value="monthly">Mensuelle</option>
                <option value="yearly">Annuelle</option>
              </select>
            </div>
          </div>

          <div class="flex justify-end">
            <button
              type="submit"
              class="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
            >
              Ajouter
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Liste des transactions -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Historique des transactions
        </h3>
      </div>
      <div class="border-t border-gray-200">
        <ul class="divide-y divide-gray-200">
          <li v-for="transaction in transactions" :key="transaction.id" class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center">
                  <p class="text-sm font-medium text-indigo-600 truncate">
                    {{ transaction.description }}
                  </p>
                  <span class="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="transaction.type === 'income' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ transaction.type === 'income' ? 'Revenu' : 'Dépense' }}
                  </span>
                  <span v-if="transaction.is_recurrent" class="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                    Récurrent
                  </span>
                </div>
                <div class="mt-2 sm:flex sm:justify-between">
                  <div class="sm:flex">
                    <p class="flex items-center text-sm text-gray-500">
                      {{ transaction.category?.name }}
                    </p>
                  </div>
                  <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                    <p>
                      {{ new Date(transaction.date).toLocaleDateString() }}
                    </p>
                    <p class="ml-4 font-medium" :class="transaction.type === 'income' ? 'text-green-600' : 'text-red-600'">
                      {{ transaction.type === 'income' ? '+' : '-' }}{{ transaction.amount.toFixed(2) }} €
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useTransactionStore } from '@/stores/transactions';
import { useCategoryStore } from '@/stores/categories';

const transactionStore = useTransactionStore();
const categoryStore = useCategoryStore();

const transactions = ref([]);
const categories = ref([]);

const newTransaction = ref({
  description: '',
  amount: 0,
  type: 'expense',
  category_id: null,
  date: new Date().toISOString().split('T')[0],
  is_recurrent: false,
  recurrence_frequency: 'monthly',
});

onMounted(async () => {
  await transactionStore.fetchTransactions();
  await categoryStore.fetchCategories();
  
  transactions.value = transactionStore.transactions;
  categories.value = categoryStore.categories;
});

const handleSubmit = async () => {
  try {
    await transactionStore.createTransaction(newTransaction.value);
    newTransaction.value = {
      description: '',
      amount: 0,
      type: 'expense',
      category_id: null,
      date: new Date().toISOString().split('T')[0],
      is_recurrent: false,
      recurrence_frequency: 'monthly',
    };
    await transactionStore.fetchTransactions();
    transactions.value = transactionStore.transactions;
  } catch (error) {
    console.error('Failed to create transaction:', error);
  }
};
</script> 