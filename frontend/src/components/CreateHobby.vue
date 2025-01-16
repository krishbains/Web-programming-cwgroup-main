<template>
  <div class="my-4 py-3">
    <!-- Open Add New Hobby Modal Button -->
    <button
      type="button"
      class="btn btn-success"
      @click="openModal"
    >
      Add Hobby
    </button>

    <!-- Add New Hobby Modal -->
    <div v-if="showModal" class="modal fade show" style="display: block;">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add New Hobby</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <!-- Hobby Name -->
            <label for="name" class="form-label">Hobby Name</label>
            <input
              v-model="formData.name"
              id="name"
              class="form-control"
              placeholder="Enter hobby name"
            />

            <!-- Hobby Benefits -->
            <label for="benefits" class="form-label mt-2">Benefits</label>
            <textarea
              v-model="formData.benefits"
              id="benefits"
              class="form-control"
              placeholder="Describe the benefits"
              rows="3"
            ></textarea>

            <!-- Hobby Rating -->
            <label for="rating" class="form-label mt-2">Rating (out of 5)</label>
            <input
              v-model.number="formData.rating"
              id="rating"
              type="number"
              class="form-control"
              min="1"
              max="5"
              placeholder="Enter rating (1-5)"
            />
          </div>

          <!-- Error Alert -->
          <div v-if="showErrorAlert" class="alert alert-danger">
            <button type="button" class="btn-close" @click="closeModal"></button>
            <p>Failed to add Hobby</p>
            <p>{{ errorMessage }}</p>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
            <button type="button" class="btn btn-primary" @click="submitForm">Save</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useUserStore } from "../stores/userStore.ts";

export default defineComponent({
  data() {
    return {
      formData: { name: "", benefits: "", rating: 1 },
      showErrorAlert: false,
      errorMessage: "",
      showModal: false,
      store: useUserStore(),
    };
  },
  methods: {
    openModal() {
      this.showModal = true;
      this.resetForm();
    },
    closeModal() {
      this.showModal = false;
    },
    resetForm() {
      this.formData = { name: "", benefits: "", rating: 1 };
      this.showErrorAlert = false;
      this.errorMessage = "";
    },
    async submitForm() {
      try {
        const csrfToken = this.store.getCookie("csrftoken", document.cookie);
        const response = await fetch("/api/hobbies", {
          method: "POST",
          credentials: "same-origin",
          headers: {
            "Content-Type": "application/json",
            "x-csrftoken": csrfToken,
          },
          body: JSON.stringify(this.formData),
        });

        if (response.ok) {
          this.closeModal();
          this.$emit("hobby-created", this.formData);
        } else {
          this.showErrorAlert = true;
          const responseContent = await response.json();
          this.errorMessage = responseContent.message || "Failed to add hobby";
        }
      } catch (error) {
        this.showErrorAlert = true;
        this.errorMessage = "Error communicating with the server.";
      }
    },
  },
});
</script>

<style scoped>
.modal-content {
  border-radius: 8px;
}

.btn-success {
  background-color: #28a745;
}

.modal-body {
  font-size: 1rem;
}

.modal-footer .btn {
  padding: 0.5rem 1rem;
}

.alert-danger {
  font-size: 0.9rem;
}
</style>
