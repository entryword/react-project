<template>
  <footer class="main-footer">
    <strong>
      <a href="https://tw.pyladies.com/">PyLadies Taiwan</a>
    </strong>
  </footer>
</template>

<script>
export default {
  name: "DashFooter",
  data: function() {
    return {
      year: new Date().getFullYear()
    };
  }
};
</script>
