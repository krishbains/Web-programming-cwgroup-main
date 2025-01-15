<template>
  <div>
    <div v-if="loading" class="h1">Loading...</div>
    <div v-else-if="error" class="h1">{{ error }}</div>
    <div v-else class="h1">
      Hello, {{ username }}!
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { apiService } from "../services/api";
import type { UserProfile } from "../services/types";

interface ComponentData {
  loading: boolean;
  error: string;
  username: string;
  profile: UserProfile | null;
}

export default defineComponent({
  data(): ComponentData {
    return {
      loading: true,
      error: "",
      username: "",
      profile: null
    };
  },

  async created() {
    await this.loadUserProfile();
  },

  methods: {
    async loadUserProfile() {
      this.loading = true;
      const response = await apiService.getCurrentProfile();

      if (response.error) {
        this.error = response.error;
      } else if (response.data) {
        this.profile = response.data;
        this.username = this.profile.username;
      }

      this.loading = false;
    }
  }
});
</script>

<style scoped>
.h1 {
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem 0;
}
</style>