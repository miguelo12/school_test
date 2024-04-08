<template>
  <v-layout>
    <AppHeader />
    <v-main style="--v-layout-top: 0!; --v-layout-bottom: 0;">
        <slot />
    </v-main>
    <AppFooter />
  </v-layout>
</template>