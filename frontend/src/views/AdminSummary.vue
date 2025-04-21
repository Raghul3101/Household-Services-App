<template>
  <NavBar activeRoute="admin-summary" role="admin" />
  <div class="container-fluid text-light">
    <h3 class="mt-3">Summary</h3>
    <div class="summary-container">
      <div>
        <h5>Users Count</h5>
        <canvas id="users-chart"></canvas>
      </div>

      <div>
        <h5>Requests Overview</h5>
        <canvas id="requests-chart"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/utils/axiosInstance";
import Chart from "chart.js/auto";
import NavBar from "@/components/NavBar.vue";

export default {
  name: "AdminSummary",
  components: {
    NavBar, // Register the component
  },
  data() {
    return {
      professionals: 0,
      customers: 0,
      requests: 0,
      accepted: 0,
      closed: 0,
      rejected: 0,
    };
  },
  mounted() {
    this.fetchSummaryData();
  },
  methods: {
    async fetchSummaryData() {
      try {
        const response = await api.get("/api/admin-summary");
        const data = response.data;

        this.professionals = data.professionals;
        this.customers = data.customers;
        this.requests = data.requests;
        this.accepted = data.accepted;
        this.closed = data.closed;
        this.rejected = data.rejected;

        this.renderCharts();
      } catch (error) {
        console.error("Error fetching summary data:", error);
      }
    },
    renderCharts() {
      const usersChartCtx = document
        .getElementById("users-chart")
        .getContext("2d");
      new Chart(usersChartCtx, {
        type: "pie",
        data: {
          labels: ["Professionals", "Customers"],
          datasets: [
            {
              data: [this.professionals, this.customers],
              backgroundColor: ["rgb(255, 99, 132)", "rgb(54, 162, 235)"],
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
              labels: {
                color: "white",
                boxWidth: 20,
                padding: 15,
              },
              align: "start",
            },
          },
          layout: {
            padding: {
              top: 10,
            },
          },
        },
      });

      const requestsChartCtx = document
        .getElementById("requests-chart")
        .getContext("2d");
      new Chart(requestsChartCtx, {
        type: "bar",
        data: {
          labels: ["Requests", "Accepted", "Closed", "Rejected"],
          datasets: [
            {
              label: "Requests",
              data: [this.requests, this.accepted, this.closed, this.rejected],
              backgroundColor: [
                "rgb(255, 202, 79)",
                "#5aff8e",
                "rgb(54, 162, 235)",
                "rgb(255, 99, 132)",
              ],
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
            x: {
              ticks: { color: "white" },
            },
            y: {
              ticks: { color: "white" },
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
