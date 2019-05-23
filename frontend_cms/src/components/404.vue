<template>
  <div id="notFound">
    <img src="<%= BASE_URL%>/static/img/logos/pyladies-circle.png" class="center-block logo">

    <div class="text-center col-sm-12">
      <h1>你迷路了</h1>
      <h4>本頁不存在</h4>
      <router-link to="/" class="vertical-5p lead">回首頁</router-link>
    </div>
  </div>
</template>
<script>
export default {
  name: "NotFound"
};
</script>

<style>
#notFound {
  padding: 10em;
  /* color: white; */
  background-color: #e2e2e2;
  min-height: 100vh;
}
</style>
