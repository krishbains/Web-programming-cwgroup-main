<template>
  <div class="main-page">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <h1>Hello, {{ username }}!</h1>
      <p class="welcome-text">Welcome to the Hobbies App. Here you can:</p>
      <ul class="features-list">
        <li>View and edit your profile</li>
        <li>Manage your hobbies</li>
        <li>Connect with users who share your interests</li>
        <li>Send and receive friend requests</li>
        <li>View your friends list</li>
      </ul>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { apiService } from "../services/api";
import type { UserProfile, ApiResponse } from "../services/types";

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
      try {
        this.loading = true;
        const response: ApiResponse<UserProfile> = await apiService.getCurrentProfile();
        if (response.error) {
          this.error = response.error;
        } else if (response.data) {
          this.profile = response.data;
          this.username = this.profile.username;
        }
      } catch (err) {
        this.error = "Failed to load profile";
      } finally {
        this.loading = false;
      }
    }
  }
});
</script>

<style scoped>
.main-page {
  padding: 20px;
}

.loading, .error {
  text-align: center;
  padding: 20px;
  color: #666;
}

.error {
  color: #dc3545;
}

h1 {
  margin-bottom: 20px;
  color: #333;
}

.welcome-text {
  font-size: 1.1em;
  color: #666;
  margin-bottom: 20px;
}

.features-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.features-list li {
  padding: 10px 0;
  border-bottom: 1px solid #eee;
  color: #495057;
}

.features-list li:last-child {
  border-bottom: none;
}
</style>