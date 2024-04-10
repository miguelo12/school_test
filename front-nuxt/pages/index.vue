<script setup>
const authStore = useAuthStore()

const items = [
  {
    title: 'Usuarios',
    text: 'Agregar nuevos usuarios o ver un usuario',
    img: 'img/colegio.jpg',
    to: 'user',
  },
  {
    title: 'Profesores',
    text: 'Agregar nuevos profesores o ver un profesor',
    img: 'img/profesor.jpg',
    to: 'teacher',
  },
  {
    title: 'Alumnos',
    text: 'Agregar nuevos alumnos o ver un alumno',
    img: 'img/alumnos.jpg',
    to: 'student',
  },
  {
    title: 'Cursos',
    text: 'Agregar nuevos cursos o ver un curso',
    img: 'img/curso.jpg',
    to: 'course',
  },
]
</script>

<template>
  <v-container class="pa-4 text-center">
    <div class="text-h1">
      Bienvenido {{ authStore.username }}
    </div>
    <v-row
      align="center"
      class="fill-height"
      justify="center"
    >
      <template
        v-for="(item, i) in items"
        :key="i"
      >
        <v-col
          cols="12"
          md="4"
        >
          <v-hover v-slot="{ isHovering, props }">
            <v-card
              :class="{ 'on-hover': isHovering }"
              :elevation="!isHovering ? 12 : 2"
              v-bind="props"
              class="bg-black"
              @click="navigateTo(`/${item.to}`)"
            >
              <v-img
                :src="item.img"
                height="225px"
                class="img-card-hover"
                style="opacity: 0.4"
                cover
              />
              <v-overlay
                :model-value="isHovering"
                class="align-center justify-center"
                scrim="black"
                contained
              >
                <v-card-title class="text-h5 text-white d-flex flex-column">
                  <p class="mt-4">
                    {{ item.title }}
                  </p>
                  <p class="ma-0 text-body-1">
                    {{ item.text }}
                  </p>
                </v-card-title>
              </v-overlay>
            </v-card>
          </v-hover>
        </v-col>
      </template>
    </v-row>
  </v-container>
</template>
