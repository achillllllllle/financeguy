<template>
  <div class="space-y-6">
    <!-- Formulaire d'ajout de catégorie -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:p-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
          Ajouter une catégorie
        </h3>
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div>
              <label for="name" class="block text-sm font-medium text-gray-700">
                Nom
              </label>
              <input
                type="text"
                id="name"
                v-model="newCategory.name"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                required
              />
            </div>

            <div>
              <label for="description" class="block text-sm font-medium text-gray-700">
                Description
              </label>
              <input
                type="text"
                id="description"
                v-model="newCategory.description"
                class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
              />
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

    <!-- Liste des catégories -->
    <div class="bg-white shadow rounded-lg">
      <div class="px-4 py-5 sm:px-6">
        <h3 class="text-lg leading-6 font-medium text-gray-900">
          Mes catégories
        </h3>
      </div>
      <div class="border-t border-gray-200">
        <ul class="divide-y divide-gray-200">
          <li v-for="category in categories" :key="category.id" class="px-4 py-4 sm:px-6">
            <div class="flex items-center justify-between">
              <div class="flex-1">
                <div class="flex items-center">
                  <p class="text-sm font-medium text-indigo-600 truncate">
                    {{ category.name }}
                  </p>
                  <span v-if="category.is_general" class="ml-2 px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                    Générale
                  </span>
                </div>
                <div class="mt-2">
                  <p class="text-sm text-gray-500">
                    {{ category.description || 'Aucune description' }}
                  </p>
                </div>
              </div>
              <div class="ml-4 flex-shrink-0" v-if="!category.is_general">
                <button
                  @click="handleDelete(category.id)"
                  class="font-medium text-red-600 hover:text-red-500"
                >
                  Supprimer
                </button>
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
import { useCategoryStore } from '@/stores/categories';

const categoryStore = useCategoryStore();

const categories = ref([]);

const newCategory = ref({
  name: '',
  description: '',
});

onMounted(async () => {
  await categoryStore.fetchCategories();
  categories.value = categoryStore.categories;
});

const handleSubmit = async () => {
  try {
    await categoryStore.createCategory(newCategory.value);
    newCategory.value = {
      name: '',
      description: '',
    };
    await categoryStore.fetchCategories();
    categories.value = categoryStore.categories;
  } catch (error) {
    console.error('Failed to create category:', error);
  }
};

const handleDelete = async (categoryId: number) => {
  try {
    await categoryStore.deleteCategory(categoryId);
    await categoryStore.fetchCategories();
    categories.value = categoryStore.categories;
  } catch (error) {
    console.error('Failed to delete category:', error);
  }
};
</script> 