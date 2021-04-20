import Vue from 'vue';
import Vuex from 'vuex';
import * as moment from "moment";

Vue.use(Vuex);

export const store = new Vuex.Store({
    state: {
        user: {},
        io: {},
        login: false,
        notification: {},
        logs: [],
        ioConnected: false,
        userMessage: null,
        dealerMessage: null,
        alert: false,
        currency: 1
    },
    mutations: {
        setUser(state, user) {
            state.user.username = user.username;
            state.user.role = user.role;
            state.user.settings = {};
            state.user.loginTime = localStorage.getItem('loginTime');
            if (user.settings) {
                for (let i of user.settings) {
                    state.user.settings[i.name] = i.value;
                }
            }
        },
        setLoginTime() {
            const loginTime = moment(new Date()).utc().format('YYYY-MM-DD HH:mm:ss');
            localStorage.setItem('loginTime', loginTime);
        },
        removeLoginTime() {
            localStorage.removeItem('loginTime');
        },
        setLog(state, log) {
            state.logs.push(log);
        },
        popLog(state) {
            state.logs.pop()
        },
        setLogin(state, login) {
            state.login = login
        },
        setSocket: (state, socket) => {
            state.io = socket
        },
        setNotify: (state, notification) => {
            state.notification = notification
        },
        setAlert: (state, alert) => {
            state.alert = alert;
        },
        setCurrency: (state, currency) => {
            state.currency = currency;
        },
        SOCKET_CONNECT: (state, status) => {
            state.ioConnected = true;
        },
        SOCKET_IDENTIFY: (state, message) => {

        },
        SOCKET_USER_TRIGGER: (state, message) => {

            state.userMessage = message;
        },
        SOCKET_DEALER_TRIGGER: (state, message) => {
            if (message instanceof Array) {
                message = message[0]
            }
            console.log('event received -----> ' + message);
            console.log('event type -----> ' + typeof message);
            let msg = {};
            msg.params = message.params;
            msg.status = message.status;
            state.dealerMessage = msg;
        },
        SOCKET_USER_NOTIFY: (state, message) => {
            state.message = message;
        }
    },
    actions: {
        socket_identify: (context) => {
            //identify as current user
            context.state.io.emit('userIdentify', context.state.user);
        },
        socket_userNotify: (context, message) => {
            console.log('event received -----> ' + message);
            if (message === 'DONE') {
                context.state.io.emit('trigger', 'need more spam');
            }
        },
        socket_userTrigger: (context, message) => {
            // context.dispatch('userNotify', message);
            // context.commit('NEW_MESSAGE_RECEIVED', message);
            // if (message.is_important) {
            //     context.dispatch('alertImportantMessage', message);
            // }
            console.log('event received -----> ' + message)
        }

    },
    getters: {
        getUser: state => {
            return state.user
        },
        getLogs: state => {
            return state.logs
        },
        getUserMessage(state) {
            if (state.userMessage instanceof Array) {
                return state.userMessage[0]
            }
            return state.userMessage
        },
        getConnect(state) {
            return state.ioConnected
        },
        getDealerMessage(state) {
            if (state.dealerMessage instanceof Array) {
                return state.dealerMessage[0]
            }
            return state.dealerMessage
        },
        getCurrency: (state) => {
            return state.currency;
        },
    }
});

