export default {
  TOGGLE_LOADING (state) {
    state.callingAPI = !state.callingAPI
  },
  TOGGLE_SEARCHING (state) {
    state.searching = (state.searching === '') ? 'loading' : ''
  },
  SET_USER (state, user) {
    state.user = user
  },
  SET_TOKEN (state, token) {
    state.token = token
  },
  LOG_OUT (state, info) {
    state.log_out_info = info
  },
  SET_EVENTS (state, events){
    const weekdayString = ['日', 'ㄧ', '二', '三', '四', '五', '六']
    const modEvents = events.map(e => {
      const index = new Date(e.date).getDay()
      return {
        ...e,
        weekday: weekdayString[index]
      }
    })
    state.events = modEvents;
  },
  SET_EVENT (state, event){
    state.event = event;
  },
  SET_TOPICS (state, topics){
    const modTopics = topics.map(t => {
      return {
        ...t,
        label: `${t.id} ${t.name}`
      }
    })
    state.topics = modTopics;
  },
  SET_PLACES (state, places){
    const modPlaces = places.map(p => {
      return {
        ...p,
        label: `${p.id} ${p.name}`
      }
    })
    state.places = modPlaces;
  },
  SET_PLACE (state, place){
    state.place = place;
  },
  SET_SPEAKERS (state, speakers){
    state.speakers = speakers;
  },
  SET_ROLE (state, roles){
    state.roles = roles;
  },
  SET_FIELDS (state, fields){
   const modFields = Object.keys(fields).map(key => {
    return {
      id: parseInt(key, 10),
      name: fields[key]
    }
   })
    state.fields = modFields;
  },
  SET_SLIDE_RESOURCES (state, resources){
    state.slide_resources = resources && resources.length > 0 ? resources.reverse() : resources;
  },
  POST_EVENT_RESULT(state, postEventResult){
    state.post_event_result = postEventResult;
  },
  POST_PLACE_RESULT(state, postPlaceResult){
    state.post_place_result = postPlaceResult;
  },
  PUT_EVENT_RESULT(state, putEventResult){
    state.put_event_result = putEventResult;
  },
  PUT_PLACE_RESULT(state, putPlaceResult){
    state.put_place_result = putPlaceResult;
  },
  POST_SLIDE_RESULT(state, postSlideResult){
    state.post_slide_result = postSlideResult;
  },
  PUT_ROLE_RESULT(state, putRoleResult){
    state.put_role_result = putRoleResult;
  },
  POST_ROLE_RESULT(state, postRoleResult){
    state.post_role_result = postRoleResult;
  }
}
