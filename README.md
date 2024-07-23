# EmotionalHelper
### 简单介绍
情感抚慰小助手是一款专为老年人设计的在线聊天机器人，旨在通过先进的技术手段，为感到孤独的老年人提供情感上的慰藉和支持。该项目采用Vue.js + flask构建，确保了用户界面的友好性和交互的流畅性

### 实现功能
1. 支持个性化对话聊天
    - 支持文字输入
    - 支持语音输入
    - 支持发送表情包、图片和文件
    - 支持键盘回车发送信息
    - 可通过对话内容，分析用户心情，并进行相应回答
2. 支持语音通话
    - 可训练个性化的语音
    - 支持自动化语音回复
3. 支持视频通话
    - 可通过用户的面部表情，分析用户心情，并进行相应回答

### 前提准备
1. 下载、安装并部署情绪识别模型
> https://github.com/simplesaad/EmotionDetection_RealTime

2. 下载并部署GPT-SOVITS模型
> https://github.com/RVC-Boss/GPT-SoVITS

### 使用手册
1. 下载代码并安装nodejs
2. 使用` npm install `安装项目依赖模块
3. 使用` npm run serve `启动开发服务
4. python创建项目，并在项目中添加并运行BackEnd中的代码
5. 运行部署好的GPT-SOVITS模型
6. 使用` npm run build `打包代码
