import api from "../api";
export default {
    getEvents: async function(context) {
        const events = await api.getEvents().then(res => res.data.data);
        context.commit('SET_EVENTS', events);
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
    }
}
