import api from "../api";
const loginUrl = '/cms/login.html';
export default {
    logout: async function(context) {
        const info = await api.getEvents().then(res => res.data.data);
        context.commit('LOG_OUT', info);
    },
    getEvents: async function(context) {
        const data = await api.getEvents().then(res => res.data);
        if (data.info.code == 0) {
            context.commit('SET_EVENTS', data.data);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    getEvent: async function(context) {
        const data = await api.getEvent().then(res => res.data);
        if (data.info.code == 0) {
            context.commit('SET_EVENT', data.data);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    getTopics: async function(context) {
        const data = await api.getTopics().then(res => res.data);
        if (data.info.code == 0) {
            context.commit('SET_TOPICS', data.data);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    getPlaces: async function(context) {
        const data = await api.getPlaces().then(res => res.data);
        if (data.info.code == 0) {
            context.commit('SET_PLACES', data.data);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    getSpeakers: async function(context) {
        const data = await api.getSpeakers().then(res => res.data);
        if (data.info.code == 0) {
            context.commit('SET_SPEAKERS', data.data);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    getDefinitions: async function(context) {
        const data = await api.getDefinitions().then(res => res.data);
        console.log(data)
        if (data.info.code == 0) {
            context.commit('SET_FIELDS', data.data.field);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    getSlideResources: async function(context) {
        const data = await api.getSlideResources().then(res => res.data);
        if (data.info.code == 0) {
            context.commit('SET_SLIDE_RESOURCES', data.data);
        } else {
            alert(data.info.message);
            window.location.href = loginUrl;
        }
    },
    postEvent: async function({ commit, state }, data) {
        const postEventResultData = await api.postEvent(data).then(res => res.data);
        if (data.info.code == 0) {
            commit('SET_SLIDE_RESOURCES', postEventResultData.data);
        } else {
            alert(data.info.message);
            // window.location.href = loginUrl;
        }
    },
    putEvent: async function({ commit, state }, data) {
        const putEventResult = await api.putEvent(data).then(res => res.data.data);
        commit('PUT_EVENT_RESULT', putEventResult);
    },
    postSlide: async function({ commit, state }, data) {
        const postSlideResultData = await api.postSlide(data).then(res => res.data);
        // commit('POST_SLIDE_RESULT', postSlideResult);
        if (data.info.code == 0) {
            commit('POST_SLIDE_RESULT', postSlideResultData.data);
        } else {
            alert(data.info.message);
            // window.location.href = loginUrl;
        }
    }
}
