<template>
  <div class="vh-100 d-flex container-fluid align-items-center">
    <form @submit.prevent="handleLogin" class="mx-auto login-box">
      <h4 class="text-center">A - Z Household Services</h4>

      <div class="mb-3 mt-5">
        <label for="email" class="form-label mb-0">Email ID</label>
        <input
          v-model="email"
          type="text"
          class="form-control"
          id="email"
          required
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label mb-0">Password</label>
        <input
          v-model="password"
          type="password"
          class="form-control"
          id="password"
          required
        />
      </div>

      <div class="d-flex flex-column align-items-center mt-4">
        <button type="submit" id="login-btn" class="btn btn-primary w-50">
          Login
        </button>
        <a href="/register-customer" class="mt-2">Create Account?</a>
        <a href="/register-professional">Register as a Professional</a>
      </div>

      <p v-if="errorMessage" class="text-danger text-center mt-2">
        {{ errorMessage }}
      </p>
    </form>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance"; // Import the Axios instance

export default {
  data() {
    return {
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleLogin() {
      // Allow "admin" without email validation
      if (this.email.toLowerCase() === "admin" && this.password === "abc123") {
        this.$router.push("/admin-home");
        return;
      }

      // Validate email format for normal users
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(this.email)) {
        this.errorMessage = "Please enter a valid email.";
        return;
      }

      try {
        const response = await api.post("/login", {
          email: this.email,
          password: this.password,
        });

        if (response.status === 200) {
          const { user_type, id, access_token } = response.data;

          // Store token securely
          localStorage.setItem("jwt_token", access_token);
          localStorage.setItem("user_id", id);
          localStorage.setItem("user_type", user_type);

          // Redirect user based on role
          if (user_type === "customer") {
            this.$router.push("/customer-home");
          } else if (user_type === "professional") {
            this.checkProfessionalStatus();
          }
        }
      } catch (error) {
        this.errorMessage = "Invalid email or password.";
      }
    },
    async checkProfessionalStatus() {
      try {
        const response = await api.get("/api/professional-status", {
          params: { email: this.email },
        });

        const status = response.data.status;
        if (status === "approved") {
          this.$router.push("/professional-home");
        } else if (status === "waiting") {
          this.errorMessage = "Your account is pending admin approval.";
        } else if (status === "rejected") {
          this.errorMessage = "Your account has been rejected by the admin.";
        }
      } catch (error) {
        this.errorMessage = "Error verifying your account status.";
      }
    },
  },
};
</script>

<style scoped>
.body-bg {
  background-color: #f8f9fa;
  height: 100vh;
}

.login-box {
  width: 100%;
  max-width: 400px;
  background: white;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}
</style>
