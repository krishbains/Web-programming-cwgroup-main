<template>
  <div class="profile-page">
    <div v-if="loading" class="loading">
      Loading...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="profile-container">
      <h1>Profile</h1>

      <!-- Profile View Mode -->
      <div v-if="!isEditing" class="profile-details">
        <div class="detail-item">
          <strong>Username:</strong> {{ profile?.username }}
        </div>
        <div class="detail-item">
          <strong>Email:</strong> {{ profile?.email }}
        </div>
        <div class="detail-item">
          <strong>Date of Birth:</strong>
          {{ profile?.date_of_birth ? new Date(profile.date_of_birth).toLocaleDateString() : 'Not set' }}
        </div>

        <button @click="isEditing = true" class="edit-btn">
          Edit Profile
        </button>
      </div>

      <!-- Edit Mode -->
      <profile-edit-form
        v-else
        :initial-data="profile"
        @save="handleProfileUpdate"
        @cancel="isEditing = false"
      />
    </div>
  </div>
</template>

<script>
import { defineComponent } from 'vue';
import { useUserStore } from '@/stores/userStore';
import ProfileEditForm from '@/components/ProfileEditForm.vue';

export default defineComponent({
  name: 'ProfilePage',

  components: {
    ProfileEditForm
  },

  data() {
    return {
      isEditing: false
    };
  },

  computed: {
    userStore() {
      return useUserStore();
    },
    profile() {
      return this.userStore.profile;
    },
    loading() {
      return this.userStore.loading;
    },
    error() {
      return this.userStore.error;
    }
  },

  methods: {
    async handleProfileUpdate(updatedData) {
      const success = await this.userStore.updateProfile(updatedData);
      if (success) {
        this.isEditing = false;
      }
    }
  },

  async created() {
    if (!this.profile) {
      await this.userStore.fetchProfile();
    }
  }
});
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-details {
  margin-top: 20px;
}

.detail-item {
  margin-bottom: 15px;
}

.hobby-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.hobby-tag {
  background-color: #e9ecef;
  padding: 5px 10px;
  border-radius: 15px;
  font-size: 0.9em;
}

.edit-btn {
  margin-top: 20px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn:hover {
  background-color: #0056b3;
}

.loading {
  text-align: center;
  margin-top: 50px;
}

.error {
  color: red;
  text-align: center;
  margin-top: 50px;
}
</style>