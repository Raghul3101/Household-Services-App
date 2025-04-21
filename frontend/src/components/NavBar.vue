<template>
  <nav class="navbar navbar-expand-lg sticky-top text-light">
    <div class="container-fluid">
      <h3 class="navbar-brand text-light mb-0">Welcome, {{ role }}</h3>
      <button class="navbar-toggler" type="button" @click="toggleNavbar">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div :class="['collapse', 'navbar-collapse', { show: isNavbarOpen }]">
        <div class="navbar-nav ms-auto">
          <router-link
            class="nav-link"
            :class="{ active: activeRoute === role + '-home' }"
            :to="'/' + role + '-home'"
          >
            Home
          </router-link>
          <router-link
            class="nav-link"
            :class="{ active: activeRoute === role + '-search' }"
            :to="'/' + role + '-search'"
          >
            Search
          </router-link>
          <router-link
            class="nav-link"
            :class="{ active: activeRoute === role + '-summary' }"
            :to="'/' + role + '-summary'"
          >
            Summary
          </router-link>
          <a class="nav-link logout-btn" href="#" @click="logout">Logout</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
  props: {
    activeRoute: String,
    role: String, // 'admin' or 'customer'
  },
  data() {
    return {
      userName: this.role, // Default to role if name is not fetched
      isNavbarOpen: false,
    };
  },
  mounted() {},
  methods: {
    toggleNavbar() {
      this.isNavbarOpen = !this.isNavbarOpen;
    },
    logout() {
      localStorage.removeItem("jwt_token");
      localStorage.removeItem("user_id");
      localStorage.removeItem("user_type");
      window.location.href = "/"; // Redirect to login page
    },
  },
};
</script>

<style scoped>
.navbar {
  font-weight: 500;
  color: white !important;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
  background-image: linear-gradient(90deg, #050e13, #163f56, #378ea1, #45b7d1);
}
.nav-link.active {
  background-color: #f8f8f8;
  border-radius: 8px;
}
.navbar-toggler {
  border: none;
}
.navbar-toggler:focus {
  box-shadow: none;
}
.logout-btn {
  color: red !important;
}
</style>
