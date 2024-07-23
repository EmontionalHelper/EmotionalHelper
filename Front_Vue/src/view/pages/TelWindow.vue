<template>
<div class="chat-window">
    <div class="top">
        <div class="head-pic">
            <HeadPortrait :imgUrl="frinedinfo.headImg"></HeadPortrait>
        </div>
        <div class="info-detail">
            <div class="name">{{ frinedinfo.name }}</div>
            <div class="detail">{{ frinedinfo.detail }}</div>
        </div>
    </div>
    <div class="bottom ">
        <audio controls style="display: none;" class="audioPlayer" autoplay></audio> 
        <div class="bottom_before ">
            <div class="bottom_zero ">
                <div class="Connecting" alt="">
                    <img src="@/assets/img/TelOn.png">
                    正在接通中……
                </div>
            </div>
            <div class="bottom_portrait">
                <div class="portrait">
                    <img src="@/assets/img/head_portrait.jpg" alt="">
                </div>
                <div class="containers">
                    <div class="point"></div>
                    <div class="point"></div>
                    <div class="point"></div>
                    <div class="point"></div>
                    <div class="point"></div>
                </div>
                <div class="portrait">
                    <img :src="frinedinfo.headImg" alt="">
                </div>
            </div>
        </div>
        <div class="bottom_later hidden">
            <div class="videochat">
                <video id="videoElement" style="width: 40%; border-radius: 20px;" class="hidden"></video>
                <img src="@/assets/img/wait.gif" style="width: 150px; height: 150px;" class="wait"/>
                <div class="gif"  style="width: 40%; height: 282px;"  @click="changGif">
                    <img :src="videoGif" style="width: 135%; height: 100%;"/>
                </div>
            </div>
            <div class="turnoff" alt="" @click="TelDown">
                <img src="@/assets/img/turnoff.png">
            </div>
        </div>
        <div class="bottom_end hidden" style="width: 100%; height: 100%;">
            <img src="@/assets/img/exit.gif" style="width: 100%; height: 100%; border-radius: 20px;"/>
        </div>

    </div>
</div>
</template>

