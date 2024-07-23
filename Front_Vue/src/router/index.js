import VueRouter from 'vue-router'

import ChatHome from '../view/pages/chatHome/index.vue'
import Video from '../view/pages/video.vue'
import Lingting from '../view/pages/TelPhone.vue'
import Setting from '../view/pages/setting.vue'

export default new VueRouter({
    routes: [
        {
            path: "/",
            redirect: "/ChatHome",
        },
        {
            path: "/ChatHome",
            name: "ChatHome",
            component: ChatHome,
        },
        {
            path: "/Video",
            name: "VideoPhone",
            component: Video
        },
        {
            path: "/TelPhone",
            name: "TelPhone",
            component: Lingting
        },
        {
            path: "/Setting",
            name: "Setting",
            component: Setting
        },
    ]
})