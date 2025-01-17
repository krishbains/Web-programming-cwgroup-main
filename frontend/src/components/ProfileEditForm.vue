<template>
  <form @submit.prevent="handleSubmit" class="edit-form">
    <!-- Profile Information Section -->
    <div class="section">
      <h3>Profile Information</h3>
      <div class="form-group">
        <label for="username">Username</label>
        <input
            id="username"
            v-model="formData.username"
            type="text"
            class="form-control"
        />
        <span v-if="errors.username" class="error-message">
          {{ errors.username }}
        </span>
      </div>

      <div class="form-group">
        <label for="email">Email</label>
        <input
            id="email"
            v-model="formData.email"
            type="email"
            class="form-control"
        />
        <span v-if="errors.email" class="error-message">
          {{ errors.email }}
        </span>
      </div>

      <div class="form-group">
        <label for="date_of_birth">Date of Birth</label>
        <input
            id="date_of_birth"
            v-model="formData.date_of_birth"
            type="date"
            class="form-control"
        />
      </div>
    </div>

    <!-- Password Change Section -->
    <div class="section">
      <h3>Change Password</h3>
      <div class="form-group">
        <label for="current_password">Current Password</label>
        <input
            id="current_password"
            v-model="formData.current_password"
            type="password"
            class="form-control"
        />
        <span v-if="errors.current_password" class="error-message">
          {{ errors.current_password }}
        </span>
      </div>

      <div class="form-group">
        <label for="new_password">New Password</label>
        <input
            id="new_password"
            v-model="formData.new_password"
            type="password"
            class="form-control"
        />
        <span v-if="errors.new_password" class="error-message">
          {{ errors.new_password }}
        </span>
      </div>
    </div>

    <div class="form-actions">
      <button type="submit" class="save-btn">Save Changes</button>
      <button type="button" @click="$emit('cancel')" class="cancel-btn">
        Cancel
      </button>
    </div>
  </form>
</template>

<script>
import {defineComponent} from 'vue';
import {apiService} from '@/services/api';

export default defineComponent({
  name: 'ProfileEditForm',

  props: {
    initialData: {
      type: Object,
      required: true
    }
  },

  data() {
    return {
      formData: {
        username: this.initialData.username,
        email: this.initialData.email,
        date_of_birth: this.initialData.date_of_birth,
        current_password: '',
        new_password: ''
      },
      errors: {
        username: '',
        email: '',
        current_password: '',
        new_password: ''
      }
    };
  },

  methods: {
    async handleSubmit() {
      // Clear previous errors
      this.errors = {
        username: '',
        email: '',
        current_password: '',
        new_password: ''
      };

      // Create form data with only the filled fields
      const updateData = {};
      for (const [key, value] of Object.entries(this.formData)) {
        if (value !== '' && value !== null && value !== undefined) {
          updateData[key] = value;
        }
      }

      const response = await apiService.updateProfile(updateData);

      if (response.status === 200) {
        // Check if password was updated
        if (updateData.new_password) {
          alert('Password updated successfully!');
          this.formData.current_password = '';
          this.formData.new_password = '';
        } else {
          this.$emit('save', this.formData);
          alert('Profile updated successfully!');
        }
      } else if (response.error) {
        try {
          const errorData = typeof response.error === 'string' ?
              JSON.parse(response.error) : response.error;

          for (const field in errorData) {
            if (this.errors.hasOwnProperty(field)) {
              this.errors[field] = Array.isArray(errorData[field])
                  ? errorData[field][0]
                  : errorData[field];
            }
          }
        } catch {
          alert('An error occurred while updating the profile');
        }
      }
    }
  }
});
</script>

<style scoped>
.edit-form {
  margin-top: 20px;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.section h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #343a40;
}

.form-group {
  margin-bottom: 20px;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 5px;
}

.error-message {
  color: #dc3545;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.save-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-btn:hover {
  background-color: #0056b3;
}

.cancel-btn {
  padding: 8px 16px;
  background-color: #6c757d;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn:hover {
  background-color: #5a6268;
}
</style>