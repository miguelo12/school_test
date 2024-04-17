<script setup>
const authStore = useAuthStore()
</script>

<template>
  <NuxtLayout>
    <template #header>
      <NuxtLayout
        name="header"
        :auth-store="authStore"
      />
    </template>
    <template #default>
      <NuxtLayout name="breadcrumb" />
      <v-container class="pa-4 text-center" />
    </template>
    <template #footer>
      <NuxtLayout name="footer" />
    </template>
  </NuxtLayout>
</template>
