<template>
  <div>
    <NavBar activeRoute="customer-search" role="customer" />
    <div class="container mt-5 ms-2 me-2" style="max-width: 1500px !important">
      <form
        @submit.prevent="performSearch"
        class="d-flex gap-2 justify-content-end align-items-center"
      >
        <p class="mb-0">Search by: &nbsp;</p>
        <div>
          <select v-model="searchType" class="form-select" required>
            <option value="" disabled selected>Select...</option>
            <option value="name">Service Name</option>
            <option value="pincode">Pincode</option>
            <option value="rating">Minimum Rating</option>
          </select>
        </div>
        <div>
          <input
            v-model="query"
            type="text"
            class="form-control rounded"
            placeholder="Search"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary h-25 me-5">Search</button>
      </form>
      <div id="resultsContainer" class="mt-4">
        <div v-if="results.length > 0">
          <div
            v-for="result in results"
            :key="result.service.id"
            class="new-card mt-2"
          >
            <div class="d-flex align-items-center service-category text-light">
              <div
                class="d-flex w-100 justify-content-evenly align-items-center"
              >
                <p class="mb-0">{{ result.service.name }}</p>
                <p class="mb-0">Category: {{ result.service.category }}</p>
                <p class="mb-0">Price: ₹{{ result.service.price }}</p>
                <p class="mb-0">
                  Rating:
                  <span
                    v-for="i in 5"
                    :key="i"
                    :style="{
                      color:
                        i <= result.professional.rating ? 'gold' : '#cccccc',
                    }"
                    >★</span
                  >
                </p>
                <p class="mb-0">Pincode: {{ result.professional.pincode }}</p>
              </div>
              <button
                class="btn ps-3 pe-3 rounded btn-hover ms-auto"
                @click="bookService(result.service.id)"
              >
                Book
              </button>
            </div>
          </div>
        </div>
        <div v-else>
          <p class="text-light">No results found.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import api from "@/utils/axiosInstance";
export default {
  components: { NavBar },
  data() {
    return {
      searchType: "",
      query: "",
      results: [],
    };
  },
  methods: {
    // Perform search based on the search type and query
    async performSearch() {
      if (!this.searchType || !this.query) {
        alert("Please fill in all fields.");
        return;
      }

      try {
        const response = await api.get(`/api/search-customer`, {
          params: {
            search_type: this.searchType,
            query: this.query,
          },
        });

        this.results = response.data.results || [];
      } catch (error) {
        console.error("Error during search:", error);
        alert("An error occurred while searching. Please try again.");
      }
    },

    // Book the service with JWT authorization
    async bookService(serviceId) {
      try {
        const token = localStorage.getItem("jwt_token"); // Get JWT Token from localStorage
        if (!token) {
          alert("No JWT token found. Please log in again.");
          return;
        }

        const response = await api.post(
          "/api/book-service",
          { service_id: serviceId },
          {
            headers: {
              Authorization: `Bearer ${token}`, // Send JWT Token
            },
          }
        );

        alert(response.data.message); // Show message from response
      } catch (error) {
        console.error(
          "Error booking service:",
          error.response?.data || error.message
        );
        alert("Error booking the service. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
/* Add any custom styles here */
</style>
