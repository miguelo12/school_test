<script setup>
  const authStore = useAuthStore()

  const userName = ref('')
  const password = ref('')
  const is_error = ref(false)
  const loading = ref(false)
  const message = ref('')

  async function logIn() {
    loading.value = true
    message.value = await authStore.logIn(userName.value, password.value)
    loading.value = false

    if (authStore.is_authenticated) {
      is_error.value = false
      navigateTo('/')
    } else {
      is_error.value = true
    }
  }

  //Redirigir para no ver el login
  // if (process.client){
  //   let token = localStorage.getItem('token')
  //   if (token !== null) {
  //     navigateTo('/')
  //   }
  // }
</script>

<template>
  <v-row>
    <v-col class="d-flex align-center">
      <v-sheet
        class="mx-auto"
        min-width="500"
        rounded="lg"
      >
        <v-form validate-on="submit lazy" @submit.prevent="logIn()">
          <v-text-field
            v-model="userName"
            label="Username"
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            :rules="[
              value => {
                if (value) return true
                return 'You must enter a first name.'
              }
            ]"
          ></v-text-field>
          <v-alert v-if="message" v-text="message"></v-alert>
          <v-btn
            :loading="loading"
            class="mt-2"
            text="Submit"
            type="submit"
            block
          ></v-btn>
        </v-form>
      </v-sheet>
    </v-col>
  </v-row>
</template>