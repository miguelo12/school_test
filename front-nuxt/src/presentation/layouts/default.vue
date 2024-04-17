<template>
  <v-app>
    <v-layout>
      <slot name="header" />
      <v-main>
        <slot />
      </v-main>
      <slot name="footer" />
    </v-layout>
  </v-app>
</template>
