<template>
  <div class="home">
    <NavBar />
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/NavBar.vue";

export default {
  name: "NavBar",
  components: {
    NavBar,
  },
};
</script>
