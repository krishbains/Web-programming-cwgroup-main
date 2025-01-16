<template>
  <div v-if="hobbies.length > 0" class="mt-5">
    <div class="card">
      <div class="card-header">
        <h3>All Hobbies</h3>
      </div>
    </div>
    <!-- List all hobbies -->
    <ul>
      <li v-for="hobby in hobbies" :key="hobby.name">
        <div>
          <h5>{{ hobby.name }}</h5>
          <p>{{ hobby.benefits }}</p>
          <span>{{ hobby.rating }}/5</span>
        </div>
      </li>
    </ul>
  </div>
  <!-- Shows message if no hobbies are found -->
  <div v-else class="mt-5">
    <p>No hobbies found</p>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/userStore.ts";
import { Hobby } from "../stores/hobbyStore.ts";

export default defineComponent({
  name: "AllHobbies",
  data() {
    return {
      hobbies: [] as Array<{ name: string; benefits: string; rating: number }>,
      store: useUserStore(),
    };
  },
  mounted() {
    this.fetchHobbies();
  },
  methods: {
    // Method for fetching all hobbies from the database
    async fetchHobbies() {
      const csrfToken = this.store.getCookie("csrftoken", document.cookie);
      const response = await fetch('/api/hobbies', {
        method: 'GET',
        credentials: "same-origin",
        mode: 'cors',
        headers: {
          'Content-Type': 'application/json',
          'Cookie': document.cookie,
          'x-csrftoken': csrfToken,
        },
      });
      if (response.ok) {
        const data = await response.json();
        this.hobbies = data;
      } else {
        alert('Failed to fetch hobbies from the database');
      }
    },
  },
});
</script>

<style scoped>
ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

h5 {
  margin: 0;
  font-size: 1.2rem;
}

p {
  margin: 5px 0;
  color: #555;
}

span {
  font-size: 0.9rem;
  color: #777;
}
</style>
