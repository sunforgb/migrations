import { createRouter, createWebHistory } from "vue-router";
import EmployeeView from '../views/Employee.vue';
const routes = [
  {
    path: "/",
    name: "home",
    component: EmployeeView,
    meta: {
      authRequired: false
    }
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
