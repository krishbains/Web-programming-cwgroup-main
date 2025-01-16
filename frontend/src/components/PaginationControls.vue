<template>
    <div>
      <button @click="$emit('prevPage')" :disabled="currentPage === 1">Previous</button>
      <span>Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="$emit('nextPage')" :disabled="currentPage === totalPages">Next</button>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    props: {
      currentPage: {
        type: Number,
        required: true
      },
      totalPages: {
        type: Number,
        required: true
      }
    }
  });
  </script>
  
  <style scoped>
  /* styles  */
  </style>