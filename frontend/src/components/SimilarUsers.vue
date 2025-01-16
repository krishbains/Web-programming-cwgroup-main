<template>
  <div>
    <h1>Similar Users</h1>
    <div>
      <label for="minAge">Min Age:</label>
      <input type="number" v-model="minAge" @change="fetchUsers" />
      <label for="maxAge">Max Age:</label>
      <input type="number" v-model="maxAge" @change="fetchUsers" />
    </div>
    <div>
      <UserCard v-for="user in users" :key="user.id" :user="user" />
    </div>
    <PaginationControls
      :currentPage="currentPage"
      :totalPages="totalPages"
      @nextPage="nextPage"
      @prevPage="prevPage"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import UserCard from '../components/UserCard.vue';
import PaginationControls from '../components/PaginationControls.vue';
import { fetchSimilarUsers } from '../api';

export default defineComponent({
  components: { UserCard, PaginationControls },
  setup() {
    const users = ref<any[]>([]);
    const currentPage = ref(1);
    const totalPages = ref(1);
    const minAge = ref<number | null>(null);
    const maxAge = ref<number | null>(null);

    const fetchUsers = async () => {
      const response = await fetchSimilarUsers(currentPage.value, minAge.value, maxAge.value);
      users.value = response.results;
      totalPages.value = response.total_pages;
    };

    const nextPage = () => {
      if (currentPage.value < totalPages.value) {
        currentPage.value++;
        fetchUsers();
      }
    };

    const prevPage = () => {
      if (currentPage.value > 1) {
        currentPage.value--;
        fetchUsers();
      }
    };

    fetchUsers();

    return { users, currentPage, totalPages, minAge, maxAge, fetchUsers, nextPage, prevPage };
  }
});
</script>

<style scoped>
/* styling  */
</style>