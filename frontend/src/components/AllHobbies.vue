<template>
    <div v-if="hobbies.length > 0" class="mt-5">
      <div class="card shadow">
        <div class="card-header bg-primary text-white d-flex align-items-center justify-content-between">
          <h3 class="mb-0">All Hobbies</h3>
        </div>
      </div>
      <!-- List all hobbies -->
      <ul class="list-group">
        <li v-for="hobby in hobbies" :key="hobby.name" class="list-group-item hobby-item">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="hobby-name">{{ hobby.name }}</h5>
              <p class="hobby-benefits">{{ hobby.benefits }}</p>
            </div>
            <div>
              <span class="badge bg-success rating-badge">{{ hobby.rating }}/5</span>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <!-- Shows message if no hobbies are found -->
    <div v-else class="text-center mt-5">
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
  .hobby-item {
    transition: transform 0.3s ease;
    cursor: pointer;
  }
  
  .hobby-item:hover {
    transform: scale(1.05);
    background-color: #f9f9f9;
  }
  
  .hobby-benefits {
    color: #6c757d;
    font-size: 0.9rem;
    margin-bottom: 0;
  }
  
  .rating-badge {
    font-size: 0.9rem;
    padding: 0.4em 0.7em;
  }
  </style>
  