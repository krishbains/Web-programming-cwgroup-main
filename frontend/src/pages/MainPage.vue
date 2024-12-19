<template>
  <div class="h1">
    {{ title }}
  </div>
</template>

<script lang="ts">
    import { defineComponent } from "vue";

    export default defineComponent({
        data() {
            return {
                title: "Main Page",
            }
        }
    })
</script>

<style scoped>
</style>
