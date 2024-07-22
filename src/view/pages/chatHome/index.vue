<template>
  <div class="chatHome">
    <div class="chatLeft">
      <div class="title">
        <h1>聊天室</h1>
      </div>
      <div class="online-person">
        <span class="onlin-text">好友列表</span>
        <div class="person-cards-wrapper">
          <div class="personList" v-for="personInfo in personList" :key="personInfo.id"
            @click="clickPerson(personInfo)">
            <PersonCard :personInfo="personInfo" :pcCurrent="pcCurrent"></PersonCard>
          </div>
        </div>
      </div>
    </div>
    <div class="chatRight">
      <!-- <router-view></router-view> -->
      <transition name="fade">
        <div v-if="showChatWindow">
          <ChatWindow :childInfo="chatWindowInfo" @personCardSort="personCardSort"></ChatWindow>
        </div>
      <div class="showIcon" v-else>
        <!-- <span class="iconfont icon-snapchat"></span> -->
        <img src="@/assets/img/chat.png" alt="" class="icon-snapchat"/>
      </div>
      </transition>
    </div>
    <!-- <el-col :span="4"><div class="grid-content bg-purple"></div></el-col> -->
  </div>
</template>

<script>
import PersonCard from "@/components/PersonCard.vue";
import ChatWindow from "./chatwindow.vue";

import { getFriend } from "@/api/getData";
export default {
  name: "App",
  components: {
    PersonCard,
    ChatWindow,
  },
  data() {
    return {
      pcCurrent: "",
      personList: [
        {
          img: "",
          name: "陈乐乐",
          detail: "😉 ♀️ 儿子❤️", 
          lastMsg: "",
          id: "1002",
          headImg: require("@/assets/img/head_portrait1.jpg"),

        },
        {
          img: "",
          name: "陈大发",
          detail: "😎 ♂️ 老公❤️",
          lastMsg: "",
          id: "1003",
          headImg: require("@/assets/img/head_portrait2.jpg"),

        },
        {
          img: "",
          name: "王芝兰",
          detail: "😋 ♀️ 朋友",
          lastMsg: "",
          id: "1004",
          headImg: require("@/assets/img/head_portrait3.jpg"),

        },
      ],
      showChatWindow: false,
      chatWindowInfo: {},
    };
  },
  // mounted() {
  //   getFriend().then((res) => {
  //     console.log(res);
  //     this.personList = res;
  //   });
  // },
  methods: {
    clickPerson(info) {
      this.showChatWindow = true;
      this.chatWindowInfo = info;
      this.personInfo = info;
      this.pcCurrent = info.id;
    },
    personCardSort(id) {
      if (id !== this.personList[0].id) {
        console.log(id);
        let nowPersonInfo;
        for (let i = 0; i < this.personList.length; i++) {
          if (this.personList[i].id == id) {
            nowPersonInfo = this.personList[i];
            this.personList.splice(i, 1);
            break;
          }
        }
        this.personList.unshift(nowPersonInfo);
      }
    },
  },
};
</script>

<style lang="scss" scoped>
.chatHome {
  // margin-top: 20px;
  display: flex;
  font-family: Times, "Times New Roman", Georgia, serif;
  font-weight: bolder;

  .chatLeft {
    width: 280px;

    .title {
      color: #fff;
      padding-left: 10px;
    }

    .online-person {
      margin-top: 100px;

      .onlin-text {
        padding-left: 10px;
        color: #fff;
      }

      .person-cards-wrapper {
        padding-left: 10px;
        height: 65vh;
        margin-top: 20px;
        overflow: hidden;
        overflow-y: scroll;
        box-sizing: border-box;

        &::-webkit-scrollbar {
          width: 0;
          /* Safari,Chrome 隐藏滚动条 */
          height: 0;
          /* Safari,Chrome 隐藏滚动条 */
          display: none;
          /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
        }
      }
    }
  }

  .chatRight {
    flex: 1;
    padding-right: 30px;

    .showIcon {
      // position: absolute;
      // top: calc(50% - 150px);
      // /*垂直居中 */
      // left: calc(50% - 50px);
        width:100%;
        height: 100%;
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
      /*水平居中 */
      .icon-snapchat {
        width: 400px;
        height: 400px;
        font-size: 300px;
        // color: rgb(28, 30, 44);
      }
    }
  }
}
</style>