<template>
  <NavBar activeRoute="customer-summary" role="customer" />
  <div>
    <h3 class="ms-3 text-light">Summary</h3>
    <div
      class="text-light w-100 h-75 d-flex gap-5 justify-content-center align-items-center"
    >
      <div>
        <h5>Requests Overview</h5>
        <canvas id="requests-chart" width="400" height="300"></canvas>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from "@/components/NavBar.vue";
import api from "@/utils/axiosInstance";
import Chart from "chart.js/auto";

export default {
  components: { NavBar },
  data() {
    return {
      customerId: null,
      customerName: "",
      requested: 0,
      accepted: 0,
      closed: 0,
      rejected: 0,
      requests: 0,
    };
  },
  mounted() {
    this.fetchSummaryData();
  },
  methods: {
    async fetchSummaryData() {
      try {
        const token = localStorage.getItem("jwt_token");
        console.log("🔵 Sending Authorization Header:", token);

        const response = await api.get("/api/summary-customer", {
          headers: {
            Authorization: `Bearer ${token}`, // ✅ Ensure token is sent
          },
        });

        console.log("✅ Response Data:", response.data);

        // Assign data to variables
        this.customerId = response.data.id;
        this.customerName = response.data.name;
        this.requested = response.data.requested;
        this.accepted = response.data.accepted;
        this.closed = response.data.closed;
        this.rejected = response.data.rejected;

        this.renderChart();
      } catch (error) {
        console.error("❌ Error fetching summary data:", error);
      }
    },

    renderChart() {
      const ctxRequests = document
        .getElementById("requests-chart")
        .getContext("2d");
      new Chart(ctxRequests, {
        type: "bar",
        data: {
          labels: ["Requested", "Ongoing", "Closed", "Rejected"],
          datasets: [
            {
              label: "Requests",
              data: [this.requested, this.accepted, this.closed, this.rejected],
              backgroundColor: [
                "rgb(255, 202, 79)",
                "#5aff8e",
                "rgb(54, 162, 235)",
                "rgb(255, 99, 132)",
              ],
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
    },
  },
};
</script>

<style scoped>
/* Add custom styles if necessary */
</style>
