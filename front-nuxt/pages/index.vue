<script setup>
  const authStore = useAuthStore()
</script>

<template>
  <h1>Bienvenido {{ authStore.username }}</h1>
  <AlertDefault>
    index
  </AlertDefault>
</template>