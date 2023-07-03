<template>
  <div>
    <button @click="fetchUsers">Fetch Users</button>
    <table v-if="users.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Username</th>
          <th>Is Admin</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.is_admin }}</td>
        </tr>
      </tbody>
    </table>
    <div v-else>No users to display</div>
  </div>
</template>

<script>
import { useUserListStore } from '@/stores/user.store';

export default {
  setup() {
    const userListStore = useUserListStore();

    const fetchUsers = () => {
      userListStore.fetchUsers();
    };

    return {
      users: userListStore.users,
      fetchUsers,
    };
  },
};
</script>
