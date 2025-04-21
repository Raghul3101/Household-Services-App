<template>
  <div class="vh-100 d-flex justify-content-center align-items-center body-bg">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form
            @submit.prevent="registerCustomer"
            class="p-4 shadow rounded bg-white"
          >
            <h4 class="text-center">Customer Signup</h4>

            <div class="mb-3 d-flex justify-content-between">
              <div class="w-50 me-2">
                <label class="form-label mb-0"
                  >First Name<span class="text-danger">*</span></label
                >
                <input
                  v-model="fname"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="w-50">
                <label class="form-label mb-0">Last Name</label>
                <input v-model="lname" type="text" class="form-control" />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label mb-0"
                >Email ID<span class="text-danger">*</span></label
              >
              <input
                v-model="email"
                type="email"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label mb-0"
                >Password<span class="text-danger">*</span></label
              >
              <input
                v-model="password"
                type="password"
                class="form-control"
                required
              />
              <small class="form-text">
                Your password must be 8-20 characters long and contain letters
                and numbers.
              </small>
            </div>

            <div class="mb-3">
              <label class="form-label mb-0"
                >Phone<span class="text-danger">*</span></label
              >
              <input
                v-model="phone"
                type="tel"
                class="form-control"
                maxlength="10"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label mb-0"
                >Address<span class="text-danger">*</span></label
              >
              <input
                v-model="address"
                type="text"
                class="form-control"
                required
              />
            </div>

            <div class="mb-3">
              <label class="form-label mb-0">Pincode</label>
              <input
                v-model="pincode"
                type="number"
                class="form-control"
                maxlength="6"
              />
            </div>

            <div class="d-flex flex-column align-items-center">
              <button type="submit" class="btn btn-primary w-100">
                Register
              </button>
              <a href="/" class="mt-2">Already Registered? Login</a>
            </div>

            <p
              v-if="message"
              :class="{ 'text-success': success, 'text-danger': !success }"
              class="text-center mt-2"
            >
              {{ message }}
            </p>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance"; // Use centralized Axios instance

export default {
  data() {
    return {
      fname: "",
      lname: "",
      email: "",
      password: "",
      phone: "",
      address: "",
      pincode: "",
      message: "",
      success: false,
    };
  },
  methods: {
    async registerCustomer() {
      try {
        const response = await api.post("/api/register-customer", {
          fname: this.fname,
          lname: this.lname,
          email: this.email,
          password: this.password,
          phone: this.phone,
          address: this.address,
          pincode: this.pincode,
        });

        this.message = response.data.message;
        this.success = true;

        setTimeout(() => {
          window.location.href = "/"; // Redirect to login after success
        }, 2000);
      } catch (error) {
        this.message = error.response?.data?.message || "Registration failed";
        console.log(error.response);
        this.success = false;
      }
    },
  },
};
</script>
