import api from "../api";
export default {
    getEvents: async function(context) {
        const events = await api.getEvents().then(res => res.data.data);
        context.commit('SET_EVENTS', events);
    },
    getEvent: async function(context) {
        const event = await api.getEvent().then(res => res.data.data);
        context.commit('SET_EVENT', event);
    },
    getTopics: async function(context) {
        const topics = await api.getTopics().then(res => res.data.data);
        context.commit('SET_TOPICS', topics);
    },
    getPlaces: async function(context) {
        const places = await api.getPlaces().then(res => res.data.data);
        context.commit('SET_PLACES', places);
    },
    getSpeakers: async function(context) {
        const speakers = await api.getSpeakers().then(res => res.data.data);
        context.commit('SET_SPEAKERS', speakers);
    },
    getDefinitions: async function(context) {
        const definitions = await api.getDefinitions().then(res => res.data.data);
        context.commit('SET_FIELDS', definitions.field);
    },
    getSlideResources: async function(context) {
        const slide_resources = await api.getSlideResources().then(res => res.data.data);
        context.commit('SET_SLIDE_RESOURCES', slide_resources);
    },
    postEvent: async function({ commit, state }, data) {
        const postEventResult = await api.postEvent(data).then(res => res.data.data);
        commit('POST_EVENT_RESULT', postEventResult);
    },
    putEvent: async function({ commit, state }, data) {
        const putEventResult = await api.putEvent(data).then(res => res.data.data);
        commit('PUT_EVENT_RESULT', putEventResult);
    },
    postSlide: async function({ commit, state }, data) {
        const postSlideResult = await api.postSlide(data).then(res => res.data.data);
        commit('POST_SLIDE_RESULT', postSlideResult);
    }
}
