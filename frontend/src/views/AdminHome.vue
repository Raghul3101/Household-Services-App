<template>
  <div class="admin-home">
    <NavBar activeRoute="admin-home" role="admin" />
    <h3 class="mt-4 ms-5 width-fit text-light">Services</h3>

    <!-- Services Table -->
    <table class="table ms-auto me-auto">
      <thead>
        <tr>
          <th>ID</th>
          <th>Service Name</th>
          <th>Base Price</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(service, index) in services" :key="service.id">
          <td>{{ index + 1 }}</td>
          <td>{{ service.name }}</td>
          <td>{{ service.price }}</td>
          <td>
            <button
              class="btn btn-primary btn-sm"
              @click="editService(service)"
            >
              Edit
            </button>
            <button
              class="ms-1 btn btn-danger btn-sm"
              @click="deleteService(service.id)"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- New Service Button -->
    <button class="new-service-btn" @click="showModal = true">
      + New Service
    </button>

    <!-- Add Service Modal -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal-box">
        <h2>Add New Service</h2>
        <form @submit.prevent="addService">
          <input
            v-model="newService.name"
            class="form-control"
            placeholder="Service Name"
            required
          />
          <select v-model="newService.category" class="form-select" required>
            <option value="" disabled selected>Select a category</option>
            <option value="ac repair">AC Repair</option>
            <option value="salon">Salon</option>
            <option value="cleaning">Cleaning</option>
            <option value="electrical">Electrical</option>
            <option value="plumbing">Plumbing</option>
            <option value="carpentry">Carpentry</option>
          </select>
          <textarea
            v-model="newService.description"
            placeholder="Description"
            class="form-control"
            required
          ></textarea>
          <input
            v-model="newService.price"
            type="number"
            placeholder="Price"
            class="form-control"
            required
          />
          <button type="submit" class="btn btn-primary">Add Service</button>
          <button
            type="button"
            class="btn btn-secondary"
            @click="showModal = false"
          >
            Cancel
          </button>
        </form>
      </div>
    </div>

    <!-- Other Sections Remain Unchanged -->
    <!-- Professional -->
    <h3 class="mt-5 ms-5 width-fit text-light">Professionals</h3>
    <table
      v-if="professionals.length > 0"
      class="table ms-auto me-auto text-center bg-transparent mb-0"
    >
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Name</th>
          <th scope="col">Experience</th>
          <th scope="col">Service Name</th>
          <th scope="col">Phone</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="professional in professionals" :key="professional.id">
          <td>{{ professional.id }}</td>
          <td>{{ professional.fname }}</td>
          <td>{{ professional.experience }}</td>
          <td>{{ professional.service }}</td>
          <td>{{ professional.phone }}</td>
          <td>
            <template v-if="professional.flag === 'waiting'">
              <button
                @click="approveProfessional(professional.id)"
                class="btn btn-success btn-sm"
              >
                Approve
              </button>
              <button
                @click="rejectProfessional(professional.id)"
                class="btn btn-warning btn-sm ms-2"
              >
                Reject
              </button>
            </template>
            <span v-else>{{
              professional.flag.charAt(0).toUpperCase() +
              professional.flag.slice(1)
            }}</span>
            <button
              @click="deleteProfessional(professional.id)"
              class="btn btn-danger btn-sm ms-2"
            >
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h5 v-else class="mt-4 ms-5 text-light">No Professionals available</h5>

    <!-- Customers -->
    <h3 class="mt-5 width-fit ms-5 text-light">Customers</h3>
    <table
      v-if="customers.length > 0"
      class="table ms-auto me-auto text-center bg-transparent mb-0"
    >
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">First Name</th>
          <th scope="col">Last Name</th>
          <th scope="col">Phone</th>
          <th scope="col">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="customer in customers" :key="customer.id">
          <td>{{ customer.id }}</td>
          <td>{{ customer.fname }}</td>
          <td>{{ customer.lname }}</td>
          <td>{{ customer.phone }}</td>
          <td>
            <button
              v-if="customer.flag"
              @click="unblockCustomer(customer.id)"
              class="btn btn-success btn-sm"
            >
              Unblock
            </button>
            <button
              v-else
              @click="blockCustomer(customer.id)"
              class="btn btn-danger btn-sm"
            >
              Block
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <h5 v-else class="mt-4 ms-5 text-light">No Customers available</h5>

    <!-- Requests -->
    <h3 class="mt-5 width-fit ms-5 text-light">Service Requests</h3>
    <table
      v-if="requests.length > 0"
      class="table ms-auto me-auto text-center bg-transparent mb-0"
    >
      <thead>
        <tr>
          <th scope="col">ID</th>
          <th scope="col">Customer</th>
          <th scope="col">Professional</th>
          <th scope="col">Service Name</th>
          <th scope="col">Request Date</th>
          <th scope="col">Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in requests" :key="request.id">
          <td>{{ request.id }}</td>
          <td>{{ request.customer }}</td>
          <td>{{ request.professional }}</td>
          <td>{{ request.service_name }}</td>
          <td>{{ request.request_date }}</td>
          <td>
            <p :class="statusClass(request.status)">
              {{ capitalizeFirstLetter(request.status) }}
            </p>
          </td>
        </tr>
      </tbody>
    </table>
    <h5 v-else class="mt-4 ms-5 text-light pb-3">No Requests available</h5>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance"; // Use the API instance
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      services: [],
      newService: { name: "", category: "", description: "", price: "" },
      showModal: false,
      professionals: [],
      customers: [],
      requests: [],
    };
  },
  mounted() {
    this.fetchServices();
    this.fetchProfessionals();
    this.fetchCustomers();
    this.fetchRequests();
  },
  methods: {
    async fetchServices() {
      const response = await api.get("/api/admin-home");
      this.services = response.data.services;
    },
    async addService() {
      await api.post("/api/add-service", this.newService);
      this.fetchServices();
      this.showModal = false;
    },
    async editService(service) {
      const newPrice = prompt("Enter new price:", service.price);
      if (newPrice) {
        await api.post(`/api/edit-service/${service.id}`, { price: newPrice });
        this.fetchServices();
      }
    },
    async deleteService(serviceId) {
      await api.post(`/api/delete-service/${serviceId}`);
      this.fetchServices();
    },
    async fetchProfessionals() {
      try {
        console.log("Fetching professionals...");
        const response = await api.get("/api/professionals");
        console.log("Received response:", response.data);
        this.professionals = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    async approveProfessional(id) {
      try {
        await api.post(`/api/approve_professional/${id}`);
        this.fetchProfessionals();
      } catch (error) {
        console.error("Error approving professional:", error);
      }
    },
    async rejectProfessional(id) {
      try {
        await api.post(`/api/reject_professional/${id}`);
        this.fetchProfessionals();
      } catch (error) {
        console.error("Error rejecting professional:", error);
      }
    },
    async deleteProfessional(id) {
      try {
        await api.delete(`/api/delete_professional/${id}`);
        this.fetchProfessionals();
      } catch (error) {
        console.error("Error deleting professional:", error);
      }
    },
    async fetchCustomers() {
      try {
        const response = await api.get("/api/customers");
        this.customers = response.data.customers;
      } catch (error) {
        console.error("Error fetching customers:", error);
      }
    },
    async blockCustomer(customerId) {
      try {
        await api.post(`/api/block_customer/${customerId}`);
        this.fetchCustomers();
      } catch (error) {
        console.error("Error blocking customer:", error);
      }
    },
    async unblockCustomer(customerId) {
      try {
        await api.post(`/api/unblock_customer/${customerId}`);
        this.fetchCustomers();
      } catch (error) {
        console.error("Error unblocking customer:", error);
      }
    },
    async fetchRequests() {
      try {
        const response = await api.get("/api/service-requests");
        this.requests = response.data.requests;
      } catch (error) {
        console.error("Error fetching service requests:", error);
      }
    },
    capitalizeFirstLetter(str) {
      return str.charAt(0).toUpperCase() + str.slice(1);
    },
    statusClass(status) {
      if (status === "accepted") return "accepted-text";
      if (status === "requested") return "requested-text";
      if (status === "rejected") return "rejected-text";
      return "closed-text";
    },
  },
};
</script>

<style scoped>
.width-fit {
  width: fit-content;
}
.admin-home {
  text-align: center;
}
th,
td {
  padding: 15px;
  text-align: center;
  border-bottom: 1px solid white;
}
.new-service-btn {
  margin-top: 10px;
  cursor: pointer;
  background: none;
  color: lightblue;
  border: none;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
.modal-box {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 300px;
  text-align: center;
}
.table {
  width: 80vw !important;
}
.table thead th,
.table tbody td {
  background-color: transparent !important;
  color: rgb(245, 245, 245) !important;
}
.accepted-text {
  background-color: green;
  padding: 5px 10px 5px 10px;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  font-weight: bold;
}
.requested-text {
  background-color: orange;
  padding: 5px 10px 5px 10px;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  font-weight: bold;
}
.rejected-text {
  background-color: red;
  padding: 5px 10px 5px 10px;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  font-weight: bold;
}
.closed-text {
  padding: 5px 10px 5px 10px;
  border-radius: 8px;
  width: fit-content;
  margin-left: auto;
  margin-right: auto;
  background-color: gray;
  font-weight: bold;
}
</style>
