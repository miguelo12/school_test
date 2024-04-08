<script setup>
const authStore = useAuthStore()
</script>

<template>
    <v-app-bar scroll-behavior="elevate" color="purple-darken-4">
        <v-app-bar-title>School</v-app-bar-title>
        <v-btn v-if="authStore.is_authenticated" @click="authStore.logOut()" icon="mdi-logout"></v-btn>
    </v-app-bar>
</template>
