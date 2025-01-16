<template>
    <div class="hobby-info-card">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">{{ hobby.name }}</h5>
          <p class="card-text">{{ hobby.benefits }}</p>
          <p class="card-text">
            <strong>Rating:</strong> {{ hobby.rating }} / 5
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType } from "vue";
  
  // Define the hobby prop type
  interface Hobby {
    name: string;
    benefits: string;
    rating: number;
  }
  
  export default defineComponent({
    name: "HobbyInfo",
    props: {
      hobby: {
        type: Object as PropType<Hobby>,
        required: true,
      },
    },
  });
  </script>
  
  <style scoped>
  .hobby-info-card {
    margin: 10px 0;
  }
  
  .card {
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  .card-body {
    padding: 15px;
  }
  
  .card-title {
    font-size: 1.25rem;
    font-weight: bold;
  }
  
  .card-text {
    font-size: 1rem;
    color: #555;
  }
  
  .card-text strong {
    font-weight: 600;
  }
  </style>
  