<script>
import HeadPortrait from "@/components/HeadPortrait";
import flvjs from "flv.js";
export default {
    components: {
        HeadPortrait
    },
    props: {
        frinedinfo: Object,
        default () {
            return {};
        },
    },
    data() {
        return {
            videoGif: require('@/assets/img/happy.png'),
            Content: "妈，怎么啦？",
            recordedChunks: [],
            overVolume: 0,
            stream: '',
            scriptNode: '',
            isInit: false,
            isParent: true,
            flvPlay:'',
            VolumeTimer:'',
            Pemotion:'',
            EmotionInterval: '',
            chat_histories: [{
                id: 1002,
                msg: "妈，怎么啦？",
            }, ]
        };
    },
    mounted() {
        //开摄像头
        // this.started();
        this.TelGet();
        this.TimeToGetEmotion();
        this.AudioToPlay();
    },
    watch: {
        Content: {
            // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
            handler(newVal, oldVal) {
                this.TelGet();
            },
            // deep: true 表示深度监视，可以监视对象内部属性的变化
            deep: true
        },
        Pemotion: {
            // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
            handler(newVal, oldVal) {
                this.changGif();
            },
            // deep: true 表示深度监视，可以监视对象内部属性的变化
            deep: true
        },
        isParent: {
            // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
            handler(newVal, oldVal) {
                this.changPng();
            },
            // deep: true 表示深度监视，可以监视对象内部属性的变化
            deep: true
        }
    },
    methods: {
        changPng(){
            if(this.isParent){
                let emotion = this.Pemotion;
                document.startViewTransition(() => {
                    if(emotion == "happy"||emotion == "surprised"||emotion == "neutral"){
                        console.log("ChangePng: happy.png");
                        this.videoGif = require('@/assets/img/happy.png');
                    }
                    else {
                        console.log("ChangePng: happy.png");
                        this.videoGif = require('@/assets/img/normal.png');
                    }
                        
                })
            }else{
                this.changGif();
            }
        },
        TimeToGetEmotion(){
            this.EmotionInterval = setInterval(this.GetEmotion,1000);
        },
        AudioToPlay(){
            document.querySelector('.audioPlayer').addEventListener('canplay',() => {
                console.log("Audio is Ready to play");
                this.isParent = false;
            })
        },
        GetEmotion(){
            fetch('http://127.0.0.1:5000/Emotion')
            .then((respose) => {
                return respose.json();
            }).then((res) => {
                this.Pemotion = res["Result"]["items"][0]["value"];
                console.log(this.Pemotion);
            })
            .catch((err) => {
                console.log(err)
            });
        },
        started(){
            if (flvjs.isSupported()) {
            var videoElement = document.getElementById('videoElement');
            var flvPlayer = flvjs.createPlayer({
                type: 'flv',
                url: 'https://vei-video-sh.byte-edge.com/edge-video/device-usb-camera/first_camera.live.flv?hostheader=http-sxn009-ai8e5c-vei-media-server-80',
                isLive: true,
            });
            flvPlayer.attachMediaElement(videoElement);
            this.flvPlay = flvPlayer;
            flvPlayer.load();
            flvPlayer.play();
            this.Connect_phone();
    }
        },
        changGif() {
            console.log("Change Emotion!!")
            let emotion = this.Pemotion;
            document.startViewTransition(() => {
                if(!this.isParent){
                    if(emotion == "happy"||emotion == "surprised")
                        this.videoGif = require('@/assets/img/happy surprised.gif');
                    else if(emotion == "angry")
                        this.videoGif = require('@/assets/img/angry.gif');
                    else if(emotion == "neutral")
                        this.videoGif = require('@/assets/img/neutral.gif');
                    else 
                        this.videoGif = require('@/assets/img/sad disgustesd fearful.gif');
                    console.log("this.videoGif",this.videoGif);
                }
            })
        },
        //接通电话动画
        Connect_phone() {
                //添加动画
                setTimeout(()=>{
                    document.startViewTransition(() => {
                    //交换隐藏特性
                    document.querySelector('.bottom_before').classList.toggle('hidden');
                    document.querySelector('.bottom_later').classList.toggle('hidden');
                    setTimeout(() => {
                        document.querySelector('#videoElement').classList.toggle('hidden');
                        document.querySelector('.wait').classList.add('hidden');
                    },500)
                })
                },500);
            //先打招呼
        },
        //----------------------------------------------------------
        //接听语音(录音开始)
        startAudio() {
            console.log("录音开始");
            this.isOver = false;
            const audioContext = new(window.AudioContext || window.wekitAudioContext)();
            let that = this;
            navigator.mediaDevices.getUserMedia({
                audio: true
            }).then((mediaStream) => {
                const mediaStreamSource = audioContext.createMediaStreamSource(mediaStream);
                const scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
                this.scriptNode = scriptProcessor;
                let input, sum = 0.0;
                scriptProcessor.onaudioprocess = (event) => {
                    //获取PCM数据
                    input = event.inputBuffer.getChannelData(0); //获得单声道的PCM数据
                    //存储PCM数据块
                    let data = this.interpolateArray(new Float32Array(input), 16000, audioContext.sampleRate);
                    console.log("recordedChunks's length:",this.recordedChunks.length);
                    this.recordedChunks.push(data);
                    for (let i = 0; i < input.length; i += 1) {
                        sum += input[i] * input[i];
                    }
                }
                let belowTimes = 0;
                this.VolumeTimer = setInterval(() => {
                    const volume = Math.round(Math.sqrt(sum / input.length) * 100);
                    sum = 0.0;
                    console.log(`volume: ${volume}`);
                    if (volume < 7) {
                        belowTimes++;
                        console.log(`Times:${belowTimes}`);
                    } else {
                        belowTimes = 0;
                    }
                    if (belowTimes >= 3) {
                        console.log("BLOOM!!!! STOP");
                        scriptProcessor.disconnect();
                        this.stopAudio();
                        clearInterval(this.VolumeTimer);
                    }
                }, 1000);
                scriptProcessor.connect(audioContext.destination);
                mediaStreamSource.connect(scriptProcessor);
            })

        },
        // 录音结束(将问题转为文字)
        stopAudio(stream) {
            console.log('停止录制');
            
            // 停止MediaStream轨道
            if (stream) {
                const tracks = stream.getTracks();
                tracks.forEach(track => {
                    track.stop();
                });
            }
            if (!this.isOver) {
                console.log("recordedChunks's length:",this.recordedChunks.length);
                let pcmData = this.flattenArray(this.recordedChunks);
                // 创建WAV文件头
                const wavHeader = this.createWavHeader(pcmData.byteLength, 16000);

                // 合并WAV文件头和PCM数据
                const wavBlob = new Blob([wavHeader, pcmData], {
                    type: 'audio/wav'
                });
                //创建文件并发送
                let formData = new FormData();
                formData.append('file', wavBlob, 'output.wav');
                let that = this;
                //语音生成文字
                fetch('http://127.0.0.1:5000', {
                        method: "POST",
                        body: formData,
                    }).then(respose => {
                        return respose.json();
                    }).then(data => {
                        let result = data.result;
                        that.Answer_text(result);
                        let AudioMsg = {
                            id: 1001,
                            msg: result,
                        };
                        this.chat_histories.push(AudioMsg);
                        console.log(result);
                    })
                    .catch(err => {
                        console.log("appear lose", err);
                    })
                this.recordedChunks = [];
            }

        },
        //生成文字回应
        Answer_text(question) {
            console.log("开始生成文字回应",question);
            if(question==""){

                if(!this.overTimer){
                    this.$message("您不想聊天了吗？可以按右侧红色按键取消聊天哦，如果长时间不聊天，30秒后会为您自动挂断哦");
                    this.overTimer = setTimeout(this.TelDown,30000);
                }             
                this.startAudio();
                return;
            }else{
                console.log("继续聊天哦");
                if(this.overTimer) clearTimeout(this.overTimer);
            }
            console.log("开始回答");
            let data = {
                "conversation_id": "123",
                "bot_id": "7391681464909266953",
                "user": "CustomizedString123",
                "query": question,
                "stream": false,
                "chat_history": this.chat_histories,
            }
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
                let json = await respose.json();
                let i;
                for (i = 0; i < json["messages"].length; i++) {
                    if (json["messages"][i]["type"] == "answer")
                        break;
                }
                let answer = await json["messages"][i]["content"];
                console.log("answer:",answer);
                let AudioMsg = {
                    id: 1002,
                    msg: answer,
                };
                //语音生成回应
                that.Content = answer;
                that.chat_histories.push(AudioMsg);
            }
            getData(data);
        },

        //语音合成并播放
        TelGet() {
            // this.$message("TelPhone 页面开始");
            console.log("开始生成语音");
            const that = this;
            fetch('http://127.0.0.1:5000/heChengAudio', {
                method: "POST",
                headers: {
                    "Content-type": "application/json",
                },
                body: JSON.stringify({
                    "text": that.Content
                }),
            }).then((respose) => {
                return respose.blob();
            }).then((blob) => {
                if(!this.isInit){
                    this.started();
                    this.isInit = true;
                }
                const audioUrl = URL.createObjectURL(blob);
                let audioPlayer = document.querySelector('.audioPlayer');
                audioPlayer.src = audioUrl;
                // that.Content = "妈妈，我很好";
                audioPlayer.onended = () =>{
                  that.isParent = true;
                  that.startAudio();
                }
            }).catch((err) => {
                console.log(err)
            });
        },
        TelDown() {
            //关闭相关的定时器与设备连接
            if(this.scriptNode)
            this.scriptNode.disconnect();
            if(this.VolumeTimer)
            clearInterval(this.VolumeTimer);
            if(this.EmotionInterval)
            clearInterval(this.EmotionInterval);
            this.isOver = true;
            this.stopAudio();
            this.stopVideo();

            document.startViewTransition(() => {
                let TelTurnOff = document.querySelector(".turnoff");
                TelTurnOff.classList.remove('hidden');
                clearInterval(this.timer);
                document.querySelector('.bottom_later').classList.add('hidden');
                document.querySelector('.bottom_end').classList.remove('hidden');
                setTimeout(() => {
                    // 通过XPath寻找元素位置
                    let btn = document.evaluate('//*[@id="app"]/div/section/aside/div/div[1]/ul/li[1]', document).iterateNext();
                    btn.click();
                    console.log("1");
                }, 2000);
            })

        },
        stopVideo() {
            if (this.flvPlay) {
                this.flvPlay.pause();
                this.flvPlay.destroy();
                console.log("flvPlayer is destroied");
            }
        },
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
    }

};
</script>

