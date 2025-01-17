<template>
  <div class="user-search">
    <h2>Find Users with Similar Hobbies</h2>

    <!-- Age Filter -->
    <div class="filters">
      <div class="age-filter">
        <label>Age Range:</label>
        <div class="age-inputs">
          <input
            type="number"
            v-model="minAge"
            placeholder="Min age"
            min="0"
            max="150"
          />
          <span>to</span>
          <input
            type="number"
            v-model="maxAge"
            placeholder="Max age"
            min="0"
            max="150"
          />
          <button @click="searchUsers" class="filter-btn">Apply Filters</button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading">
      Loading users...
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <!-- Results -->
    <div v-else class="users-list">
      <div v-if="users.length === 0" class="no-results">
        No users found with similar hobbies
      </div>

      <div v-else class="user-cards">
        <div v-for="user in users" :key="user.id" class="user-card">
          <div class="user-info">
            <h3>{{ user.username }}</h3>
          </div>
          
          <div class="user-details">
            <div class="detail-row">
              <span class="detail-label">Age:</span>
              <span class="detail-value">{{ user.age || 'Not specified' }}</span>
            </div>
          </div>
          
          <div class="hobbies-section">
            <h4>Common Hobbies ({{ user.common_hobbies_count }}):</h4>
            <div class="hobby-tags">
              <span v-for="hobby in user.hobbies" :key="hobby.id" class="hobby-tag">
                {{ hobby.name }}
              </span>
            </div>
          </div>

          <button 
            v-if="user.is_friend"
            @click="unfollowFriend(user.id)"
            class="friend-request-btn unfollow-btn"
          >
            Unfollow
          </button>
          <button 
            v-else-if="user.has_pending_request"
            class="friend-request-btn pending-btn"
            disabled
          >
            Pending Request
          </button>
          <button 
            v-else
            @click="sendFriendRequest(user.id)"
            class="friend-request-btn"
            :disabled="user.friend_request_sent"
          >
            {{ user.friend_request_sent ? 'Friend Request Sent' : 'Send Friend Request' }}
          </button>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="pagination">
        <button 
          @click="changePage(currentPage - 1)"
          :disabled="currentPage === 1"
          class="page-btn"
        >
          Previous
        </button>
        <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
        <button 
          @click="changePage(currentPage + 1)"
          :disabled="currentPage === totalPages"
          class="page-btn"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Hobby {
  id: number;
  name: string;
}

interface User {
  id: number;
  username: string;
  age?: number;
  hobbies: Hobby[];
  common_hobbies_count: number;
  friend_request_sent?: boolean;
  is_friend: boolean;
  has_pending_request: boolean;
}

const users = ref<User[]>([])
const loading = ref(false)
const error = ref('')
const minAge = ref('')
const maxAge = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const totalUsers = ref(0)

const searchUsers = async () => {
  try {
    loading.value = true
    error.value = ''

    // Build query parameters
    const params = new URLSearchParams()
    if (minAge.value) params.append('min_age', minAge.value)
    if (maxAge.value) params.append('max_age', maxAge.value)
    params.append('page', currentPage.value.toString())

    const response = await fetch(`/api/profile/search_users/?${params.toString()}`)
    if (!response.ok) throw new Error('Failed to fetch users')
    
    const data = await response.json()
    users.value = data.users
    totalPages.value = data.total_pages
    totalUsers.value = data.total_users
    currentPage.value = data.current_page

  } catch (err) {
    error.value = 'Error fetching users'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const sendFriendRequest = async (userId: number) => {
  try {
    // Get CSRF token from cookie
    const csrfToken = document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];

    if (!csrfToken) {
      throw new Error('CSRF token not found');
    }

    const response = await fetch('/api/friend-requests/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        receiver: userId
      }),
      credentials: 'include'
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Failed to send friend request');
    }

    // Update UI to show request is pending
    const user = users.value.find(u => u.id === userId);
    if (user) {
      user.has_pending_request = true;
      user.friend_request_sent = true;
    }

  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : 'Error sending friend request';
    error.value = errorMessage;
    
    // Clear error after 3 seconds
    setTimeout(() => {
      error.value = '';
    }, 3000);
    
    console.error('Error:', err);
  }
}

const unfollowFriend = async (userId: number) => {
  try {
    // Get CSRF token from cookie
    const csrfToken = document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];

    if (!csrfToken) {
      throw new Error('CSRF token not found');
    }

    const response = await fetch(`/api/friend-requests/unfollow/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify({
        user_id: userId
      }),
      credentials: 'include'
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || 'Failed to unfollow user');
    }

    // Update UI to show user is no longer a friend
    const user = users.value.find(u => u.id === userId);
    if (user) {
      user.is_friend = false;
    }

  } catch (err) {
    const errorMessage = err instanceof Error ? err.message : 'Error unfollowing user';
    error.value = errorMessage;
    
    // Clear error after 3 seconds
    setTimeout(() => {
      error.value = '';
    }, 3000);
    
    console.error('Error:', err);
  }
}

const changePage = (page: number) => {
  currentPage.value = page
  searchUsers()
}

onMounted(() => {
  searchUsers()
})
</script>

<style scoped>
.user-search {
  padding: 20px;
}

.filters {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.age-filter {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.age-inputs {
  display: flex;
  gap: 10px;
  align-items: center;
}

.age-inputs input {
  width: 100px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.filter-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.filter-btn:hover {
  background-color: #0056b3;
}

.user-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.user-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: white;
}

.user-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.user-info h3 {
  margin: 0;
  color: #333;
}

.user-details {
  margin: 12px 0;
}

.detail-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.detail-label {
  font-weight: 500;
  color: #495057;
}

.detail-value {
  color: #212529;
}

.age-badge {
  display: inline-block;
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.85em;
  color: #495057;
  margin-top: 4px;
}

.hobbies-section h4 {
  margin: 0 0 10px 0;
  font-size: 0.9em;
  color: #555;
}

.hobby-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 15px;
}

.hobby-tag {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.9em;
  color: #495057;
}

.friend-request-btn {
  width: 100%;
  padding: 8px 16px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.friend-request-btn:hover {
  background-color: #218838;
}

.friend-request-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.page-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.page-btn:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.page-info {
  color: #6c757d;
}

.loading, .error, .no-results {
  text-align: center;
  padding: 40px;
  color: #666;
  background: white;
  border-radius: 8px;
  border: 1px dashed #ddd;
}

.error {
  color: #dc3545;
  border-color: #dc3545;
}

.unfollow-btn {
  background-color: #6c757d;
}

.unfollow-btn:hover {
  background-color: #5a6268;
}

.pending-btn {
  background-color: #ffc107;
  color: #212529;
  cursor: not-allowed;
}

.pending-btn:hover {
  background-color: #ffc107;
}
</style> 