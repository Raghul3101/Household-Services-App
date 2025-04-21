<template>
  <NavBar activeRoute="professional-search" role="professional" />
  <div class="container mt-5">
    <h2 class="text-light">Search for Requests</h2>

    <!-- Search Form -->
    <form
      @submit.prevent="performSearch"
      class="d-flex gap-2 justify-content-end align-items-center"
    >
      <p class="mb-0 text-light">Search by: &nbsp;</p>
      <select v-model="searchType" class="form-select" required>
        <option value="" disabled selected>Select...</option>
        <option value="date">Date</option>
        <option value="pincode">Pincode</option>
        <option value="location">Location</option>
      </select>
      <input
        v-model="query"
        type="text"
        class="form-control rounded"
        placeholder="Enter your query"
        required
      />
      <button type="submit" class="btn btn-primary h-25 me-5">Search</button>
    </form>

    <!-- Results Section -->
    <div v-if="results.length > 0" class="mt-4">
      <div
        v-for="result in results"
        :key="result.result.id"
        class="service-category d-flex align-items-center mt-2 text-light"
      >
        <div class="d-flex w-100 justify-content-between align-items-center">
          <p class="mb-0">Customer Name: {{ result.result.customer_name }}</p>
          <p class="mb-0">Phone: {{ result.result.phone }}</p>
          <p class="mb-0">Location: {{ result.result.location }}</p>
          <p class="mb-0">Request Date: {{ result.result.request_date }}</p>
          <p class="mb-0">Status: {{ result.result.status }}</p>
        </div>
      </div>
    </div>

    <p v-if="errorMessage" class="text-danger mt-3">{{ errorMessage }}</p>
    <p v-if="noResultsMessage" class="text-light mt-3">
      {{ noResultsMessage }}
    </p>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance"; // Use centralized Axios instance
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar, // Navigation Bar Component
  },
  data() {
    return {
      searchType: "",
      query: "",
      results: [],
      errorMessage: "",
      noResultsMessage: "",
    };
  },
  methods: {
    async performSearch() {
      if (!this.searchType || !this.query) {
        this.errorMessage = "Please fill in all fields.";
        return;
      }

      // Update URL
      const newUrl = `/search-professional?search_type=${this.searchType}&query=${this.query}`;
      history.pushState(null, "", newUrl);

      try {
        this.errorMessage = "";
        this.noResultsMessage = "";
        this.results = [];

        // Make API call
        const response = await api.get("/api/search-professional", {
          params: {
            search_type: this.searchType,
            query: this.query,
          },
          withCredentials: true,
        });

        console.log("API Response:", response.data);

        if (response.data.results.length > 0) {
          this.results = response.data.results;
        } else {
          this.noResultsMessage = "No matching records found.";
        }
      } catch (error) {
        console.error("Search error:", error);
        this.errorMessage = error.response?.data?.error || "An error occurred.";
      }
    },
  },
};
</script>

<style scoped>
.service-category {
  background-color: rgba(255, 255, 255, 0.1);
  padding: 10px;
  border-radius: 5px;
}
</style>
