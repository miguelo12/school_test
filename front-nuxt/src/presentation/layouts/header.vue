<script setup>
const props = defineProps({
  authStore: Object,
})
</script>

<template>
  <v-app-bar
    scroll-behavior="elevate"
    color="purple-darken-3"
  >
    <v-app-bar-title>School</v-app-bar-title>

    <v-spacer />

    <v-toolbar-items>
      <v-btn
        v-if="props.authStore.is_authenticated"
        icon="mdi-logout"
        variant="text"
        min-width="100"
        :ripple="false"
      >
        {{ props.authStore.username }}
      </v-btn>
      <v-divider vertical />
      <v-btn
        v-if="props.authStore.is_authenticated"
        icon="mdi-logout"
        min-width="60"
        @click="props.authStore.logOut()"
      />
    </v-toolbar-items>
  </v-app-bar>
</template>
