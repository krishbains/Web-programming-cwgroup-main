<template>
    <div class="user-card">
      <h2>{{ user.username }}</h2>
      <p>Email: {{ user.email }}</p>
      <p>Date of Birth: {{ user.date_of_birth }}</p>
      <p>Hobbies: {{ user.hobbies.join(', ') }}</p>
      <p>Similarity Score: {{ user.similarity_score }}</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType } from 'vue';
  
  export default defineComponent({
    props: {
      user: {
        type: Object as PropType<{
          id: number;
          username: string;
          email: string;
          date_of_birth: string;
          hobbies: string[];
          similarity_score: number;
        }>,
        required: true
      }
    }
  });
  </script>
  
  <style scoped>
  .user-card {
    border: 1px solid #ccc;
    padding: 16px;
    margin: 8px 0;
  }
  </style>