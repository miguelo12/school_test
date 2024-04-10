<script setup>
const authStore = useAuthStore()
</script>

<template>
  <v-app-bar
    scroll-behavior="elevate"
    color="purple-darken-3"
  >
    <v-app-bar-title>School</v-app-bar-title>
    <div v-if="authStore.is_authenticated">
      {{ authStore.username }}
    </div>
    <v-btn
      v-if="authStore.is_authenticated"
      icon="mdi-logout"
      @click="authStore.logOut()"
    />
  </v-app-bar>
</template>
