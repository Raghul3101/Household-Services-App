import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../views/LoginPage.vue";
import RegisterCustomer from "@/views/RegisterCustomer.vue";
import RegisterProfessional from "@/views/RegisterProfessional.vue";
import AdminHome from "@/views/AdminHome.vue";
import AdminSearch from "@/views/AdminSearch.vue";
import AdminSummary from "@/views/AdminSummary.vue";
import ProfessionalHome from "@/views/ProfessionalHome.vue";
import ProfessionalSearch from "@/views/ProfessionalSearch.vue";
import ProfessionalSummary from "@/views/ProfessionalSummary.vue";
import CustomerHome from "@/views/CustomerHome.vue";
import CustomerSearch from "@/views/CustomerSearch.vue";
import CustomerSummary from "@/views/CustomerSummary.vue";

const routes = [
  {
    path: "/",
    name: "login",
    component: LoginPage,
  },
  {
    path: "/register-customer",
    name: "register-customer",
    component: RegisterCustomer,
  },
  {
    path: "/register-professional",
    name: "register-professional",
    component: RegisterProfessional,
  },
  {
    path: "/admin-home",
    name: "admin-home",
    component: AdminHome,
  },
  {
    path: "/admin-search",
    name: "admin-search",
    component: AdminSearch,
  },
  {
    path: "/admin-summary",
    name: "admin-summary",
    component: AdminSummary,
  },
  {
    path: "/professional-home",
    name: "professional-home",
    component: ProfessionalHome,
  },
  {
    path: "/professional-search",
    name: "professional-search",
    component: ProfessionalSearch,
  },
  {
    path: "/professional-summary",
    name: "professional-summary",
    component: ProfessionalSummary,
  },
  {
    path: "/customer-home",
    name: "customer-home",
    component: CustomerHome,
  },
  {
    path: "/customer-search",
    name: "customer-search",
    component: CustomerSearch,
  },
  {
    path: "/customer-summary",
    name: "customer-summary",
    component: CustomerSummary,
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
