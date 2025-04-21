<template>
  <div>
    <NavBar activeRoute="admin-search" role="admin" />
    <form
      @submit.prevent="performSearch"
      class="d-flex gap-2 justify-content-end align-items-center mt-4 me-4"
    >
      <p class="mb-0">Search by: &nbsp;</p>
      <div>
        <select v-model="searchType" class="form-select" required>
          <option value="" disabled>Select...</option>
          <option value="customer">Customer</option>
          <option value="professional">Professional</option>
          <option value="service_request">Service Request</option>
        </select>
      </div>
      <div>
        <input
          type="text"
          v-model="query"
          class="form-control rounded"
          placeholder="Enter your query"
          required
        />
      </div>
      <button type="submit" class="btn btn-primary">Search</button>
    </form>

    <div v-if="results.length > 0" class="mt-4">
      <div
        v-for="result in results"
        :key="result.id"
        class="service-category ms-auto me-auto d-flex align-items-center mt-3 w-75"
      >
        <div
          class="d-flex w-100 justify-content-between align-items-center text-light"
        >
          <p v-if="result.name" class="mb-0">{{ result.name }}</p>
          <p v-if="result.email" class="mb-0">{{ result.email }}</p>
          <p v-if="result.phone" class="mb-0">Phone: {{ result.phone }}</p>
          <p v-if="result.specialization" class="mb-0">
            Specialization: {{ result.specialization }}
          </p>
          <p v-if="result.customer_name" class="mb-0">
            Customer Name: {{ result.customer_name }}
          </p>
          <p v-if="result.professional_name" class="mb-0">
            Professional Name: {{ result.professional_name }}
          </p>
          <p v-if="result.request_date" class="mb-0">
            Request Date: {{ result.request_date }}
          </p>
          <p v-if="result.status" class="mb-0">Status: {{ result.status }}</p>
        </div>
      </div>
    </div>
    <p v-if="noResults" class="text-light mt-3">No results found.</p>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance";
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar, // Register the component
  },
  data() {
    return {
      searchType: "",
      query: "",
      results: [],
      noResults: false,
    };
  },
  methods: {
    async performSearch() {
      if (!this.searchType || !this.query) {
        alert("Please select a search type and enter a query.");
        return;
      }
      try {
        const response = await api.get("/api/search-admin", {
          params: {
            search_type: this.searchType,
            query: this.query,
          },
        });
        this.results = response.data.results;
        this.noResults = this.results.length === 0;
      } catch (error) {
        console.error("Error fetching search results:", error);
        this.results = [];
        this.noResults = true;
      }
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 1500px;
}
.service-category {
  background: transparent;
  border: 1px solid white;
  border-radius: 12px !important;
  padding: 20px;
  border-radius: 5px;
  color: white;
}
</style>
