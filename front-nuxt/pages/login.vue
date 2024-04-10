<script setup>
  const authStore = useAuthStore()
  
  // Form data
  const modeCreate = ref(false)
  const userName = ref('')
  const password = ref('')
  const rePassword = ref('')
  const show_pass = ref(false)

  // form extra
  const is_error = ref(false)
  const loading = ref(false)
  const message = ref('')

  async function logIn(event) {
    loading.value = true
    const results = await event

    // Verifica que el form sea valido
    if (!results.valid) {
      message.value = ''
      loading.value = false
      return
    }

    const messageLogIn = await authStore.logIn(userName.value, password.value)
    loading.value = false

    if (!authStore.is_authenticated) {
      message.value = messageLogIn
      is_error.value = true
    }
  }

  async function userCreate(event) {
    loading.value = true
    const results = await event

    // Verifica que el form sea valido
    if (!results.valid) {
      message.value = ''
      loading.value = false
      return
    }

    const dataUser = await authStore.createUser(userName.value, password.value)
    message.value = dataUser.message
    is_error.value = dataUser.is_failed
    loading.value = false

    changeMode(false)
  }

  function changeMode(removeMessage = true) {
    userName.value = ''
    password.value = ''
    rePassword.value = ''
    if (removeMessage) message.value = ''
    modeCreate.value = !modeCreate.value
  }

  //Redirigir para no ver el login
  if (process.client){
    if (authStore.is_authenticated) {
      navigateTo('/')
    }
  }
</script>

<template>
  <v-row>
    <v-col class="d-flex align-center">
      <v-sheet
        class="mx-auto"
        min-width="500"
        rounded="lg"
      >
        <v-form v-if="!modeCreate" validate-on="submit lazy" @submit.prevent="logIn">
          <v-text-field
            v-model="userName"
            label="Username"
            :rules="[
              value => {
                if (value) return true
                return 'El Username no debe estar vació.'
              }
            ]"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            :type="show_pass ? 'text' : 'password'"
            :append-inner-icon="show_pass ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[
              value => {
                if (value) return true
                return 'El Password no debe estar vació.'
              }
            ]"
            @click:append-inner="show_pass = !show_pass"
            required
          ></v-text-field>
          <v-alert
            v-if="message"
            class="mt-4 mb-4"
            :type="is_error ? 'warning' : 'success'"
            v-text="message"
          />
          <v-btn
            :loading="loading"
            class="mt-2"
            text="Iniciar sesión"
            type="submit"
            block
          />
          <v-divider class="mt-8 mb-8 border-opacity-25"/>
          <v-btn
            :loading="loading"
            variant="plain"
            class="mt-2"
            @click="changeMode()"
            block
          >Crear un usuario <v-icon icon="mdi-chevron-right"/></v-btn>
        </v-form>
        <v-form v-else validate-on="submit lazy" @submit.prevent="userCreate">
          <v-text-field
            v-model="userName"
            label="Username"
            :rules="[
              value => {
                if (value) return true
                return 'El Username no debe estar vació.'
              }
            ]"
            required
          />
          <v-text-field
            v-model="password"
            label="Password"
            :type="show_pass ? 'text' : 'password'"
            :append-inner-icon="show_pass ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[
                value => {
                  if (value) return true
                  return 'El Password no debe estar vació.'
                }
              ]"
            @click:append-inner="show_pass = !show_pass"
            required
          />
          <v-text-field
            v-model="rePassword"
            label="Re-Password"
            :type="show_pass ? 'text' : 'password'"
            :append-inner-icon="show_pass ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[
              value => {
                if (value !== password) return 'El password y el Re-Password no es el mismo.' 
                if (value) return true
                return 'El Re-Password no debe estar vació.'
              }
            ]"
            @click:append-inner="show_pass = !show_pass"
            required
          />
          <v-alert
            v-if="message"
            class="mt-4 mb-4"
            :type="is_error ? 'warning' : 'success'"
            v-text="message"
          />
          <v-btn
          :loading="loading"
          class="mt-2"
          text="Crear usuario"
          type="submit"
          block
          />
          <v-divider class="mt-8 mb-8 border-opacity-25"/>
          <v-btn
            :loading="loading"
            variant="plain"
            text="Ir a iniciar sesión"
            class="mt-2"
            @click="changeMode()"
            block
          >Ir a iniciar sesión <v-icon icon="mdi-chevron-right"/></v-btn>
        </v-form>
      </v-sheet>
    </v-col>
  </v-row>
</template>