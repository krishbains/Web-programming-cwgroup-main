<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface FriendRequest {
  id: number;
  sender: {
    id: number;
    name: string;
    email: string;
  };
  receiver: {
    id: number;
    name: string;
    email: string;
  };
  status: 'pending' | 'accepted' | 'rejected';
  created_at: string;
}

const friendRequests = ref<FriendRequest[]>([])

// Debug data
const debugRequests: FriendRequest[] = [
  {
    id: 1,
    sender: {
      id: 101,
      name: "Debug User 1",
      email: "debug1@test.com"
    },
    receiver: {
      id: 1,
      name: "Current User",
      email: "current@test.com"
    },
    status: 'pending',
    created_at: new Date().toISOString()
  },
  {
    id: 2,
    sender: {
      id: 102,
      name: "Debug User 2",
      email: "debug2@test.com"
    },
    receiver: {
      id: 1,
      name: "Current User",
      email: "current@test.com"
    },
    status: 'pending',
    created_at: new Date().toISOString()
  },
  {
    id: 3,
    sender: {
      id: 103,
      name: "Debug User 3",
      email: "debug3@test.com"
    },
    receiver: {
      id: 1,
      name: "Current User",
      email: "current@test.com"
    },
    status: 'pending',
    created_at: new Date().toISOString()
  }
]

const initializeDebugRequests = () => {
  // Only initialize if debugPendingRequests doesn't exist in localStorage
  if (!localStorage.getItem('debugPendingRequests')) {
    localStorage.setItem('debugPendingRequests', JSON.stringify(debugRequests))
  }
}

const resetDebugData = () => {
  localStorage.setItem('debugPendingRequests', JSON.stringify(debugRequests))
  localStorage.setItem('debugFriends', JSON.stringify([]))
  fetchFriendRequests()
}

const fetchFriendRequests = async () => {
  try {
    // In debug mode, get requests from localStorage
    const storedRequests = localStorage.getItem('debugPendingRequests')
    friendRequests.value = storedRequests ? JSON.parse(storedRequests) : []
    return

    // Normal API call (commented out for debug)
    /*const response = await fetch('/api/friend-requests/pending/')
    if (!response.ok) throw new Error('Failed to fetch requests')
    friendRequests.value = await response.json()*/
  } catch (error) {
    console.error('Error fetching friend requests:', error)
  }
}

const handleRequest = async (requestId: number, action: 'accept' | 'reject') => {
  try {
    // Debug mode: remove the request from localStorage
    const storedRequests = JSON.parse(localStorage.getItem('debugPendingRequests') || '[]')
    const updatedRequests = storedRequests.filter((req: FriendRequest) => req.id !== requestId)
    localStorage.setItem('debugPendingRequests', JSON.stringify(updatedRequests))

    if (action === 'accept') {
      // Store the accepted request in localStorage for the Friends page
      const acceptedRequest = friendRequests.value.find(req => req.id === requestId)
      if (acceptedRequest) {
        const existingFriends = JSON.parse(localStorage.getItem('debugFriends') || '[]')
        existingFriends.push({
          id: acceptedRequest.sender.id,
          name: acceptedRequest.sender.name,
          email: acceptedRequest.sender.email,
          hobbies: ['Debug Hobby 1', 'Debug Hobby 2'],
          date_of_birth: '1990-01-01'
        })
        localStorage.setItem('debugFriends', JSON.stringify(existingFriends))
      }
    }
    
    // Update the UI
    friendRequests.value = updatedRequests
    return

    // Normal API call (commented out for debug)
    /*const response = await fetch(`/api/friend-requests/${requestId}/${action}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    if (!response.ok) throw new Error(`Failed to ${action} request`)
    await fetchFriendRequests()*/
  } catch (error) {
    console.error(`Error ${action}ing friend request:`, error)
  }
}

onMounted(() => {
  initializeDebugRequests()
  fetchFriendRequests()
})
</script>

<template>
  <div class="friend-requests">
    <div class="header">
      <h2>Friend Requests</h2>
      <button @click="resetDebugData" class="reset-btn">
        Reset Debug Data
      </button>
    </div>
    
    <div v-if="friendRequests.length === 0" class="no-requests">
      No pending friend requests
    </div>
    
    <div v-else class="requests-list">
      <div v-for="request in friendRequests" :key="request.id" class="request-item">
        <div class="request-info">
          <span class="user-name">{{ request.sender.name }}</span>
          <span class="user-email">{{ request.sender.email }}</span>
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

.reset-btn {
  background-color: #6c757d;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.reset-btn:hover {
  background-color: #5a6268;
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

.user-email {
  color: #666;
  font-size: 0.9em;
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

.no-requests {
  text-align: center;
  color: #666;
  margin-top: 20px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  border: 1px dashed #ddd;
}
</style> 