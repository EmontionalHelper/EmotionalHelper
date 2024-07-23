<template>
<div class="chat-window">
    <audio class="audioUrlSave" controls style="display: none;"></audio>
    <div class="top">
        <div class="head-pic">
            <HeadPortrait :imgUrl="childInfo.headImg"></HeadPortrait>
        </div>
        <div class="info-detail">
            <div class="name">{{ childInfo.name }}</div>
            <div class="detail">{{ childInfo.detail }}</div>
        </div>
        <!-- 展示挂件 -->
        <div class="other-fun">
            <label for="docFile">
                <span class="iconfont icon-wenjian"></span>
            </label>
            <label for="imgFile">
                <span class="iconfont icon-tupian"></span>
            </label>
            <input type="file" name="" id="imgFile" @change="sendImg" accept="image/*" />
            <input type="file" name="" id="docFile" @change="sendFile" accept="application/*,text/*" />
            <!-- accept="application/*" -->
        </div>
        <!-- --------------------------- -->

    </div>
    <div class="botoom">

        <!-- 展示聊天记录 -->
        <div class="chat-content" ref="chatContent">
            <!-- <div class="model hidden" ></div> -->
            <div class="overlay hidden">
                <div class="overlay_one ">
                    <img class="voicedisplay" src="@/assets/img/emoji/voice.png" alt="" />
                    <div class="contain">
                        <span class="item "></span>
                        <span class="item "></span>
                        <span class="item "></span>
                        <span class="item "></span>
                        <span class="item "></span>
                        <span class="item "></span>
                        <span class="item "></span>
                    </div>
                </div>
                <div class="overlay_two" style="margin-left: 50px;">
                    <img :src="pause_btn" alt="" @mouseenter="mouseenter" @mouseleave="mouseleave">
                </div>
            </div>
            <div class="chat-wrapper" v-for="item in chatList" :key="item.id">
                <!-- Children聊天记录 -->
                <div class="chat-child" v-if="item.uid !== '1001'">
                    <div class="chat-text" v-if="item.chatType == 0">
                        {{ item.msg }}
                    </div>
                    <div class="chat-img" v-if="item.chatType == 1">
                        <img :src="item.msg" alt="表情" v-if="item.extend.imgType == 1" style="width: 100px; height: 100px" />
                        <el-image :src="item.msg" :preview-src-list="srcImgList" v-else>
                        </el-image>
                    </div>
                    <div class="chat-img" v-if="item.chatType == 2">
                        <div class="word-file">
                            <FileCard :fileType="item.extend.fileType" :file="item.msg"></FileCard>
                        </div>
                    </div>

                    <div class="info-time">
                        <img :src="item.headImg" alt="" />
                        <span>{{ item.name }}</span>
                        <span>{{ item.time }}</span>
                    </div>
                </div>
                <!-- -------------------------------------------- -->
                <!-- Parent聊天记录 -->
                <div class="chat-me" v-else>
                    <div class="chat-text" v-if="item.chatType == 0">
                        {{ item.msg }}
                    </div>
                    <div class="chat-img" v-if="item.chatType == 1">
                        <img :src="item.msg" alt="表情" v-if="item.extend.imgType == 1" style="width: 100px; height: 100px" />
                        <el-image style="max-width: 300px; border-radius: 10px" :src="item.msg" :preview-src-list="srcImgList" v-else>
                        </el-image>
                    </div>
                    <div class="chat-img" v-if="item.chatType == 2">
                        <div class="word-file">
                            <FileCard :fileType="item.extend.fileType" :file="item.msg"></FileCard>
                        </div>
                    </div>
                    <div class="chat-voice" @click="playAudio" v-if="item.chatType == 3">
                        <!-- <img class="voicsState" src="@/assets/img/emoji/voicing.png" style="width: 20px; height: 20px" /> -->
                        <img :src="voiceState" style="width: 25px; height: 25px" />
                        {{voiceTime}}

                    </div>
                    <div class="info-time">
                        <span>{{ item.time }}</span>
                        <span>{{ item.name }}</span>
                        <img :src="item.headImg" alt="" />
                    </div>
                </div>
            </div>
        </div>

        <!-- --------------------------------------------- -->

        <!-- 输入框 -->
        <div class="chatInputs">

            <!--  表情框 -->
            <div class="emoji boxinput" @click="clickEmoji">
                <img src="@/assets/img/emoji/smiling-face.png" alt="" />
            </div>
            <!-- --------------------------------------- -->
            <!-- 表情选择框 -->
            <div class="emoji-content">
                <Emoji v-show="showEmoji" @sendEmoji="sendEmoji" @closeEmoji="clickEmoji"></Emoji>
            </div>
            <!-- -------------------------------- -->
            <!-- 输入框 -->
            <input class="inputs" v-model="inputMsg" @keyup.enter="sendText" />
            <!-- 火箭发射器 -->
            <div class="send boxinput" @click="sendText">
                <img src="@/assets/img/emoji/sendOut.png" alt="" />
            </div>
            <div class="send voice" @click="startAudio">
                <img src="@/assets/img/emoji/voice.png" alt="" />
            </div>
        </div>

    </div>

