<template>
    <main class="container pt-4">
        <div>
            <router-link
                class="router-link"
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class="router-link"
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
            |
            <router-link
                class="router-link"
                :to="{name: 'Profile Page'}"
            >
                Profile Page
            </router-link>
            |
            <router-link
                class="router-link"
                :to="{name: 'All Hobbies'}"
            >
                All Hobbies
            </router-link>
        </div>
        <RouterView class="flex-shrink-0" />
    </main>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

export default defineComponent({
    components: { RouterView },
});
</script>

<style scoped>
.router-link {
    text-decoration: none;
    color: blue;
    font-weight: bold;
    padding: 0 5px;
    transition: color 0.3s ease;
}

.router-link:hover {
    color: purple;
}
</style>
