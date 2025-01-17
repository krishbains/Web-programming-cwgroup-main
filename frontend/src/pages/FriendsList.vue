<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Friend {
  id: number;
  name: string;
  email: string;
  hobbies: string[];
  date_of_birth: string;
}

const friends = ref<Friend[]>([])

const fetchFriends = async () => {
  try {
    // In debug mode, get friends from localStorage
    const debugFriends = JSON.parse(localStorage.getItem('debugFriends') || '[]')
    friends.value = debugFriends
    return

    // Normal API call (commented out for debug)
    /*const response = await fetch('/api/friend-requests/friends/')
    if (!response.ok) throw new Error('Failed to fetch friends')
    friends.value = await response.json()*/
  } catch (error) {
    console.error('Error fetching friends:', error)
  }
}

const unfollowFriend = async (friendId: number) => {
  try {
    // Debug mode: remove friend from localStorage
    const debugFriends = JSON.parse(localStorage.getItem('debugFriends') || '[]')
    const updatedFriends = debugFriends.filter((friend: Friend) => friend.id !== friendId)
    localStorage.setItem('debugFriends', JSON.stringify(updatedFriends))
    friends.value = updatedFriends
    return

    // Normal API call (commented out for debug)
    /*const response = await fetch(`/api/friends/${friendId}/unfollow/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    if (!response.ok) throw new Error('Failed to unfollow friend')
    await fetchFriends()*/
  } catch (error) {
    console.error('Error unfollowing friend:', error)
  }
}

const calculateAge = (dateOfBirth: string): number => {
  const today = new Date()
  const birthDate = new Date(dateOfBirth)
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  
  return age
}

onMounted(() => {
  fetchFriends()
})
</script>

<template>
  <div class="friends-list">
    <h2>My Friends</h2>
    
    <div v-if="friends.length === 0" class="no-friends">
      You haven't added any friends yet
    </div>
    
    <div v-else class="friends-grid">
      <div v-for="friend in friends" :key="friend.id" class="friend-card">
        <div class="friend-header">
          <h3>{{ friend.name }}</h3>
          <span class="age">{{ calculateAge(friend.date_of_birth) }} years old</span>
        </div>
        <p class="email">{{ friend.email }}</p>
        <div class="hobbies">
          <h4>Hobbies:</h4>
          <div class="hobby-tags">
            <span v-for="hobby in friend.hobbies" :key="hobby" class="hobby-tag">
              {{ hobby }}
            </span>
          </div>
        </div>
        <button @click="unfollowFriend(friend.id)" class="unfollow-btn">
          Unfollow
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.friends-list {
  padding: 20px;
}

.friends-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.friend-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  background: white;
  transition: transform 0.2s ease;
  position: relative;
}

.friend-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.friend-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.friend-header h3 {
  margin: 0;
  color: #333;
}

.age {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
  color: #495057;
}

.email {
  color: #666;
  margin-bottom: 15px;
  font-size: 0.9em;
}

.hobbies h4 {
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

.unfollow-btn {
  width: 100%;
  padding: 8px 16px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.2s ease;
}

.unfollow-btn:hover {
  background-color: #c82333;
}

.no-friends {
  text-align: center;
  color: #666;
  margin-top: 20px;
  padding: 40px;
  background: white;
  border-radius: 8px;
  border: 1px dashed #ddd;
}
</style> 