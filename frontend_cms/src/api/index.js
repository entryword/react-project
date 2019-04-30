import axios from 'axios'
import config from '../config'

const prefix = ' /cms/api'

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
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/topics.json"
    } else {
      url = `${prefix}/topics`
    }
    return axios({ method, url, data })
  },
  getEvents() {
    let method = "get";
    let url = "";
    let data = null;
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/events.json"
    } else {
      url = `${prefix}/events`
    }
    return axios({ method, url, data })
  },
  getEvent(id) {
    let method = "get";
    let url = "";
    let data = null;
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/event.json"
    } else {
      url = `${prefix}/event/${id}`
    }
    return axios({ method, url, data })
  },
  getPlaces() {
    let method = "get";
    let url = "";
    let data = null;
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/places.json"
    } else {
      url = `${prefix}/places`
    }
    return axios({ method, url, data })
  },
  getSpeakers() {
    let method = "get";
    let url = "";
    let data = null;
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/speakers.json"
    } else {
      url = `${prefix}/speakers`
    }
    return axios({ method, url, data })
  },
  getDefinitions() {
    let method = "get";
    let url = "";
    let data = null;
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/definitions.json"
    } else {
      url = `${prefix}/definitions`
    }
    return axios({ method, url, data })
  },
  getSlideResources() {
    let method = "get";
    let url = "";
    let data = null;
    if (process.env.NODE_ENV === 'development'){
      url = "/static/fake_data/resources.json"
    } else {
      url = `${prefix}/getSlideResources`
    }
    return axios({ method, url, data })
  },
  postEvent(data){
    let method = "POST";
    let url = "";
    if (process.env.NODE_ENV === 'development'){
      console.log(data)
      method = "get";
      url = "/static/fake_data/post_event_result.json"
    } else {
      url = `${prefix}/event`
    }
    return axios({ method, url, data })
  },
  putEvent(data){
    let method = "POST";
    let url = "";
    if (process.env.NODE_ENV === 'development'){
      console.log(data)
      method = "get";
      url = "/static/fake_data/put_event_result.json"
    } else {
      url = `${prefix}/event`
    }
    return axios({ method, url, data })
  },
  postSlide(data){
    let method = "POST";
    let url = "";
    if (process.env.NODE_ENV === 'development'){
      console.log(data)
      method = "get";
      url = "/static/fake_data/post_slide_result.json"
    } else {
      url = `${prefix}/slide`
    }
    return axios({ method, url, data })
  }
}

console.log("NODE_ENV", process.env.NODE_ENV);
