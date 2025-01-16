<template>
    <main class="container pt-4">
        <nav class="navigation">
            <router-link
                class="nav-link"
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Profile page'}"
            >
                Profile Page
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Friend Requests'}"
            >
                Friend Requests
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Friends List'}"
            >
                Friends
            </router-link>
            <router-link
                class="nav-link"
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
        </nav>
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
.navigation {
    display: flex;
    gap: 10px;
    padding: 15px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 20px;
}

.nav-link {
    text-decoration: none;
    color: #495057;
    padding: 8px 16px;
    border-radius: 4px;
    transition: all 0.2s ease;
}

.nav-link:hover {
    background: #e9ecef;
}

.nav-link.router-link-active {
    background: #007bff;
    color: white;
}
</style>
