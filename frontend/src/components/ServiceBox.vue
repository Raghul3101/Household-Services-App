<template>
  <div class="service-box" @click="selectCategory">
    {{ category }}
  </div>
</template>

<script>
export default {
  props: ["category"],
  methods: {
    selectCategory() {
      this.$emit("selectCategory", this.category);
    },
  },
};
</script>

<style scoped>
.service-box {
  width: 150px !important;
  height: 150px !important;
  min-width: 150px !important;
  min-height: 150px !important;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid rgb(30, 30, 30);
  border-radius: 23px;
  margin: 15px;
  font-size: 18px;
  color: whitesmoke;
  cursor: pointer;
  transition: all 0.3s ease;
}

.service-box:hover {
  background-color: #f0f0f0;
  transform: scale(1.05);
  color: rgb(30, 30, 30);
  border-color: white;
}
</style>