<style lang="scss" scoped>
.chat-window {
    width: 100%;
    height: 100%;
    margin-left: 20px;
    position: relative;

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
                font-size: 12px;
                margin-top: 2px;
            }
        }

    }
}

.portrait {
    --border-color: rgb(217, 93, 48);
    width: 105px;
    height: 105px;
    border-radius: 50%;
    // border: 2px solid rgb(137,140,151);
    border: 2px solid rgb(255, 255, 255);
    position: relative;

    img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        // padding: 2px;
        box-sizing: border-box;
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        vertical-align: middle;
    }
}
.containers {
    display: flex;
    width: 400px;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.containers .point {
    width: 2em;
    height: 2em;
    border-radius: 50%;
    background-color: #fff;
    margin: 1em;
    user-select: none;
    position:relative;
}
.containers .point::before {
    position: absolute;
    content: '';
    width: 100%;
    height: 100%;
    background: inherit;
    border-radius: inherit;
    animation: wave 2s ease-out infinite;
}

@keyframes wave {
    50%,
    70% {
        transform:scale(2.5);
    }
    80%,
    100%{
        opacity: 0;
    }
}
.containers .point:nth-child(1){
    background-color:#b5f5ec;
}
.containers .point:nth-child(2){
    background-color:#87e8de;
}
.containers .point:nth-child(3){
    background-color:#5cdbd3;
}
.containers .point:nth-child(4){
    background-color:#36cfc9 ;
}
.containers .point:nth-child(5){
    background-color:#13c2c2 ;
}

.containers .point:nth-child(1)::before{
    animation-delay:0s;
}
.containers .point:nth-child(2)::before{
    animation-delay:0.2s;
}
.containers .point:nth-child(3)::before{
    animation-delay:0.4s;
}
.containers .point:nth-child(4)::before{
    animation-delay:0.6s;
}
.containers .point:nth-child(5)::before{
    animation-delay:0.8s;
}

.bottom {
    width: 100%;
    height: 70vh;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0 5px 35px rgba(0, 0, 0, 0.1);
    border-radius: 20px;
    padding: 20px;
    box-sizing: border-box;
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;

    .videoPlayer {
        width: 400px;
        height: 300px;
        border-radius: 20px;

        &::-webkit-media-controls {
            display: none !important;
        }
    }
}
.gif {
    box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    margin-left: 20px;
    // box-shadow: 0 10px 15px rgba(0, 0, 0, 1);
    overflow: hidden;
    border-radius: 20px;
    background-image: url('@/assets/img/background.jpg'); /* 替换为你的图像URL */
    background-size: cover; /* 让背景图像覆盖整个元素 */
    background-position: center; /* 将背景图像定位到元素的中心 */
    background-repeat: no-repeat; /* 防止背景图像重复 */
    width: 100%; /* 元素的宽度 */
    height: 100%; /* 元素的高度 */
    // img {
    //     height: 100%;
    // }
}
.bottom_before {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
}
.bottom_portrait{
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
}
.turnoff {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background-color: red;
    margin: 40px 35px 0 0;
    &:hover::before {
            opacity: 1;
            animation: wave 1.5s ease-out infinite;
    }
}
.turnoff::before {
    position: absolute;
    content: '';
    opacity: 0;
    width: 80px;
    height: 80px;
    background: inherit;
    border-radius: inherit;
}
@keyframes wave {
    50%,
    70% {
        transform:scale(2);
    }
    80%,
    100%{
        opacity: 0;
    }
}
.turnoff img {
    width: 80px;
    height: 80px;
    border-radius: 50%;

}
.bottom_zero {
    font-size: 30px;
    color: #fff;
    margin-bottom:70px;
}

.bottom_zero img {
    width: 50px;
    height: 50px;
    margin-right: 15px;
    vertical-align: middle;
}
.videochat {
    display: flex;
    width: 100%;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.bottom_later {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;   
}
.wait {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}
.hidden {
    display: none;
}
.background_img {
    background-image: url('@/assets/img/exit.gif'); /* 替换为你的图像URL */
    background-size: cover; /* 让背景图像覆盖整个元素 */
    background-position: center; /* 将背景图像定位到元素的中心 */
    background-repeat: no-repeat; /* 防止背景图像重复 */
    width: 100%; /* 元素的宽度 */
    height: 100%; /* 元素的高度 */
}
#videoElement {
    box-shadow: rgba(50, 50, 93, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(10, 37, 64, 0.35) 0px -2px 6px 0px inset;
}
</style>