</div>
</template>

<script>
import {
    animation
} from "@/util/util";
import HeadPortrait from "@/components/HeadPortrait";
import Emoji from "@/components/Emoji";
import FileCard from "@/components/FileCard.vue";
export default {
    components: {
        HeadPortrait,
        Emoji,
        FileCard,
    },
    props: {
        childInfo: Object,
        default () {
            return {};
        },
    },
    watch: {
        childInfo() {
            this.getChildChatMsg();
        },
        isReply: {
            // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
            handler(newVal, oldVal) {
                this.ChangeChatList();
            },
            // deep: true 表示深度监视，可以监视对象内部属性的变化
            deep: true
        },
        waveflag: {
            // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
            handler(newVal, oldVal) {
                this.ChangeAnimation();
            },
            // deep: true 表示深度监视，可以监视对象内部属性的变化
            deep: true
        }
    },
    data() {
        return {
            chatList: [],
            inputMsg: "",
            showEmoji: false,
            friendInfo: {},
            srcImgList: [],
            isReply: false,
            time: "09:12 AM",
            voiceTime: '2"',
            buffer: [],
            voicetimes: 0,
            Readingvoicetimes: 0,
            recordedChunks: [],
            waveflag: false,
            pause_btn: require("@/assets/img/pause.png"),
            voiceState: require("@/assets/img/Addvoice.png"),
            FirstChildChat: [{
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: "昨天 09：12 AM",
                    msg: " 乐乐，你今天上班吗？",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1001", //uid
                },

                {
                    headImg: require("@/assets/img/head_portrait1.jpg"),
                    name: "陈乐乐",
                    time: "昨天 09：12 AM",
                    msg: " 妈，我今天上班呢，不过还好不算太忙。您和爸今天身体咋样？记得按时吃药哈。",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1002", //uid
                },
                {
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: "昨天 09：12 AM",
                    msg: "我和你爸那里都好，照顾好你自己就好了",
                    chatType: 0, ////信息类型，0文字，1图片, 2文件，3语音
                    uid: "1001",
                },
                {
                    headImg: require("@/assets/img/head_portrait1.jpg"),
                    name: "陈乐乐",
                    time: "昨天 09：12 AM",
                    msg: "好的，妈😉",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1002", //uid
                },
            ],
            SecondChildChat: [{
                    headImg: require("@/assets/img/head_portrait2.jpg"),
                    name: "陈大发",
                    time: "昨天 10：34 AM",
                    msg: "老婆，今天晚上买啥菜啊？",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1002", //uid
                },
                {
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: "昨天 10：34 AM",
                    msg: "今天儿子回来，给他买了排骨，做他最爱吃的糖醋排骨",
                    chatType: 0, ////信息类型，0文字，1图片, 2文件，3语音
                    uid: "1001",
                },
                {
                    headImg: require("@/assets/img/head_portrait2.jpg"),
                    name: "陈大发",
                    time: "昨天 10：34 AM",
                    msg: "哈哈哈，今天有口福了",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1002", //uid
                },
            ],
            ThirdChildChat: [{
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: "昨天 18：06 PM",
                    msg: "芝兰，今天还跳舞吗？",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1001", //uid
                },
                {
                    headImg: require("@/assets/img/head_portrait3.jpg"),
                    name: "王芝兰",
                    time: "昨天 18：06 PM",
                    msg: "今天先不了，女儿和女婿回来了😊，我要给他们做点好吃的",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1002", //uid
                },
                {
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: "昨天 18：06 PM",
                    msg: "哈哈，好羡慕你家呀，我们家乐乐还没找到对象",
                    chatType: 0, ////信息类型，0文字，1图片, 2文件，3语音
                    uid: "1001",
                },
                {
                    headImg: require("@/assets/img/head_portrait3.jpg"),
                    name: "王芝兰",
                    time: "昨天 18：06 PM",
                    msg: "没事儿，乐乐挺优秀一孩子，不愁找不到对象",
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1002", //uid
                },
                {
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: "昨天 18：06 PM",
                    msg: "哎，但愿吧",
                    chatType: 0, ////信息类型，0文字，1图片, 2文件，3语音
                    uid: "1001",
                },
            ],
        };
    },
    // 挂载聊天记录
    mounted() {
        this.getChildChatMsg();
    },
    methods: {
        // 聊天回应
        ChangeChatList() {
            //获取与该Child聊天中的最新回应
            let imgNum = String(Number(this.childInfo.id) - 1001);
            let query, chatHistory;
            if (imgNum == "1") {
                chatHistory = this.FirstChildChat;
                query = this.FirstChildChat.slice(-1);
            } else if (imgNum == "2") {
                chatHistory = this.SecondChildChat;
                query = this.SecondChildChat.slice(-1);;
            } else if (imgNum == "3") {
                chatHistory = this.ThirdChildChat;
                query = this.ThirdChildChat.slice(-1);;
            }
            //按照格式规定chatHistory
            let chat_histories = [];
            chatHistory.forEach(
                chat => {
                    let chat_history = {
                        "role": (chat["uid"] == "1001" ? "user" : "assistant"),
                        "type": (chat["uid"] == "1001" ? "query" : "answer"),
                        "content": chat["msg"],
                        "content_type": (chat["chatType"] == 0 ? "text" : "img"),
                    }
                    chat_histories.push(chat_history);
                }
            )
            //-----------------------
            //获得聊天的相关信息，比如时间，child's name, child's id
            this.gettime();
            let childName = this.childInfo.name;
            let NowTime = this.time;
            let friendId = this.childInfo.id;
            // ----------------------------------------------------------
            //形成向cozeAPI提问的标准形式
            let data = {
                "conversation_id": "123",
                "bot_id": "7391681464909266953",
                "user": "CustomizedString123",
                "query": `${query["0"]["msg"]}`,
                "stream": false,
                "chat_history": chat_histories,
            }
            //向cozeAPI提问
            let that = this;
            async function getData(data) {
                let respose = await fetch('https://api.coze.cn/open_api/v2/chat', {
                    method: "POST",
                    mode: "cors",
                    // credentials: "include",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": "你在coze中的身份令牌",
                        "Accept": "*/*",
                        "Host": "api.coze.cn",
                        "Connection": "keep-alive",
                    },
                    body: JSON.stringify(data),
                });
                //获得回应，并开始提取回答
                let json = await respose.json();
                console.log(json);
                let i;
                for (i = 0; i < json["messages"].length; i++) {
                    if (json["messages"][i]["type"] == "answer" && json["messages"][i]["content_type"] == "text")
                        break;
                }
                let answer = await json["messages"][i]["content"];
                //将回答包装并发送出去
                let chatMsg = {
                    headImg: require(`@/assets/img/head_portrait${imgNum}.jpg`),
                    name: childName,
                    time: NowTime,
                    msg: answer,
                    chatType: 0, //信息类型，0文字，1图片
                    uid: friendId, //uid
                };
                that.sendMsg(chatMsg);
            }
            getData(data);
        },
        // -------------------------------------------------------------

        // //分析音频数据
        // analyseAudio(audioContext,microphone){
        //     // 创建一个analyser来分析音频数据
        //     const analyser = audioContext.createAnalyser();
        //     analyser.fftSize = 512;
        //     //接收分析器结点的分析数据
        //     let dataArray = new Uint8Array(analyser.frequencyBinCount);
        //     microphone.connect(analyser);
        //     // analyser.connect(audioContext.destination);
        // },  
        
        //文字转语音(录音开始)
        startAudio() {
            this.$message("录音开始~🥳");
            document.querySelector('.overlay').classList.remove('hidden');
            //------------------------------------------      
            navigator.mediaDevices.getUserMedia({
                audio: true
            }).then((stream) => {
                let track = stream.getAudioTracks()[0];
                console.log(track.getCapabilities());
                const audioContext = new(window.AudioContext || window.wekitAudioContext)();
                // 将麦克风输入连接到音频上下文
                const microphone = audioContext.createMediaStreamSource(stream);
                // 创建一个ScriptProcessorNode来处理音频数据    
                const scriptNode = audioContext.createScriptProcessor(4096, 1, 1);          
                //监听ScriptProcessorNode来处理音频数据
                let timer, sum = 0.0,len;
                console.log("this.recordedChunks's length",this.recordedChunks.length);
                scriptNode.onaudioprocess = (event) => {
                    // 获取PCM数据
                    const inputBuffer = event.inputBuffer;
                    const pcmData = inputBuffer.getChannelData(0); // 获取单个声道的PCM数据
                    len = pcmData.length;
                    // 存储PCM数据块
                    let data = this.interpolateArray(new Float32Array(pcmData), 16000, audioContext.sampleRate)
                    console.log("recordedChunks's length:",this.recordedChunks.length);
                    this.recordedChunks.push(data);
                    for (let i = 0; i < pcmData.length; i += 1) {
                        sum += pcmData[i] * pcmData[i];
                    }
                    //recordedChunks.push(new Float32Array(pcmData))
                };
                let that = this;
                timer = setInterval(() => {
                    const volume = Math.round(Math.sqrt(sum / len) * 100);
                    sum = 0.0;
                    console.log(`volume: ${volume}`);
                    if (volume < 7) {
                        this.waveflag = false;
                    } else {
                        console.log("yeah!!!");
                        this.waveflag = true;
                        console.log(this.waveflag);
                    }
                }, 1000);
                // 连接音频节点
                microphone.connect(scriptNode);
                scriptNode.connect(audioContext.destination);

                document.querySelector('.overlay_two').onclick = (audioContext, stream) => {
                    that.stopAudio(stream,scriptNode,timer);
                }
            }).catch((err) => {
                console.error('获取麦克风权限失败：', err);
            });
        },
        // 录音结束
        stopAudio(stream,scriptNode,timer) {
            console.log('停止录制');
            clearInterval(timer);
            document.querySelector('.overlay').classList.add('hidden');
            // 停止MediaStream轨道
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => {
                    track.stop();
                });
            }
            //断开连接
            scriptNode.disconnect();
            // console.log("recordedChunks's length:",this.recordedChunks.length);
            let pcmData = this.flattenArray(this.recordedChunks);
            // 创建WAV文件头
            const wavHeader = this.createWavHeader(pcmData.byteLength, 16000);

            // 合并WAV文件头和PCM数据
            const wavBlob = new Blob([wavHeader, pcmData], {
                type: 'audio/wav'
            });
            //const wavBlob = new Blob([pcmData], { type: 'audio/pcm' });
            let audiourl = URL.createObjectURL(wavBlob);
            document.querySelector(".audioUrlSave").src = audiourl;
            //创建文件并发送
            let formData = new FormData();
            formData.append('file', wavBlob, 'output.wav');
            let that = this;
            fetch('http://127.0.0.1:5000', {
                    method: "POST",
                    body: formData,
                }).then(respose => {
                    return respose.json();
                }).then(data => {
                    that.sendVoiceMsg(data.result);
                    console.log(data.result);
                })
                .catch(err => {
                    console.log("appear lose", err);
                })
            this.recordedChunks = [];
        },
        // 动画变化
        //------------------------------------------------------------------
        ChangeAnimation(){
            const elements = document.querySelectorAll('.item');
            for(let i = 0; i<elements.length ; i++){
                document.startViewTransition(()=>{
                elements[i].classList.toggle("waveChange");
                })
            }
        },
        mouseenter(){
            this.pause_btn = require("@/assets/img/pause1.png");
        },
        mouseleave(){
            this.pause_btn = require("@/assets/img/pause.png");
        },
        //------------------------------------------------------------------
        //关闭录音
        sendVoiceMsg(result) {
            console.log("sendResult:", result);
            this.gettime();
            let chatMsg = {
                headImg: require("@/assets/img/head_portrait.jpg"),
                name: "聂小春",
                time: this.time,
                msg: result,
                chatType: 3, //信息类型，0文字，1图片
                extend: {
                    imgType: 1, //(1表情，2本地图片)
                },
                uid: "1001",
            };
            this.sendMsg(chatMsg);
            this.isReply = !this.isReply;
        },
        // 播放录音
        playAudio(e) {
            
            let event = e.target;
            let newAudio;
            if (!event.classList.contains('chat-voice'))
                event = event.parentNode;
            if (event.querySelectorAll('audio').length == 0) {
                console.log("To Create audio");
                let audioUrlSave = document.querySelector('.audioUrlSave');
                let audioURL = audioUrlSave.src;
                newAudio = document.createElement('audio');
                newAudio.style.display = "none";
                newAudio.controls = true;
                newAudio.src = audioURL;
                event.appendChild(newAudio);
            } else {
                newAudio = event.querySelector('audio');
                console.log(newAudio);
            }

            if (newAudio.paused || newAudio.ended) {
                newAudio.play();
            } else {
                newAudio.stop();
            }

            newAudio.onplaying = () => {
                event.style.backgroundColor = "green";
                this.voiceState = require("@/assets/img/Addvoice.gif");
            }
            newAudio.onended = () => {
                event.style.backgroundColor = "rgb(29, 144, 245)";
                this.voiceState = require("@/assets/img/Addvoice.png");
            }
            this.$message("录音结束……");
        },
        //-------------------------------------------------------

        //-------------------------------------------------------
        getChildChatMsg() {
            let params = {
                frinedId: this.childInfo.id,
            };
            if (this.childInfo.id == "1002") {
                this.chatList = this.FirstChildChat;
            } else if (this.childInfo.id == "1003") {
                this.chatList = this.SecondChildChat;
            } else if (this.childInfo.id == "1004") {
                this.chatList = this.ThirdChildChat;
            }

        },

        //获得时间
        gettime() {
            let time = new Date(Date.now());
            let hour = time.getHours() >= 10 ? String(time.getHours()) : ('0' + time.getHours());
            let minute = time.getMinutes() >= 10 ? String(time.getMinutes()) : ('0' + time.getMinutes());
            this.time = hour + "：" + minute + (time.getHours() >= 12 ? ' PM' : ' AM');
        },
        //发送信息
        sendMsg(msgList) {
            if (this.childInfo.id == "1002") {
                this.FirstChildChat.push(msgList);
            } else if (this.childInfo.id == "1003") {
                this.SecondChildChat.push(msgList);
            } else if (this.childInfo.id == "1004") {
                this.ThirdChildChat.push(msgList);
            }
            this.scrollBottom();
        },
        //获取窗口高度并滚动至最底层
        scrollBottom() {
            this.$nextTick(() => {
                const scrollDom = this.$refs.chatContent;
                animation(scrollDom, scrollDom.scrollHeight - scrollDom.offsetHeight);
            });
        },
        //关闭标签框
        clickEmoji() {
            this.showEmoji = !this.showEmoji;
        },
        //发送文字信息
        sendText() {
            if (this.inputMsg) {
                this.gettime();
                let chatMsg = {
                    headImg: require("@/assets/img/head_portrait.jpg"),
                    name: "聂小春",
                    time: this.time,
                    msg: this.inputMsg,
                    chatType: 0, //信息类型，0文字，1图片
                    uid: "1001", //uid
                };
                this.sendMsg(chatMsg);
                this.$emit('personCardSort', this.childInfo.id)
                this.inputMsg = "";
                this.isReply = !this.isReply;
            } else {
                this.$message({
                    message: "消息不能为空哦~",
                    type: "warning",
                });
            }
        },
        //发送表情
        sendEmoji(msg) {
            this.gettime();
            let chatMsg = {
                headImg: require("@/assets/img/head_portrait.jpg"),
                name: "聂小春",
                time: this.time,
                msg: msg,
                chatType: 1, //信息类型，0文字，1图片
                extend: {
                    imgType: 1, //(1表情，2本地图片)
                },
                uid: "1001",
            };
            this.sendMsg(chatMsg);
            this.clickEmoji();
            this.isReply = !this.isReply;
        },
        //发送本地图片
        sendImg(e) {
            this.gettime();
            let _this = this;
            console.log(e.target.files);
            let chatMsg = {
                headImg: require("@/assets/img/head_portrait.jpg"),
                name: "聂小春",
                time: this.time,
                msg: "",
                chatType: 1, ////信息类型，0文字，1图片, 2文件，3语音
                extend: {
                    imgType: 2, //(1表情，2本地图片)
                },
                uid: "1001",
            };
            let files = e.target.files[0]; //图片文件名
            if (!e || !window.FileReader) return; // 看是否支持FileReader
            let reader = new FileReader();
            reader.readAsDataURL(files); // 关键一步，在这里转换的
            reader.onloadend = function () {
                chatMsg.msg = this.result; //赋值
                _this.srcImgList.push(chatMsg.msg);
            };
            this.sendMsg(chatMsg);
            this.isReply = !this.isReply;
            e.target.files = null;
        },
        //发送文件
        sendFile(e) {
            this.gettime();
            let chatMsg = {
                headImg: require("@/assets/img/head_portrait.jpg"),
                name: "聂小春",
                time: this.time,
                msg: "",
                chatType: 2, //信息类型，0文字，1图片, 2文件，3语音
                extend: {
                    fileType: "", //(1word，2excel，3ppt，4pdf，5zpi, 6txt)
                },
                uid: "1001",
            };
            let files = e.target.files[0]; //图片文件名
            chatMsg.msg = files;
            console.log(files);
            if (files) {
                switch (files.type) {
                    case "application/msword":
                    case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                        chatMsg.extend.fileType = 1;
                        break;
                    case "application/vnd.ms-excel":
                    case "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
                        chatMsg.extend.fileType = 2;
                        break;
                    case "application/vnd.ms-powerpoint":
                    case "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                        chatMsg.extend.fileType = 3;
                        break;
                    case "application/pdf":
                        chatMsg.extend.fileType = 4;
                        break;
                    case "application/zip":
                    case "application/x-zip-compressed":
                        chatMsg.extend.fileType = 5;
                        break;
                    case "text/plain":
                        chatMsg.extend.fileType = 6;
                        break;
                    default:
                        chatMsg.extend.fileType = 0;
                }
                this.sendMsg(chatMsg);
                this.isReply = !this.isReply;
                e.target.files = null;
            }
        },
        //-----------------------------------------------------------------
        // for changing the sampling rate, data,
        interpolateArray(data, newSampleRate, oldSampleRate) {
            var fitCount = Math.round(data.length * (newSampleRate / oldSampleRate));
            var newData = new Array();
            var springFactor = new Number((data.length - 1) / (fitCount - 1));
            newData[0] = data[0]; // for new allocation
            for (var i = 1; i < fitCount - 1; i++) {
                var tmp = i * springFactor;
                var before = new Number(Math.floor(tmp)).toFixed();
                var after = new Number(Math.ceil(tmp)).toFixed();
                var atPoint = tmp - before;
                newData[i] = this.linearInterpolate(data[before], data[after], atPoint);
            }
            newData[fitCount - 1] = data[data.length - 1]; // for new allocation
            return newData;
        },
        linearInterpolate(before, after, atPoint) {
            return before + (after - before) * atPoint;
        },
        // 辅助函数：将二维数组扁平化为一维数组
        flattenArray(arrays, sampleRate) {
            const buffer = new ArrayBuffer(arrays.length * 4096 * 2);
            const view = new DataView(buffer);
            let offset = 0

            for (var i = 0; i < arrays.length; i++) {
                for (var j = 0; j < arrays[i].length; j++) {
                    let data = parseInt(arrays[i][j] * 32768)
                    view.setUint16(offset, data, true);
                    offset += 2
                }
            }
            return buffer.slice(0, offset)
        },
        // 辅助函数：创建WAV文件头
        createWavHeader(dataSize, sampleRate) {
            const buffer = new ArrayBuffer(44);
            const view = new DataView(buffer);

            // Chunk ID
            view.setUint32(0, 0x52494646, false); // "RIFF"

            // File size (excluding first 8 bytes)
            console.log(dataSize)
            view.setUint32(4, dataSize + 36, true);

            // Format (WAVE)
            view.setUint32(8, 0x57415645, false); // "WAVE"

            // Subchunk 1 ID (fmt)
            view.setUint32(12, 0x666D7420, false); // "fmt "

            // Subchunk 1 size
            view.setUint32(16, 16, true);

            // Audio format (PCM)
            view.setUint16(20, 1, true);

            // Number of channels (1 for mono)
            view.setUint16(22, 1, true);

            // Sample rate
            view.setUint32(24, sampleRate, true);

            // Byte rate (sample rate * block align)
            view.setUint32(28, sampleRate * 2, true);

            // Block align (number of bytes per sample)
            view.setUint16(32, 2, true);

            // Bits per sample
            view.setUint16(34, 16, true);

            // Subchunk 2 ID (data)
            view.setUint32(36, 0x64617461, false); // "data"

            // Subchunk 2 size
            view.setUint32(40, dataSize, true);

            return buffer;
        },
    },
};
</script>

