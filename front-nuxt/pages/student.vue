<script setup>
const breadcrumbItems = [
  {
    title: 'Index',
    disabled: false,
    to: '/',
  },
  {
    title: 'Alumno',
    disabled: true,
  },
]
</script>

<template>
  <v-container>
    <v-breadcrumbs :items="breadcrumbItems" />
  </v-container>
</template>
