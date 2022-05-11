import { createWebHistory, createRouter } from "vue-router"
import Index from "@/components/index.vue"
import Login from "@/components/login.vue"
import Register from "@/components/register.vue"
import Profile from "@/components/profile.vue"
import Good from "@/components/good.vue"
import Sell from "@/components/sell.vue"
import Order from "@/components/order.vue"
import Soldgoods from "@/components/soldgoods.vue"
import Auctions from "@/components/auctions.vue"

const routes = [
  {
    path: "/",
    name: "index",
    component: Index,
    meta: {
      title: "proj1-3"
    }
  },
  {
    path: "/login",
    name: "login",
    component: Login,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/register",
    name: "register",
    component: Register,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/profile/:email",
    name: "profile",
    component: Profile,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/good/:id",
    name: "good",
    component: Good,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/sell",
    name: "sell",
    component: Sell,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/order",
    name: "order",
    component: Order,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/soldgoods",
    name: "soldgoods",
    component: Soldgoods,
    meta: {
      title: "proj1-3"
    }
  },
  {               
    path: "/auctions",
    name: "auctions",
    component: Auctions,
    meta: {
      title: "proj1-3"
    }
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;