<style lang="scss" scoped>
.chat-window {
    width: 100%;
    height: 100%;
    margin-left: 20px;
    position: relative;
    font-family: Times, "Times New Roman", Georgia, serif;

    .top {
        margin-bottom: 50px;

        &::after {
            content: "";
            display: block;
            clear: both;
        }

        .head-pic {
            float: left;
        }

        .info-detail {
            float: left;
            margin: 5px 20px 0;

            .name {
                font-size: 20px;
                font-weight: 600;
                color: #fff;
            }

            .detail {
                color: #9e9e9e;
                font-size: 14px;
                margin-top: 2px;
            }
        }

        .other-fun {
            float: right;
            margin-top: 20px;

            span {
                margin-left: 40px;
                font-size: 35px;
                cursor: pointer;

                &:hover {
                    color: rgb(29, 144, 245);
                }
            }

            // .icon-tupian {

            // }
            input {
                display: none;
            }
        }
    }

    .botoom {
        width: 100%;
        height: 70vh;
        overflow: auto;
        // background-color: rgb(50, 54, 68);
        background: rgba(255, 255, 255, 0.2);
        // border-radius: 15px;
        box-shadow: 0 5px 35px rgba(0, 0, 0, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-sizing: border-box;
        position: relative;
        font-weight: bolder;

        .chat-content {
            width: 100%;
            height: 85%;
            overflow-y: scroll;
            padding: 20px;
            box-sizing: border-box;

            &::-webkit-scrollbar {
                width: 0;
                /* Safari,Chrome 隐藏滚动条 */
                height: 0;
                /* Safari,Chrome 隐藏滚动条 */
                display: none;
                /* 移动端、pad 上Safari，Chrome，隐藏滚动条 */
            }

            .chat-wrapper {
                position: relative;
                word-break: break-all;

                .chat-child {
                    width: 100%;
                    float: left;
                    margin-bottom: 20px;
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-start;
                    align-items: flex-start;

                    .chat-text {
                        max-width: 90%;
                        padding: 20px;
                        border-radius: 20px 20px 20px 5px;
                        background-color: rgba(255, 255, 255, 0.4);
                        color: #000000;

                        &:hover {
                            background-color: rgb(97, 240, 159);
                        }
                    }

                    .chat-img {
                        img {
                            width: 100px;
                            height: 100px;
                        }
                    }

                    .info-time {
                        margin: 10px 0;
                        color: #fff;
                        font-size: 14px;

                        img {
                            width: 30px;
                            height: 30px;
                            border-radius: 50%;
                            vertical-align: middle;
                            margin-right: 10px;
                        }

                        span:last-child {
                            color: rgb(101, 104, 115);
                            margin-left: 10px;
                            vertical-align: middle;
                        }
                    }
                }

                .chat-me {
                    width: 100%;
                    float: right;
                    margin-bottom: 20px;
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    justify-content: flex-end;
                    align-items: flex-end;

                    .chat-text {
                        float: right;
                        max-width: 90%;
                        padding: 20px;
                        border-radius: 20px 20px 5px 20px;
                        background-color: rgb(29, 144, 245);
                        color: #fff;

                        &:hover {
                            background-color: rgb(26, 129, 219);
                        }
                    }

                    .chat-img {
                        img {
                            max-width: 300px;
                            max-height: 200px;
                            border-radius: 10px;

                        }
                    }

                    .chat-voice {
                        float: right;
                        max-width: 90%;
                        padding: 20px;
                        border-radius: 20px 20px 5px 20px;
                        background-color: rgb(29, 144, 245);
                        display: flex;
                        flex-direction: row;
                        justify-content: center;
                        align-items: center;

                        img {
                            margin-right: 5px;
                        }
                    }

                    .info-time {
                        margin: 10px 0;
                        color: #fff;
                        font-size: 14px;
                        display: flex;
                        justify-content: flex-end;

                        img {
                            width: 30px;
                            height: 30px;
                            border-radius: 50%;
                            vertical-align: middle;
                            margin-left: 10px;
                        }

                        span {
                            line-height: 30px;
                        }

                        span:first-child {
                            color: rgb(101, 104, 115);
                            margin-right: 10px;
                            vertical-align: middle;
                        }
                    }
                }
            }
        }

        .chatInputs {
            width: 90%;
            position: absolute;
            bottom: 0;
            margin: 3%;
            display: flex;

            .boxinput {
                width: 50px;
                height: 50px;
                background-color: rgb(66, 70, 86);
                border-radius: 15px;
                border: 1px solid rgb(80, 85, 103);
                position: relative;
                cursor: pointer;

                img {
                    width: 30px;
                    height: 30px;
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                }
            }

            .voice {
                width: 50px;
                height: 50px;
                background-color: rgb(66, 70, 86);
                border-radius: 15px;
                border: 1px solid rgb(80, 85, 103);
                position: relative;
                cursor: pointer;
                margin-left: 20px;

                img {
                    width: 30px;
                    height: 30px;
                    position: absolute;
                    left: 50%;
                    top: 50%;
                    transform: translate(-50%, -50%);
                }
            }

            .emoji {
                transition: 0.3s;

                &:hover {
                    background-color: rgb(46, 49, 61);
                    border: 1px solid rgb(71, 73, 82);
                }
            }

            .inputs {
                width: 90%;
                height: 50px;
                background-color: rgb(66, 70, 86);
                border-radius: 15px;
                border: 2px solid rgb(34, 135, 225);
                padding: 10px;
                box-sizing: border-box;
                transition: 0.2s;
                font-size: 20px;
                color: #fff;
                font-weight: 100;
                margin: 0 20px;

                &:focus {
                    outline: none;
                }
            }

            .send {
                background-color: rgb(29, 144, 245);
                border: 0;
                transition: 0.3s;
                box-shadow: 0px 0px 5px 0px rgba(0, 136, 255);

                &:hover {
                    box-shadow: 0px 0px 10px 0px rgba(0, 136, 255);
                }
            }
        }
    }

    // .modal{
    //   position: absolute;
    //   top: 50%;
    //   left: 50%;
    //   transform: translate(-50%, -50%);
    //   max-width: 60rem;
    //   background-color: #f3f3f3;
    //   padding: 5rem 6rem;
    //   box-shadow: 0 4rem 6rem rgba(0, 0, 0, 0.3);
    //   z-index: 1000;
    //   transition: all 0.5s;
    // }
    .overlay {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 60vw;
        /* 元素宽度 */
        height: 65vh;
        /* 元素高度 */
        border-radius: 20px;
        box-sizing: border-box;
        background-color: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(4px);
        z-index: 100;
        transition: all 0.5s;

        .overlay_one {
            width: 100%;
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
        }
        .overlay_two {
            img {
                width: 150px;
                height: 150px;
            }
        }
    }

    .hidden {
        display: none;
    }
    .contain {
        display: flex;
        flex-direction: row;
        justify-content: center;
        align-items: center;
        width: 40%;
        height: 100%;
    }
    .item {
        width: 16px;
        height: 80px;
        margin: 20px;
        background-color: white;
        border-radius: 4px;
        transition: all 1s ease-out; /* 所有属性在0.5秒内过渡 */
    }
    .waveChange {
        animation: wave 2s ease-in-out infinite;
    }
    @keyframes wave {
        20% {
            transform:scale(1.5);
        }
        50% {
            transform:scale(1);
        }
        80% {
            transform:scale(0.7);
        }
    }
    .contain .item:nth-child(1){
        animation-delay:0s;
    }
    .contain .item:nth-child(2){
        animation-delay:0.2s;
    }
    .contain .item:nth-child(3){
        animation-delay:0.4s;
    }
    .contain .item:nth-child(4){
        animation-delay:0.6s;
    }
    .contain .item:nth-child(5){
        animation-delay:0.8s;
    }
    .contain .item:nth-child(6){
        animation-delay:1s;
    }
    .contain .item:nth-child(7){
        animation-delay:1.2s;
    }
}
</style>
