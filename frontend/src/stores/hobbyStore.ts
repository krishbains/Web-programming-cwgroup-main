import { defineStore } from "pinia";

export interface Hobby {
  id: number;
  name: string;
  benefits: string;
  rating: number;
}

export const useHobbyStore = defineStore("hobbyStore", {
  state: () => ({
    hobbies: [] as Hobby[],
  }),
  actions: {
    // Fetch all hobbies from the backend
    async fetchHobbies() {
      try {
        const response = await fetch("/api/hobbies", {
          method: "GET",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          this.hobbies = await response.json();
        } else {
          console.error("Failed to fetch hobbies.");
        }
      } catch (error) {
        console.error("Error fetching hobbies:", error);
      }
    },

    // Add a new hobby
    async addHobby(newHobby: Omit<Hobby, "id">) {
      try {
        const response = await fetch("/api/hobbies", {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(newHobby),
        });
        if (response.ok) {
          const addedHobby = await response.json();
          this.hobbies.push(addedHobby);
        } else {
          console.error("Failed to add hobby.");
        }
      } catch (error) {
        console.error("Error adding hobby:", error);
      }
    },

    // Update an existing hobby
    async updateHobby(updatedHobby: Hobby) {
      try {
        const response = await fetch(`/api/hobbies/${updatedHobby.id}`, {
          method: "PUT",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updatedHobby),
        });
        if (response.ok) {
          const index = this.hobbies.findIndex((h) => h.id === updatedHobby.id);
          if (index !== -1) {
            this.hobbies[index] = updatedHobby;
          }
        } else {
          console.error("Failed to update hobby.");
        }
      } catch (error) {
        console.error("Error updating hobby:", error);
      }
    },

    // Delete a hobby
    async deleteHobby(hobbyId: number) {
      try {
        const response = await fetch(`/api/hobbies/${hobbyId}`, {
          method: "DELETE",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (response.ok) {
          this.hobbies = this.hobbies.filter((h) => h.id !== hobbyId);
        } else {
          console.error("Failed to delete hobby.");
        }
      } catch (error) {
        console.error("Error deleting hobby:", error);
      }
    },
  },
});
