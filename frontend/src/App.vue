<template>
    <main class="container pt-4">
        <!-- <div>
            <router-link
                class=""
                :to="{name: 'Main Page'}"
            >
                Main Page
            </router-link>
            |
            <router-link
                class=""
                :to="{name: 'Other Page'}"
            >
                Other Page
            </router-link>
            |
            <router-link 
                class="" 
                :to="{ name: 'Similar Users' }"
                >
                    Similar Users
                </router-link>

        </div> -->
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
            <router-link 
                class="nav-link" 
                :to="{ name: 'Similar Users' }"
                >
                    Similar Users
            </router-link>
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
</style>
