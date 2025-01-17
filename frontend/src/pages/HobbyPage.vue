<template>
    <div class="container mt-4">
      <h1 class="display-3 text-primary text-center">All About Hobbies</h1>

      
      <!-- Section for adding a new hobby -->
      <section class="mt-5">
        <h2 class="text-success text-center">Add a New Hobby</h2>
        <AddHobby @hobby-added="refreshHobbyList" />
      </section>
  
      <!-- Section for listing all hobbies -->
      <section class="mt-5">
        <h2 class="text-info text-center">Your Hobbies</h2>
        <AllHobbies ref="hobbyList" />
      </section>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent } from "vue";
  import CreateHobby from "../components/CreateHobby.vue";
  import AllHobbies from "../components/AllHobbies.vue";
  import { Hobby } from "../stores/hobbyStore.ts";
  
  export default defineComponent({
    components: {
      CreateHobby,
      AllHobbies,
    },
    methods: {
      // Refreshes the list of hobbies when a new one is added
      refreshHobbyList(newHobby: Hobby) {
        (this.$refs.hobbyList as any).fetchHobbies();
      },
    },
  });
  </script>
  
  <style scoped>
  .container {
    background-color: #f9f9f9;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  }
  
  .text-primary {
    font-weight: 700;
    text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
  }
  
  .text-secondary {
    font-size: 1.2rem;
    font-style: italic;
  }
  
  .text-info {
    font-size: 1.8rem;
    text-decoration: underline;
  }
  
  .text-success {
    font-size: 1.6rem;
    font-weight: bold;
  }
  </style>
  
