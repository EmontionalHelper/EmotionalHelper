<template>
  <div id="app">
    <Home></Home>
  </div>
</template>

<script>
import Home from './view/home.vue'

export default {
  name: 'App',
  components: {
    Home
  }
}
</script>

<style lang="scss">
@import url(./assets/font/iconfont.css);
.iconfont {
  font-family: "iconfont" !important;
  font-style: normal;
  font-size: 25px;
  vertical-align: middle;
  color: rgb(117,120,137);
  transition: .3s;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
* {
  padding: 0;
  margin: 0;
}

#app {
  width: 100vw;
  height: 100vh;
  background:linear-gradient(125deg,#51a6ca,#23e0d4,#8dc731
  ,#58c9ec,#8bdee9,#a9c1d0);
  background-size : 500%;
  animation: beginAnimation 15s linear infinite;
}
@keyframes beginAnimation{
  0%{
      background-position: 0% 50%;
  }
  50%{
    background-position: 50% 100%;
  }
  100%{
    background-position: 0% 50%;
  }
}
</style>