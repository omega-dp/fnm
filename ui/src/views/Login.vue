<template>
  <form @submit.prevent="submitForm" class="max-w-sm mx-auto">
    <div class="mb-4">
      <label for="email" class="block mb-2">Email</label>
      <input v-model="email" type="email" id="email" required class="w-full px-3 py-2 border rounded" />
    </div>

    <div class="mb-4">
      <label for="password" class="block mb-2">Password</label>
      <input v-model="password" type="password" id="password" required class="w-full px-3 py-2 border rounded" />
    </div>

    <div class="flex items-center mb-4">
      <input type="checkbox" id="remember-me" class="mr-2" />
      <label for="remember-me">Remember me</label>
    </div>

    <div>
      <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded">
        Login
      </button>
    </div>
  </form>
</template>

<script>
import { useUserStore } from '@/stores/user.store';

export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  methods: {
    submitForm() {
      const userStore = useUserStore();
      userStore.login(this.email, this.password);
    },
  },
};
</script>

<style>
/* Add any custom styles here if needed */
</style>
