<script setup>
const authStore = useAuthStore()
</script>

<template>
    <v-app-bar scroll-behavior="elevate" color="purple-darken-4">
        <v-app-bar-title>School</v-app-bar-title>
        <v-btn v-if="authStore.is_authenticated" icon="mdi-heart"></v-btn>
    </v-app-bar>
</template>
