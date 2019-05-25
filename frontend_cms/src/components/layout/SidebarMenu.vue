<template>
  <ul class="sidebar-menu">
    <router-link tag="li" class="pageLink" to="/event-list">
      <a>
        <i class="fa fa-calendar"></i>
        <span>活動</span>
      </a>
    </router-link>
    <router-link tag="li" class="pageLink" to="/topic-list">
      <a>
        <i class="fa fa-trophy"></i>
        <span>主題</span>
      </a>
    </router-link>
    <router-link tag="li" class="pageLink" to="/place-list">
      <a>
        <i class="fa fa-map-marker"></i>
        <span>場地</span>
      </a>
    </router-link>
    <router-link tag="li" class="pageLink" to="/tutor-list">
      <a>
        <i class="fa fa-graduation-cap"></i>
        <span>講師/助教</span>
      </a>
    </router-link>
    <router-link tag="li" class="pageLink" to="/field-list">
      <a>
        <i class="fa fa-book"></i>
        <span>領域</span>
      </a>
    </router-link>
    <!-- <router-link tag="li" class="pageLink" to="/">
      <a>
        <i class="fa fa-info-circle"></i>
        <span>FAQ</span>
      </a>
    </router-link>
    <router-link tag="li" class="pageLink" to="/">
      <a>
        <i class="fa fa-gears"></i>
        <span>權限設定</span>
      </a>
    </router-link>-->
  </ul>
</template>
<script>
export default {
  name: "SidebarMenu"
};
</script>
<style>
/* override default */
.sidebar-menu > li > a {
  padding: 12px 15px 12px 15px;
}

.sidebar-menu li.active > a > .fa-angle-left,
.sidebar-menu li.active > a > .pull-right-container > .fa-angle-left {
  animation-name: rotate;
  animation-duration: 0.2s;
  animation-fill-mode: forwards;
}

.treeview-title {
  z-index: 1;
}

@keyframes rotate {
  0% {
    transform: rotate(0deg);
  }

  100% {
    transform: rotate(-90deg);
  }
}
</style>
