import { defineStore } from 'pinia';
import { apiService } from '../services/api';
import type { UserProfile } from '../services/types';

interface UserState {
  profile: UserProfile | null;
  loading: boolean;
  error: string | null;
}

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    profile: null,
    loading: false,
    error: null,
  }),

  getters: {
    hasProfile: (state) => !!state.profile,
    userHobbies: (state) => state.profile?.hobbies || [],
  },

  actions: {
    async fetchProfile() {
      this.loading = true;
      this.error = null;

      const response = await apiService.getCurrentProfile();

      if (response.error || !response.data) {
        this.error = response.error || 'No data received';
        this.loading = false;
        return;
      }

      this.profile = response.data;
      this.loading = false;
    },

    async updateProfile(profileData: Partial<UserProfile>) {
      this.loading = true;
      this.error = null;

      const response = await apiService.updateProfile(profileData);

      if (response.error || !response.data) {
        this.error = response.error || 'No data received';
        this.loading = false;
        return false;
      }

      this.profile = response.data;
      this.loading = false;
      return true;
    }
  }
});