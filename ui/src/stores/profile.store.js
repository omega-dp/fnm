import { defineStore } from 'pinia';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api', // Replace this with your API base URL
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
        const response = await api.get('/users/profile/');
        const profileData = response.data;
        // Update the store state with the profile data
        Object.assign(this, profileData);
      } catch (error) {
        console.error(error);
      }
    },
  },
});
