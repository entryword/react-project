import axios from 'axios'
import config from '../config'

const prefix = ' /cms/api'
const prefix_officialSite = ' /v1.0/api'
const devPrefix = '/api'
const devPrefix_officialSite = '/fapi'

const useFakeData = false;

export default {
  request (method, uri, data = null) {
    if (!method) {
      console.error('API function call requires method argument')
      return
    }

    if (!uri) {
      console.error('API function call requires uri argument')
      return
    }

    var url = config.serverURI + uri
    return axios({ method, url, data })
  },
  getTopics() {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/topics.json"
    } else if (process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/topics`
    } else {
      url = `${prefix}/topics`
    }
    return axios({ method, url, data })
  },
  getEvents() {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/events.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/events`
    } else {
      url = `${prefix}/events`
    }
    return axios({ method, url, data })
  },
  getEvent(id) {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/event.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/event/${id}`
    } else {
      url = `${prefix}/event/${id}`
    }
    return axios({ method, url, data })
  },
  getPlaces() {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/places.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/places`
    } else {
      url = `${prefix}/places`
    }
    return axios({ method, url, data })
  },
  getSpeakers() {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/speakers.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/speakers`
    } else {
      url = `${prefix}/speakers`
    }
    return axios({ method, url, data })
  },
  getDefinitions() {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/definitions.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix_officialSite}/definitions`
    } else {
      url = `${prefix_officialSite}/definitions`
    }
    return axios({ method, url, data })
  },
  getSlideResources() {
    let method = "get";
    let url = "";
    let data = null;
    if (useFakeData && process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/resources.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/slides`
    } else {
      url = `${prefix}/slides`
    }
    return axios({ method, url, data })
  },
  postEvent(data){
    let method = "POST";
    let url = "";
    if (useFakeData && process.env.NODE_ENV === 'development'){
      method = "get";
      url = "/static/fake_data/post_event_result.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/event`
    } else {
      url = `${prefix}/event`
    }
    return axios({ method, url, data })
  },
  putEvent({data, id}){
    let method = "PUT";
    let url = "";
    if (useFakeData && process.env.NODE_ENV === 'development'){
      //console.log(data)
      method = "get";
      url = "/static/fake_data/put_event_result.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/event/${id}`
    } else {
      url = `${prefix}/event/${id}`
    }
    return axios({ method, url, data })
  },
  postSlide(data){
    let method = "POST";
    let url = "";
    if (useFakeData && process.env.NODE_ENV === 'development'){
      method = "get";
      url = "/static/fake_data/post_slide_result.json"
    } else if (!useFakeData && process.env.NODE_ENV === 'development'){
      url = `${devPrefix}/slide`
    } else {
      url = `${prefix}/slide`
    }
    return axios({ method, url, data })
  }
}
