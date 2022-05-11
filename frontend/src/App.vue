<template>
  <div id="app">
    <router-view :key="$route.fullPath"/>
  </div>
</template>


<script>
  import HeaderBar from './components/headerbar.vue';
  export default {
    name: 'App',
    components: [
      HeaderBar
    ],
  }
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  width: 85%;
  margin: 0 auto;
}
</style>
