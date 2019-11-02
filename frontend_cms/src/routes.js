import DashView from './components/Dash.vue'
import LoginView from './components/Login.vue'
import NotFoundView from './components/404.vue'

// Import Views - Dash
import ServerView from './components/views/Server.vue'

import EventEditView from './components/views/EventEdit.vue'
import EventAddView from './components/views/EventAdd.vue'
import EventListView from './components/views/EventList.vue'
import TopicListView from './components/views/TopicList.vue'
import FieldListView from './components/views/FieldList.vue'
import PlaceListView from './components/views/PlaceList.vue'
import TutorListView from './components/views/TutorList.vue'

// Routes
const routes = [
  {
    path: '/login',
    component: LoginView
  },
  {
    path: '/',
    component: DashView,
    children: [
      {
        path: '/server',
        component: ServerView,
        name: 'Servers',
        meta: {description: 'List of our servers', requiresAuth: true}
      },
      {
        path: '/event-edit/:id',
        component: EventEditView,
        name: '活動編輯',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/event-copy/:id',
        component: EventEditView,
        name: '活動複製',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/event-add',
        component: EventAddView,
        name: '建立活動',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/',
        component: EventListView,
        name: '活動列表',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/event-list',
        component: EventListView,
        name: '活動列表',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/topic-list',
        component: TopicListView,
        name: '主題列表',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/field-list',
        component: FieldListView,
        name: '領域列表',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/place-list',
        component: PlaceListView,
        name: '場地列表',
        meta: {description: '', requiresAuth: true}
      },
      {
        path: '/tutor-list',
        component: TutorListView,
        name: '講師/助教列表',
        meta: {description: '', requiresAuth: true}
      }
    ]
  }, {
    // not found handler
    path: '*',
    component: NotFoundView
  }
]

export default routes
