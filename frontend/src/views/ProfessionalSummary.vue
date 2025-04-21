<template>
  <NavBar activeRoute="professional-summary" role="professional" />
  <div class="container-fluid text-light">
    <h3 class="mt-3">Summary</h3>
    <div class="summary-container">
      <div>
        <h5>Requests Overview</h5>
        <canvas ref="requestsChart"></canvas>
      </div>

      <div>
        <h5>Rating</h5>
        <canvas ref="ratingChart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance"; // Use centralized Axios instance
import Chart from "chart.js/auto";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "ProfessionalSummary",
  components: { NavBar },
  data() {
    return {
      name: "",
      received: 0,
      accepted: 0,
      closed: 0,
      rejected: 0,
      rating: 0,
      requestsChartInstance: null,
      ratingChartInstance: null,
    };
  },
  mounted() {
    this.fetchSummaryData();
  },
  methods: {
    async fetchSummaryData() {
      try {
        const response = await api.get("/api/professional-summary", {
          withCredentials: true,
        });
        const data = response.data;

        this.name = data.name;
        this.received = data.received;
        this.accepted = data.accepted;
        this.closed = data.closed;
        this.rejected = data.rejected;
        this.rating = data.rating;

        this.$nextTick(() => this.renderCharts()); // Ensure DOM is ready
      } catch (error) {
        console.error("Error fetching summary data:", error);
      }
    },
    renderCharts() {
      // Destroy existing charts if they exist
      if (this.requestsChartInstance) this.requestsChartInstance.destroy();
      if (this.ratingChartInstance) this.ratingChartInstance.destroy();

      // Requests Chart
      const requestsChartCtx = this.$refs.requestsChart.getContext("2d");
      this.requestsChartInstance = new Chart(requestsChartCtx, {
        type: "bar",
        data: {
          labels: ["Received", "Accepted", "Closed", "Rejected"],
          datasets: [
            {
              label: "Requests",
              data: [this.received, this.accepted, this.closed, this.rejected],
              backgroundColor: ["#FFCA4F", "#5AFF8E", "#36A2EB", "#FF6384"],
              borderColor: "white",
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: false },
          },
          scales: {
            x: { ticks: { color: "white" } },
            y: { ticks: { color: "white" } },
          },
        },
      });

      // Rating Chart
      const ratingChartCtx = this.$refs.ratingChart.getContext("2d");
      this.ratingChartInstance = new Chart(ratingChartCtx, {
        type: "doughnut",
        data: {
          datasets: [
            {
              data: [this.rating, 5 - this.rating],
              backgroundColor: ["#DFC100", "#CFD8DC"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: "top" },
            title: {
              display: true,
              text: `Average Rating: ${this.rating}/5`,
              color: "white",
            },
          },
        },
      });
    },
  },
};
</script>

<style scoped>
.container-fluid {
  padding: 20px;
}

.summary-container {
  display: flex;
  justify-content: center;
  gap: 50px;
  align-items: center;
  height: 75vh;
}

h5 {
  text-align: center;
}
</style>
