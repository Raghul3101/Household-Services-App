<template>
  <link
    rel="stylesheet"
    href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"
  />
  <div v-if="flag" class="text-center mt-5">
    <h3>You have been blocked by Admin</h3>
  </div>
  <div v-else class="body-bg2">
    <NavBar activeRoute="customer-home" role="customer" />
    <div class="ms-auto me-auto text-center text-light">
      <h4 class="text-color mt-5 mb-4">Looking For?</h4>

      <div class="services-container">
        <ServiceBox
          v-for="category in categories"
          :key="category"
          :category="category"
          @selectCategory="fetchServices"
        />
      </div>

      <div v-if="selectedCategory" class="mt-4">
        <h4 class="text-center">Best {{ selectedCategory }} Services</h4>
        <div v-if="services.length">
          <div
            v-for="service in services"
            :key="service.id"
            class="service-category text-light"
          >
            <p class="mb-0 me-auto">{{ service.name }}</p>
            <p class="mb-0 me-auto">Price: ₹{{ service.price }}</p>
            <p class="mb-0 me-auto">
              Rating:
              <span v-for="i in 5" :key="i">
                <i
                  class="fa-solid fa-star"
                  :style="{ color: i <= service.rating ? 'gold' : '#cccccc' }"
                ></i>
              </span>
            </p>
            <button class="btn btn-primary" @click="bookService(service.id)">
              Book Now
            </button>
          </div>
        </div>
        <p v-else class="text-center mt-3">
          No Services Available in this Category
        </p>
      </div>

      <h3 class="mt-5 ms-5 text-light text-start">Service History</h3>
      <div>
        <div v-if="serviceHistory.length" class="container mt-5">
          <table class="table ms-auto me-auto text-center bg-transparent">
            <thead>
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Service Name</th>
                <th scope="col">Professional Name</th>
                <th scope="col">Price</th>
                <th scope="col">Status</th>
                <!-- ✅ Removed Action column -->
              </tr>
            </thead>
            <tbody>
              <tr v-for="(history, index) in serviceHistory" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ history.service_name }}</td>
                <td>{{ history.professional_name }}</td>
                <td>₹{{ history.price }}</td>
                <td :class="statusClass(history.status)">
                  <!-- ✅ If status is 'accepted', show the button instead -->
                  <button
                    v-if="history.status === 'accepted'"
                    class="btn btn-primary"
                    @click="openModal(history)"
                  >
                    Close it?
                  </button>
                  <span v-else>{{ history.status }}</span>
                  <!-- Otherwise, show text -->
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <h5 v-else class="mt-4 ms-5 text-light">No services found</h5>

        <!-- Bootstrap Modal for Closing Service and Rating -->
        <div
          class="modal fade"
          id="serviceModal"
          tabindex="-1"
          aria-labelledby="serviceModalLabel"
          aria-hidden="true"
        >
          <div class="modal-dialog">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="serviceModalLabel">
                  Service Remarks
                </h5>
                <button
                  type="button"
                  class="btn-close"
                  @click="hideModal"
                  aria-label="Close"
                ></button>
              </div>
              <div class="modal-body">
                <p>
                  <strong>Service Name:</strong> {{ modalData.serviceName }}
                </p>
                <p>
                  <strong>Professional Name:</strong>
                  {{ modalData.professionalName }}
                </p>

                <!-- Rating Section -->
                <div class="mt-3">
                  <p><strong>Service Rating:</strong></p>
                  <div class="star-rating">
                    <span
                      v-for="i in 5"
                      :key="i"
                      :class="{ selected: i <= selectedRating }"
                      @click="setRating(i)"
                    >
                      <i class="fa-solid fa-star"></i>
                    </span>
                  </div>
                </div>

                <!-- Remarks Section -->
                <div class="mt-3">
                  <label for="remarks" class="form-label"
                    ><strong>Remarks (if any):</strong></label
                  >
                  <textarea
                    v-model="remarks"
                    class="form-control"
                    rows="3"
                    placeholder="Add remarks"
                  ></textarea>
                </div>
              </div>
              <div class="modal-footer">
                <button
                  type="button"
                  class="btn btn-secondary"
                  @click="hideModal"
                >
                  Close
                </button>
                <button class="btn btn-primary" @click="closeService">
                  Submit
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance";
import NavBar from "@/components/NavBar.vue";
import ServiceBox from "@/components/ServiceBox.vue";

