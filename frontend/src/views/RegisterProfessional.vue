<template>
  <div class="container d-flex justify-content-center align-items-center">
    <div class="card p-4 shadow">
      <h4 class="text-center">Service Professional Signup</h4>
      <form @submit.prevent="registerProfessional">
        <div class="mb-3 d-flex justify-content-between">
          <div class="w-50 me-2">
            <label class="form-label"
              >First Name<span class="text-danger">*</span></label
            >
            <input
              type="text"
              class="form-control"
              v-model="form.fname"
              required
            />
          </div>
          <div class="w-50">
            <label class="form-label">Last Name</label>
            <input type="text" class="form-control" v-model="form.lname" />
          </div>
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Email ID<span class="text-danger">*</span></label
          >
          <input
            type="email"
            class="form-control"
            v-model="form.email"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Password<span class="text-danger">*</span></label
          >
          <input
            type="password"
            class="form-control"
            v-model="form.password"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Service Category<span class="text-danger">*</span></label
          >
          <select
            class="form-select"
            v-model="form.category"
            @change="fetchServices"
          >
            <option disabled selected>Select a category</option>
            <option
              v-for="category in categories"
              :key="category"
              :value="category"
            >
              {{ category }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Service Name<span class="text-danger">*</span></label
          >
          <select class="form-select" v-model="form.service">
            <option disabled selected>Select a service</option>
            <option
              v-for="service in services"
              :key="service.id"
              :value="service.name"
            >
              {{ service.name }}
            </option>
          </select>
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Phone<span class="text-danger">*</span></label
          >
          <input
            type="tel"
            class="form-control"
            v-model="form.phone"
            maxlength="10"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Experience (Years)<span class="text-danger">*</span></label
          >
          <input
            type="number"
            class="form-control"
            v-model="form.experience"
            max="99"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label"
            >Address<span class="text-danger">*</span></label
          >
          <input
            type="text"
            class="form-control"
            v-model="form.address"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input
            type="number"
            class="form-control"
            v-model="form.pincode"
            maxlength="6"
            minlength="6"
          />
        </div>

        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>
      <div class="text-center mt-3">
        <router-link to="/">Already Registered? Login</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance"; // Use centralized Axios instance

export default {
  data() {
    return {
      form: {
        fname: "",
        lname: "",
        email: "",
        password: "",
        category: "",
        service: "",
        phone: "",
        experience: "",
        address: "",
        pincode: "",
      },
      categories: [], // Fetch from backend
      services: [],
    };
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await api.get("/api/get-categories");
        this.categories = response.data.categories;
      } catch (error) {
        console.error("Error fetching categories:", error);
      }
    },
    async fetchServices() {
      if (!this.form.category) return;
      try {
        const response = await api.get(
          `/api/get-services?category=${this.form.category.toLowerCase()}`
        );
        this.services = response.data.services;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async registerProfessional() {
      try {
        const response = await api.post(
          "/api/register-professional",
          this.form
        );
        alert(response.data.message);
        this.$router.push("/");
      } catch (error) {
        console.error("Registration failed:", error);
        alert("Registration failed. Please try again.");
      }
    },
  },
  mounted() {
    this.fetchCategories(); // Fetch categories when component loads
  },
};
</script>

<style>
.container {
  max-width: 700px;
}
.card {
  border-radius: 10px;
  width: 50% !important;
  max-height: 90vh;
  overflow-y: auto;
}
</style>
