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
        <!-- accept="application/*" -->
    </div>
    <div class="bottom">
        <audio controls style="display: none;" class="audioPlayer" autoplay></audio>
        <div class="bottom_zero hidden">
            <div class="Connecting" alt="">
                <img src="@/assets/img/TelOn.png">
                {{ waitMsg }}
            </div>
        </div>
        <div class="bottom_one">
            <div class="portrait">
                <img :src="imgHead" alt="">
            </div>
            <div class="turnoff hidden" alt="" @click="TelDown">
                <img src="@/assets/img/turnoff.png">
            </div>
        </div>
        <div class="bottom_two">
            <div class="TelTime" alt="">
                <img :src="TelState">
                {{ DisplayTelTime }}
            </div>
        </div>
    </div>
</div>
</template>

<script>
// import { getChatMsg } from "@/api/getData";
import HeadPortrait from "@/components/HeadPortrait";
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
            imgHead: require('@/assets/img/head_portrait.jpg'),
            TelState: require('@/assets/img/TelOn.png'),
            DisplayTelTime: "正在呼叫中……",
            TelTime: 0,
            timer: 0,
            overTimer:0,
            VolumeTimer:'',
            Content: "妈，怎么啦？",
            recordedChunks: [],
            overVolume: 0,
            isOver: false,
            waitMsg:"正在通话中……",
            scriptNode:'',
            isInit:false,
            chat_histories: [{
                id: 1002,
                msg: "妈，怎么啦？",
            }, ]
        };
    },
    mounted() {
        // this.Connect_phone();
        this.TelGet();
    },
    watch: {
        Content: {
            // 使用 handler 属性指定当 chatList 发生变化时调用 ChangeChatList 方法
            handler(newVal, oldVal) {
                this.TelGet();
            },
            // deep: true 表示深度监视，可以监视对象内部属性的变化
            deep: true
        }
    },
    methods: {
        TelTimeStart() {
            this.timer = setInterval(() => {
                this.TelTime += 1;
                this.DisplayTime();

                // console.log(this.TelTime);
            }, 1000);
        },
        DisplayTime() {
            let minutes = Math.floor(this.TelTime / 60) < 10 ? ('0' + Math.floor(this.TelTime / 60)) : String(Math.floor(this.TelTime / 60));
            let seconds = (this.TelTime % 60) < 10 ? ('0' + this.TelTime % 60) : String(this.TelTime % 60);
            this.DisplayTelTime = minutes + " : " + seconds;
        },

        //----------------------------------------------------------
        //接通电话动画
        Connect_phone() {
                //添加动画
                document.startViewTransition(() => {
                    //移除隐藏特性
                    document.querySelector('.turnoff').classList.remove('hidden');
                    document.querySelector('.bottom_zero').classList.remove('hidden');
                    //更改小圆圈的颜色
                    document.querySelector('.portrait').style.setProperty('--border-color', '#6beb6b');
                    //换成钟表图像
                    this.TelState = require('@/assets/img/TelTime.png');
                    //设置并显示事件
                    this.DisplayTime();
                    this.TelTimeStart();
                    // this.TelGet();
                })
            //先打招呼
        },
        //接听语音(录音开始)
        startAudio() {
            console.log("录音开始");
            this.waitMsg = "您要跟我说点什么呢？😀"
            document.querySelector('.bottom').style.backgroundColor = "rgb(0,206,209,0.5)";
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
            this.waitMsg = "思考中……请稍后……";
            document.querySelector('.bottom').style.backgroundColor = "rgb(0, 255, 127,0.5)";
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
                        "Authorization": "Bearer pat_6os9bFhLhhTHGU3RtnXr5zBk35SsY4ywysS1JhR90aTpqWuYmv8O6HkUnRIHWBKd",
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
            this.waitMsg = "思考中……请稍后……";
            document.querySelector('.bottom').style.backgroundColor = "rgb(0, 255, 127,0.5)";
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
                
                const audioUrl = URL.createObjectURL(blob);
                let audioPlayer = document.querySelector('.audioPlayer');
                audioPlayer.src = audioUrl;
                setTimeout(() => {
                    if(!this.isInit){
                        this.Connect_phone();
                        this.isInit = true;
                    }
                })
                this.waitMsg = "正在通话中……";
                // that.Content = "妈妈，我很好";
                audioPlayer.onended = () =>{
                  that.startAudio();
                }
            }).catch((err) => {
                console.log(err)
            });
        },
        TelDown() {
            this.scriptNode.disconnect();
            this.isOver = true;
            this.stopAudio();
            if(this.VolumeTimer)
                clearInterval(this.VolumeTimer);
            document.startViewTransition(() => {
                this.TelState = require('@/assets/img/TelDown.png');
                let TelTurnOff = document.querySelector(".turnoff");
                TelTurnOff.classList.remove('hidden');
                clearInterval(this.timer);
                this.TelTime = 0;
                this.DisplayTelTime = "已挂断……";
                document.querySelector('.bottom_zero').classList.add('hidden');
                const Timeid = setTimeout(() => {
                    // 通过XPath寻找元素位置
                    let btn = document.evaluate('//*[@id="app"]/div/section/aside/div/div[1]/ul/li[1]', document).iterateNext();
                    btn.click();
                    console.log("1");
                }, 2000);
            })

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
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.bottom_one {
    width: 100%;
    height: 30vh;
    box-sizing: border-box;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

.portrait {
    --border-color: rgb(217, 93, 48);
    width: 105px;
    height: 105px;
    border-radius: 50%;
    // border: 2px solid rgb(137,140,151);
    border: 2px solid rgb(255, 255, 255);
    position: relative;

    &::before {
        content: '';
        width: 25px;
        height: 25px;
        z-index: 1;
        display: block;
        border-radius: 50%;
        background-color: var(--border-color);
        position: absolute;
        right: 0;
    }

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
.turnoff {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    margin-left: 200px;
    background-color: red;
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

.hidden {
    display: none;
}

.bottom_two {
    font-size: 30px;
    color: #fff;

}

.bottom_two img {
    width: 50px;
    height: 50px;
    margin-right: 15px;
    vertical-align: middle;
}

.bottom_zero {
    font-size: 30px;
    color: #fff;

}

.bottom_zero img {
    width: 50px;
    height: 50px;
    margin-right: 15px;
    vertical-align: middle;
}
</style>
