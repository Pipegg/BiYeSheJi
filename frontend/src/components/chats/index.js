import chats from "./chats";
import chatSession from './chat-session';
import button from "./button";
import dialog from "./chat-dialog";
import check from "./chat-check";
import event from "@/utils/event";
import {useChatStore} from "@/stores/chat";

function install(Vue) {
    Vue.component(chats.name , chats)
    Vue.component(chatSession.name , chatSession)
    Vue.component(button.name , button)
    Vue.component(dialog.name , dialog)
    Vue.component(check.name,check);

    event.on('login' , ()=>{
        useChatStore().login();
    });

    event.on("logout",()=>{
        useChatStore().logout();
    })


}

export default {
    install
}




