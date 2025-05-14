import config from "../config";
import axios from "axios";

const TOKEN_KEY = 'token';
const SESSION_KEY = 'session';

export const UserStore = {
    token: localStorage.getItem(TOKEN_KEY) || '',
    session: JSON.parse(localStorage.getItem(SESSION_KEY) || '{}'),

    setToken(token) {
        this.token = token;
        localStorage.setItem(TOKEN_KEY, token);
    },

    setSession(session) {
        this.session = session;
        localStorage.setItem(SESSION_KEY, JSON.stringify(session));
    },

    clear() {
        this.token = '';
        this.session = {};
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(SESSION_KEY);
    },

    async refreshToken() {
        if (!this.token) return false;
        
        try {
            const response = await axios.get(`${config.service_url}${config.token_login}?token=${this.token}`);
            if (response.data.code === 0) {
                this.setToken(response.data.data.token);
                this.setSession(response.data.data.session);
                return true;
            }
        } catch (e) {
            console.error('Token refresh failed:', e);
        }
        
        this.clear();
        return false;
    }
};

// 初始化时尝试刷新token
UserStore.refreshToken(); 