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

        <div class="detail-item">
          <strong>Hobbies:</strong>
          <div class="hobby-tags">
            <span v-for="hobby in profile?.hobbies" :key="hobby.id" class="hobby-tag">
              {{ hobby.name }}
            </span>
          </div>
        </div>

        <!-- Add Hobby Dropdown -->
        <div class="add-hobby">
          <label for="hobby-select" class="form-label">Add Hobby</label>
          <select v-model="selectedHobby" id="hobby-select" class="form-select">
            <option v-for="hobby in allHobbies" :key="hobby.id" :value="hobby.id">
              {{ hobby.name }}
            </option>
          </select>
          <button @click="addHobby" class="btn btn-primary mt-2">Add Hobby</button>
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
      isEditing: false,
      selectedHobby: null, // To store the selected hobby ID
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
    },
    allHobbies() {
      return this.userStore.allHobbies; // Fetch all available hobbies from the store
    }
  },

  methods: {
    async handleProfileUpdate(updatedData) {
      const success = await this.userStore.updateProfile(updatedData);
      if (success) {
        this.isEditing = false;
      }
    },

    async addHobby() {
      if (this.selectedHobby) {
        // Add hobby to the profile
        const success = await this.userStore.addHobbyToProfile(this.selectedHobby);
        if (success) {
          // Optionally, update the profile's hobbies list here
          this.profile.hobbies.push(this.allHobbies.find(hobby => hobby.id === this.selectedHobby));
          this.selectedHobby = null; // Clear the selected hobby after adding
        }
      }
    }
  },

  async created() {
    if (!this.profile) {
      await this.userStore.fetchProfile();
    }
    // Fetch all hobbies available to the user
    if (!this.userStore.allHobbies.length) {
      await this.userStore.fetchAllHobbies();
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

.add-hobby {
  margin-top: 20px;
}

.add-hobby select {
  width: 100%;
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
