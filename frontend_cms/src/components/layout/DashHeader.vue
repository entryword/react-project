<template>
  <header class="main-header">
    <span class="logo-mini">
      <b>PyLadies</b>
      CMS
    </span>
    <!-- Header Navbar -->
    <nav class="navbar navbar-static-top" role="navigation">
      <!-- Sidebar toggle button-->
      <a href="javascript:;" class="sidebar-toggle" data-toggle="offcanvas" role="button">
        <span class="sr-only">Toggle navigation</span>
      </a>

      <!-- Navbar Right Menu -->
      <div class="navbar-custom-menu">
        <ul class="nav navbar-nav">
          <user-menu :user="user"></user-menu>
        </ul>
      </div>
    </nav>
  </header>
</template>

<script>
import { mapState } from "vuex";
import UserMenu from "./UserMenu";

export default {
  name: "DashHeader",
  components: {
    UserMenu
  },
  props: ["user"],
  computed: {
    ...mapState(["userInfo"])
  }
};
</script>

<style scoped>
.main-header {
  background-color: var(--pyladies-pink);
}
.skin-red .main-header .navbar {
  background-color: transparent;
}
.logo-mini {
  float: left;
  width: 230px;
  color: #fff;
  text-align: center;
  line-height: 50px;
  font-size: 24px;
}

.sidebar-collapse .logo-mini {
  display: none;
}
</style>
