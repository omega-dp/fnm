<template>
  <div className="flex h-screen bg-gray-50 dark:bg-gray-900" id="app">
    <!-- Use the useUserStore to check authentication status -->
    <template v-if="userStore.loggedIn">
      <Sidebar :isSideMenuOpen="isSideMenuOpen" @close-side-menu="isSideMenuOpen = false"/>

      <div className="flex flex-col flex-1 w-full">
        <Navigation @open-side-menu="isSideMenuOpen = !isSideMenuOpen"/>
        <div className="p-6 dark:text-white">
          <RouterView/>
        </div>
      </div>
    </template>

    <!-- Show the login page if not authenticated -->
    <template v-else>
      <Login/>
    </template>
  </div>
</template>

<script setup lang="js">
import {ref} from 'vue';
import Login from "@/views/Login.vue";
import '@/assets/main.min.css';
import {useUserStore} from './stores/user.store'; // Import the useUserStore

import {RouterView} from 'vue-router';
import Sidebar from './components/Sidebar.vue';
import Navigation from './components/Navigation.vue';

const isSideMenuOpen = ref(false);

const userStore = useUserStore(); // Initialize the useUserStore
</script>