export default {
  name: "CustomerHome",
  components: { NavBar, ServiceBox },
  data() {
    return {
      customerName: "",
      categories: [
        "AC Repair",
        "Salon",
        "Cleaning",
        "Electrical",
        "Plumbing",
        "Carpentry",
      ],
      selectedCategory: "",
      services: [],
      serviceHistory: [], // Added to store service history
      showModal: false,
      modalData: {
        serviceName: "",
        professionalName: "",
        requestId: 0,
      },
      selectedRating: 0,
      remarks: "",
      flag: "",
    };
  },
  mounted() {
    this.fetchCustomerData();
    this.fetchServiceHistory(); // Fetch service history when the component is mounted
  },
  methods: {
    async fetchCustomerData() {
      try {
        const token = localStorage.getItem("jwt_token");
        if (!token) {
          console.error("🔴 No JWT token found in localStorage!");
          return;
        }
        const response = await api.get("/api/customer", {
          headers: { Authorization: `Bearer ${token}` },
          withCredentials: true,
        });

        console.log("🟢 Customer Data:", response.data);
        this.flag = response.data.flag;
        this.customerName = response.data.name;
      } catch (error) {
        console.error("🔴 Error fetching customer data:", error);
      }
    },
    async fetchServices(category) {
      this.selectedCategory = category;
      try {
        const response = await api.get(`/api/services/${category}`);
        this.services = response.data.services;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async bookService(serviceId) {
      try {
        const token = localStorage.getItem("jwt_token"); // ✅ Get JWT Token from localStorage
        const response = await api.post(
          "/api/book-service",
          { service_id: serviceId },
          {
            headers: {
              Authorization: `Bearer ${token}`, // ✅ Send JWT Token
            },
          }
        );
        alert(response.data.message);
        this.fetchServiceHistory();
      } catch (error) {
        console.error(
          "Error booking service:",
          error.response?.data || error.message
        );
      }
    },
    async fetchServiceHistory() {
      try {
        const token = localStorage.getItem("jwt_token"); // Get JWT token from localStorage
        if (!token) {
          console.error("🔴 No JWT token found in localStorage!");
          return;
        }

        // Make GET request to fetch service history with Authorization header
        const response = await api.get("/api/service-history", {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token in the Authorization header
          },
        });

        console.log("🟢 Service History:", response.data);
        this.serviceHistory = response.data.history;
        console.log(this.serviceHistory);
      } catch (error) {
        console.error(
          "Error fetching service history:",
          error.response?.data || error.message
        );
      }
    },

    openModal(history) {
      this.modalData.serviceName = history.service_name;
      this.modalData.professionalName = history.professional_name;
      this.remarks = "";
      this.modalData.requestId = history.requestId;
      console.log(this.modalData.requestId);
      this.selectedRating = 0;
      this.showModal = true;
      const modal = document.getElementById("serviceModal");
      if (modal) {
        modal.classList.add("show");
        modal.style.display = "block";
        document.body.classList.add("modal-open");
      }
    },

    setRating(rating) {
      this.selectedRating = rating;
    },
    statusClass(status) {
      return {
        "text-warning": status === "requested",
        "text-success": status === "accepted",
        "text-danger": status === "rejected",
        "text-primary": status === "closed",
      };
    },

    async closeService() {
      if (!this.selectedRating) {
        alert("Please select a rating");
        return;
      }
      const payload = {
        request_id: this.modalData.requestId,
        rating: this.selectedRating,
      };

      try {
        const token = localStorage.getItem("jwt_token");
        if (!token) {
          console.error("No JWT token found");
          return;
        }

        const response = await api.post("/api/close_service", payload, {
          headers: { Authorization: `Bearer ${token}` },
        });

        alert(response.data.msg);

        // ✅ Hide modal properly
        this.showModal = false;
        this.hideModal(); // Call hideModal function
        this.fetchServiceHistory(); // Refresh service history
      } catch (error) {
        console.error("Error closing service", error);
        alert("Error closing the service. Please try again.");
      }
    },

    hideModal() {
      const modal = document.getElementById("serviceModal");
      if (modal) {
        modal.classList.remove("show");
        modal.style.display = "none";
        document.body.classList.remove("modal-open");
        document.querySelector(".modal-backdrop")?.remove();
      }
    },
  },
};
</script>

<style scoped>
.services-container {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
}

.service-category {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border: 2px solid white;
  border-radius: 18px;
  padding: 15px;
  margin-top: 10px;
  width: 100%;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.btn-primary {
  padding: 5px 15px;
}
th,
td {
  padding: 15px !important;
  text-align: center;
  border-bottom: 1px solid white;
}
.service-history-item {
  margin-top: 20px;
  border: 1px solid white;
  border-radius: 10px;
  padding: 15px;
}

.text-color {
  color: #212529;
  font-size: 45px !important;
}

.table {
  width: 80vw !important;
}
.table thead th,
.table tbody td {
  background-color: transparent !important;
  color: rgb(245, 245, 245) !important;
}

.star-rating {
  display: flex;
  justify-content: center;
  gap: 5px;
  font-size: 1.5rem;
  cursor: pointer;
}

.star-rating .selected {
  color: gold;
}

.modal-content {
  background-color: #343a40;
  color: white;
  border-radius: 10px;
}

.modal-header {
  border-bottom: 1px solid #555;
}

.modal-footer {
  border-top: 1px solid #555;
}
</style>
