<template>
  <li class="dropdown user user-menu">
    <a href="javascript:;" class="dropdown-toggle" data-toggle="dropdown">
      <!-- The user image in the navbar-->
      <img :src="user.avatar" class="user-image" alt="User Image">
      <!-- hidden-xs hides the username on small devices so only the image appears. -->
      <span class="hidden-xs">{{user.displayName}}</span>
    </a>
    <!-- Account Info and Menu -->
    <ul class="dropdown-menu">
      <!-- <li class="user-header" style="height:auto;min-height:85px;padding-bottom:15px;">
        <p>
          <span>{{user.displayName}}</span>
          <small v-for="role in user.roles" :key="role">{{role}}</small>
        </p>
      </li>-->
      <li class="user-footer">
        <a href="javascript:;" class="btn btn-default btn-flat btn-block" @click="go_logout">
          <i class="fa fa-sign-out"></i>
          <span>Logout</span>
        </a>
      </li>
    </ul>
  </li>
</template>

<script>
import Vue from "vue";
import { mapActions } from "vuex";

export default {
  name: "UserMenu",
  props: ["user"],
  methods: {
    ...mapActions(["logout"]),
    go_logout() {
      this.logout().then(() => {
        // TODO logout href
        window.location.href = "/cms/login.html";
      });
    }
  }
};
</script>
<style>
.user-panel > .image > img {
  width: 100%;
  max-width: 40px;
  height: auto;
}
.user-panel > .info {
  padding: 12px 5px 5px 15px;
}
</style>

