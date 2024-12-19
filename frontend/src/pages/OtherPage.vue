<template>
    <div class="h3">
      {{ title }}
    </div>
  </template>
  
  <script lang="ts">
      import { defineComponent } from "vue";
  
      export default defineComponent({
          data() {
              return {
                  title: "Other Page",
              }
          }
      })
  </script>
  
  <style scoped>
  </style>
  