<template>
  <div class="friend-requests">
    <div class="header">
      <h2>Friend Requests</h2>
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="loading">
      Loading friend requests...
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <div v-else-if="friendRequests.length === 0" class="no-requests">
      No pending friend requests
    </div>
    
    <div v-else class="requests-list">
      <div v-for="request in friendRequests" :key="request.id" class="request-item">
        <div class="request-info">
          <span class="user-name">{{ request.sender_username }}</span>
          <span class="request-date">{{ new Date(request.created_at).toLocaleDateString() }}</span>
        </div>
        
        <div class="request-actions">
          <button 
            @click="handleRequest(request.id, 'accept')"
            class="accept-btn">
            Accept
          </button>
          <button 
            @click="handleRequest(request.id, 'reject')"
            class="reject-btn">
            Reject
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface FriendRequest {
  id: number;
  sender_username: string;
  receiver_username: string;
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
}

const friendRequests = ref<FriendRequest[]>([])
const loading = ref(false)
const error = ref('')

const fetchFriendRequests = async () => {
  try {
    loading.value = true
    error.value = ''

    const response = await fetch('/api/friend-requests/pending/')
    if (!response.ok) throw new Error('Failed to fetch requests')
    
    const data = await response.json()
    friendRequests.value = data

  } catch (err) {
    error.value = 'Error fetching friend requests'
    console.error('Error:', err)
  } finally {
    loading.value = false
  }
}

const handleRequest = async (requestId: number, action: 'accept' | 'reject') => {
  try {
    // Get CSRF token from cookie
    const csrfToken = document.cookie.split('; ')
      .find(row => row.startsWith('csrftoken='))
      ?.split('=')[1];

    if (!csrfToken) {
      throw new Error('CSRF token not found');
    }

    const response = await fetch(`/api/friend-requests/${requestId}/${action}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      credentials: 'include'
    });

    if (!response.ok) {
      const data = await response.json();
      throw new Error(data.error || `Failed to ${action} request`);
    }

    // Remove the request from the list
    friendRequests.value = friendRequests.value.filter(req => req.id !== requestId);

  } catch (err) {
    error.value = err instanceof Error ? err.message : `Error ${action}ing friend request`;
    console.error('Error:', err);

    // Clear error after 3 seconds
    setTimeout(() => {
      error.value = '';
    }, 3000);
  }
}

onMounted(() => {
  fetchFriendRequests()
})
</script>

<style scoped>
.friend-requests {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.requests-list {
  margin-top: 20px;
}

.request-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #ddd;
  margin-bottom: 10px;
  border-radius: 8px;
  background: white;
}

.request-info {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.user-name {
  font-weight: bold;
  font-size: 1.1em;
}

.request-date {
  color: #888;
  font-size: 0.8em;
}

.request-actions {
  display: flex;
  gap: 10px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.accept-btn {
  background-color: #4CAF50;
  color: white;
}

.accept-btn:hover {
  background-color: #45a049;
}

.reject-btn {
  background-color: #f44336;
  color: white;
}

.reject-btn:hover {
  background-color: #da190b;
}

.loading, .error, .no-requests {
  text-align: center;
  color: #666;
  margin-top: 20px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  border: 1px dashed #ddd;
}

.error {
  color: #dc3545;
  border-color: #dc3545;
}
</style> 