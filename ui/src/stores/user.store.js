import { defineStore } from 'pinia';
import axios from 'axios';

// Create a new Axios instance with the base URL
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // Replace this with your API base URL
});

// Add an interceptor to include the access token in requests
api.interceptors.request.use(config => {
  const userStore = useUserStore();
  if (userStore.loggedIn) {
    config.headers.Authorization = `Bearer ${userStore.access}`;
  }
  return config;
});


export const useUserStore = defineStore('user', {
  state: () => ({
    refresh: localStorage.getItem('refresh') || '',
    access: localStorage.getItem('access') || '',
    loggedIn: localStorage.getItem('loggedIn') === 'true',
  }),
  actions: {
    async login(email, password) {
      try {
        const response = await api.post('/users/auth/login/', {
          email,
          password,
        });

        this.refresh = response.data.refresh;
        this.access = response.data.access;
        this.loggedIn = true;

        // Store the tokens and loggedIn state in local storage
        localStorage.setItem('refresh', this.refresh);
        localStorage.setItem('access', this.access);
        localStorage.setItem('loggedIn', 'true');
      } catch (error) {
        console.error(error);
      }
    },
    logout() {
      this.refresh = '';
      this.access = '';
      this.loggedIn = false;

      // Clear the tokens and loggedIn state from local storage
      localStorage.removeItem('refresh');
      localStorage.removeItem('access');
      localStorage.setItem('loggedIn', 'false');
    },
  },
});

export const useUserListStore = defineStore('userList', {

  state: () => ({
    users: [],
  }),
  actions: {
    async fetchUsers() {
      try {
        const res = await api.get('/users/list/');
        this.users = res.data;
      } catch (error) {
        console.error(error);
      }
    },
  },
});


export const useProfileStore = defineStore('profile', {
  state: () => ({
    id: null,
    user: null,
    email: '',
    username: null,
    avatar: '',
    contactNo: '',
    address: '',
    jobTitle: '',
    jobGroup: '',
    department: '',
    dateOfBirth: '',
  }),
  actions: {
    async fetchProfile() {
      try {
        const response = await api.get('/users/profile/me/');
        const profileData = response.data;
        // Update the store state with the profile data
        Object.assign(this, profileData);

      } catch (error) {
        console.error(error);
      }
    },
  },
});

