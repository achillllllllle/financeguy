<template>
  <div class="space-y-6">
    <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <!-- Solde actuel -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Solde actuel
                </dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-gray-900">
                    {{ balance.toFixed(2) }} €
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Dépenses du mois -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 9V7a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2m2 4h10a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 002 2zm7-5a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Dépenses du mois
                </dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-red-600">
                    {{ monthlyExpenses.toFixed(2) }} €
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <!-- Revenus du mois -->
      <div class="bg-white overflow-hidden shadow rounded-lg">
        <div class="p-5">
          <div class="flex items-center">
            <div class="flex-shrink-0">
              <svg class="h-6 w-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div class="ml-5 w-0 flex-1">
              <dl>
                <dt class="text-sm font-medium text-gray-500 truncate">
                  Revenus du mois
                </dt>
                <dd class="flex items-baseline">
                  <div class="text-2xl font-semibold text-green-600">
                    {{ monthlyIncome.toFixed(2) }} €
                  </div>
                </dd>
              </dl>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Rappels à venir -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Rappels à venir
        </h3>
      </div>
      <div class="border-t border-gray-200">
        <ul class="divide-y divide-gray-200">
          <li v-for="reminder in upcomingReminders" :key="reminder.id" class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center">
                  <p class="text-sm font-medium text-indigo-600 truncate">
                    {{ reminder.title }}
                  </p>
                  <span class="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="reminder.is_paid ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ reminder.is_paid ? 'Payé' : 'En attente' }}
                  </span>
                </div>
                <div class="mt-2 sm:flex sm:justify-between">
                  <div class="sm:flex">
                    <p class="flex items-center text-sm text-gray-500">
                      {{ reminder.description }}
                    </p>
                  </div>
                  <div class="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                    <p>
                      Échéance : {{ new Date(reminder.due_date).toLocaleDateString() }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Dernières transactions -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Dernières transactions
        </h3>
      </div>
      <div class="border-t border-gray-200">
        <ul class="divide-y divide-gray-200">
          <li v-for="transaction in recentTransactions" :key="transaction.id" class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center">
                  <p class="text-sm font-medium text-indigo-600 truncate">
                    {{ transaction.description }}
                  </p>
                  <span class="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full" :class="transaction.type === 'income' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'">
                    {{ transaction.type === 'income' ? 'Revenu' : 'Dépense' }}
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
import { useReminderStore } from '@/stores/reminders';

const transactionStore = useTransactionStore();
const reminderStore = useReminderStore();

const balance = ref(0);
const monthlyExpenses = ref(0);
const monthlyIncome = ref(0);
const recentTransactions = ref([]);
const upcomingReminders = ref([]);

onMounted(async () => {
  await transactionStore.fetchTransactions();
  await reminderStore.fetchReminders();
  
  // Calculer le solde
  balance.value = transactionStore.balance;
  
  // Calculer les dépenses et revenus du mois
  const now = new Date();
  const firstDayOfMonth = new Date(now.getFullYear(), now.getMonth(), 1);
  
  monthlyExpenses.value = transactionStore.transactions
    .filter(t => t.type === 'expense' && new Date(t.date) >= firstDayOfMonth)
    .reduce((sum, t) => sum + t.amount, 0);
    
  monthlyIncome.value = transactionStore.transactions
    .filter(t => t.type === 'income' && new Date(t.date) >= firstDayOfMonth)
    .reduce((sum, t) => sum + t.amount, 0);
    
  // Récupérer les 5 dernières transactions
  recentTransactions.value = transactionStore.transactions
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, 5);
    
  // Récupérer les rappels à venir
  upcomingReminders.value = reminderStore.reminders
    .filter(r => !r.is_paid && new Date(r.due_date) >= new Date())
    .sort((a, b) => new Date(a.due_date).getTime() - new Date(b.due_date).getTime())
    .slice(0, 5);
});
</script> 