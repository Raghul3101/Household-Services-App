<template>
  <div v-if="status === 'waiting'" class="text-center mt-5">
    <h3>Please wait for the admin to verify you</h3>
  </div>
  <div v-else-if="status === 'rejected'" class="text-center mt-5">
    <h3>You have been rejected by admin</h3>
  </div>
  <div v-else class="body-bg2">
    <NavBar activeRoute="professional-home" role="professional" />
    <!-- Today's Services -->
    <div class="mt-5">
      <h3 class="mt-4 ms-5 text-light">Today's Services</h3>
      <div v-if="todayServices.length > 0" class="container mt-5">
        <table class="table text-center bg-transparent mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Phone No.</th>
              <th>Location</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in todayServices" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.customer_name }}</td>
              <td>{{ service.phone }}</td>
              <td>{{ service.location }}</td>
              <td>
                <button
                  v-if="service.status === 'requested'"
                  class="btn btn-success me-2"
                  @click="acceptRequest(service.id)"
                >
                  Accept
                </button>
                <button
                  v-if="service.status === 'requested'"
                  class="btn btn-warning"
                  @click="rejectRequest(service.id)"
                >
                  Reject
                </button>
                <p v-else class="accepted-text">Accepted</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <h5 v-else class="mt-4 ms-5 text-light">No services for today</h5>
    </div>

    <!-- Closed Services -->
    <div class="mt-5">
      <h3 class="mt-4 ms-5 text-light">Closed Services</h3>
      <div v-if="closedServices.length > 0" class="container mt-5">
        <table class="table text-center bg-transparent mb-0">
          <thead>
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Phone No.</th>
              <th>Location</th>
              <th>Request Date</th>
              <th>Completion Date</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in closedServices" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.customer_name }}</td>
              <td>{{ service.phone }}</td>
              <td>{{ service.location }}</td>
              <td>{{ service.request_date }}</td>
              <td>{{ service.completion_date }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <h5 v-else class="mt-4 ms-5 text-light">No services completed yet</h5>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import api from "@/utils/axiosInstance"; // Import the Axios instance
import { jwtDecode } from "jwt-decode";

export default {
  components: {
    NavBar, // Register the component
  },
  data() {
    return {
      status: "",
      professional: {},
      todayServices: [],
      closedServices: [],
      userEmail: "",
    };
  },
  mounted() {
    this.extractEmailFromJWT();
    this.fetchProfessionalData();
  },
  methods: {
    extractEmailFromJWT() {
      const token = localStorage.getItem("jwt_token"); // Retrieve JWT token from localStorage
      if (token) {
        try {
          const decodedToken = jwtDecode(token); // Decode the JWT token
          const sub = decodedToken.sub ? JSON.parse(decodedToken.sub) : null; // Parse the 'sub' field
          if (sub && sub.email) {
            this.userEmail = sub.email; // Extract email from the parsed 'sub' object
          } else {
            console.error("Email not found in decoded token.");
          }
        } catch (error) {
          console.error("Error decoding JWT token:", error);
        }
      } else {
        console.error("JWT token not found in localStorage.");
      }
    },
    async fetchProfessionalData() {
      console.log("User Email:", this.userEmail);
      try {
        const response = await api.get("/api/professional-home", {
          params: { email: this.userEmail }, // Pass email from Vue state
        });
        console.log(response.data.professional.flag);
        if (
          response.data.professional.flag === "waiting" ||
          response.data.professional.flag === "rejected"
        ) {
          this.status = response.data.professional.flag;
        } else {
          this.status = "approved";
          this.professional = response.data.professional;
          this.todayServices = response.data.todayServices;
          this.closedServices = response.data.closedServices;
        }
      } catch (error) {
        console.error("Error fetching professional data:", error);
      }
    },
    async acceptRequest(id) {
      await api.post(`/api/accept-request/${id}`);
      this.fetchProfessionalData();
    },
    async rejectRequest(id) {
      await api.post(`/api/reject-request/${id}`);
      this.fetchProfessionalData();
    },
  },
};
</script>

<style scoped>
.accepted-text {
  background-color: limegreen;
  font-weight: bold;
  padding: 5px 10px 5px 10px;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  font-weight: bold;
}
th,
td {
  text-align: center;
  border-bottom: 1px solid white;
}
.table {
  width: 80vw !important;
}
.table thead th,
.table tbody td {
  background-color: transparent !important;
  color: rgb(245, 245, 245) !important;
}
</style>
