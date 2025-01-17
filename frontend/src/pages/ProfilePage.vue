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

        <!-- User's Hobbies Section -->
        <div class="hobbies-section">
          <h2>My Hobbies</h2>
          <div class="hobbies-list">
            <span
              v-for="hobby in profile?.hobbies"
              :key="hobby.id"
              class="hobby-tag"
            >
              {{ hobby.name }}
              <button
                @click="removeHobby(hobby.id)"
                class="remove-hobby-btn"
                title="Remove hobby"
              >
                ×
              </button>
            </span>
            <span v-if="!profile?.hobbies?.length" class="no-hobbies">
              No hobbies added yet
            </span>
          </div>
        </div>

        <!-- Available Hobbies Section -->
        <div class="available-hobbies-section">
          <h2>Available Hobbies</h2>
          <div class="hobbies-list">
            <span
              v-for="hobby in availableHobbies"
              :key="hobby.id"
              class="hobby-tag"
              :class="{ 'hobby-added': hobby.user_has_hobby }"
            >
              {{ hobby.name }}
              <button
                v-if="!hobby.user_has_hobby"
                @click="addHobby(hobby.id)"
                class="add-hobby-btn"
                title="Add to my hobbies"
              >
                +
              </button>
            </span>
          </div>

          <!-- Create New Hobby Form -->
          <div class="create-hobby-form">
            <input
              v-model="newHobby"
              type="text"
              placeholder="Create a new hobby"
              class="hobby-input"
              @keyup.enter="handleCreateHobby"
            />
            <button
              @click="handleCreateHobby"
              class="create-hobby-btn"
              :disabled="!newHobby.trim()"
            >
              Create Hobby
            </button>
          </div>
          <p v-if="hobbyError" class="error-message">{{ hobbyError }}</p>
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
import {defineComponent} from 'vue';
import {useUserStore} from '@/stores/userStore';
import ProfileEditForm from '@/components/ProfileEditForm.vue';
import {apiService} from '@/services/api';

export default defineComponent({
  name: 'ProfilePage',

  components: {
    ProfileEditForm
  },

  data() {
    return {
      isEditing: false,
      newHobby: '',
      hobbyError: '',
      availableHobbies: [],
      loadingHobbies: false,
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
      return this.userStore.loading || this.loadingHobbies;
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
    },

    async fetchHobbies() {
      try {
        this.loadingHobbies = true;
        const response = await apiService.getAllHobbies();
        if (response.data) {
          this.availableHobbies = response.data;
        }
      } catch (error) {
        this.hobbyError = 'Failed to load hobbies';
      } finally {
        this.loadingHobbies = false;
      }
    },

    async handleCreateHobby() {
      if (!this.newHobby.trim()) return;

      try {
        this.hobbyError = '';
        const response = await apiService.createHobby(this.newHobby.trim());

        if (response.error) {
          this.hobbyError = response.error;
          return;
        }

        // Refresh both profile and available hobbies
        await Promise.all([
          this.userStore.fetchProfile(),
          this.fetchHobbies()
        ]);

        this.newHobby = ''; // Clear the input
      } catch (error) {
        this.hobbyError = 'Failed to create hobby. Please try again.';
      }
    },

    async addHobby(hobbyId) {
      try {
        this.hobbyError = '';
        const response = await apiService.addHobbyToProfile(hobbyId);

        if (response.error) {
          this.hobbyError = response.error;
          return;
        }

        // Refresh both profile and available hobbies
        await Promise.all([
          this.userStore.fetchProfile(),
          this.fetchHobbies()
        ]);
      } catch (error) {
        this.hobbyError = 'Failed to add hobby. Please try again.';
      }
    },

    async removeHobby(hobbyId) {
      try {
        this.hobbyError = '';
        const response = await apiService.removeHobbyFromProfile(hobbyId);

        if (response.error) {
          this.hobbyError = response.error;
          return;
        }

        // Refresh both profile and available hobbies
        await Promise.all([
          this.userStore.fetchProfile(),
          this.fetchHobbies()
        ]);
      } catch (error) {
        this.hobbyError = 'Failed to remove hobby. Please try again.';
      }
    }
  },

  async created() {
    if (!this.profile) {
      await this.userStore.fetchProfile();
    }
    await this.fetchHobbies();
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

.hobbies-section,
.available-hobbies-section {
  margin-top: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.available-hobbies-section {
  background-color: #e9ecef;
}

.hobbies-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.hobby-tag {
  background-color: #fff;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.hobby-added {
  background-color: #e2e3e5;
}

.no-hobbies {
  color: #6c757d;
  font-style: italic;
}

.create-hobby-form {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.hobby-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.create-hobby-btn {
  padding: 8px 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.create-hobby-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.create-hobby-btn:hover:not(:disabled) {
  background-color: #218838;
}

.add-hobby-btn,
.remove-hobby-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0 4px;
  font-size: 16px;
  line-height: 1;
  color: #6c757d;
}

.add-hobby-btn:hover {
  color: #28a745;
}

.remove-hobby-btn:hover {
  color: #dc3545;
}

.error-message {
  color: #dc3545;
  font-size: 14px;
  margin-top: 8px;
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