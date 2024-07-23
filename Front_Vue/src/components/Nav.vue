<template>
  <div class="nav">
    <div class="nav-menu-wrapper">
      <ul class="menu-list">
        <li v-for="(item, index) in menuList" :key="index" :class="{ activeNav: index == current }"
          @click="changeMenu(index)">
          <div class="block"></div>
          <span class="iconfont" :class="item"></span>
        </li>
      </ul>
    </div>
    <div class="own-pic">
      <HeadPortrait :imgUrl="imgUrl"></HeadPortrait>
    </div>
  </div>
</template>

<script>
import HeadPortrait from "./HeadPortrait.vue";

export default {
  components: {
    HeadPortrait,
  },
  data() {
    return {
      menuList: [
        "icon-xinxi",
        "icon-shipin",
        "icon-gf-telephone",
        "icon-shezhi",
      ],
      current: 0,
      imgUrl: require('@/assets/img/head_portrait.jpg')
    };
  },
  watch:{
    current: {
    // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
    handler(newVal, oldVal) {
      ()=>{console.log(this.current)}
    },
    // deep: true 表示深度监视，可以监视对象内部属性的变化
    deep: true
  },
},
  methods: {
    // 跳转页面
    changeMenu(index) {
      switch (index) {
        case 0:
          if(!document.startViewTransition){
          this.$router.push({
            name: "ChatHome",
            }, () => { });
          }
          document.startViewTransition(()=>{
          this.$router.push({
            name: "ChatHome",
          }, () => { });
          })

          break;
        case 1:
          if(!document.startViewTransition){
          this.$router.push({
            name: "TelPhone",
            }, () => { });
          }
          document.startViewTransition(()=>{
          this.$router.push({
            name: "TelPhone",
          }, () => { });
          })
          break;
        case 2:
          if(!document.startViewTransition){
          this.$router.push({
            name: "VideoPhone",
            }, () => { });
          }
          document.startViewTransition(()=>{
          this.$router.push({
            name: "VideoPhone",
          }, () => { });
          })

          break;
        case 3:
          if(!document.startViewTransition){
          this.$router.push({
            name: "Setting",
            }, () => { });
          }
          document.startViewTransition(()=>{
          this.$router.push({
            name: "Setting",
          }, () => { });
          })
          break;
        default:
          this.$router.push({
            name: "ChatHome",
          });
      }

      this.current = index;
    },
  },
};
</script>

<style lang="scss" scoped>
.nav {
  width: 100%;
  height: 90vh;
  position: relative;
  border-radius: 20px 0 0 20px;
  

  .nav-menu-wrapper {
    position: absolute;
    top: 40%;
    transform: translate(0, -50%);

    .menu-list {
      margin-left: 10px;

      li {
        margin: 40px 0 0 30px;
        list-style: none;
        cursor: pointer;
        position: relative;

        .block {
          background-color: rgb(29, 144, 245);
          position: absolute;
          left: -40px;
          width: 6px;
          height: 30px;
          transition: 0.5s;
          border-top-right-radius: 6px;
          border-bottom-right-radius: 6px;
          opacity: 0;
        }

        &:hover {
          span {
            color: rgb(29, 144, 245);
          }

          .block {
            opacity: 1;
          }
        }
      }
    }
  }

  .own-pic {
    position: absolute;
    bottom: 10%;
    margin-left: 25px;
  }
}

.activeNav {
  span {
    color: rgb(29, 144, 245);
  }

  .block {
    opacity: 1 !important;
  }
}
</style>