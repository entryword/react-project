<template>
  <div>
    <form action="#" method="post">
      <section class="content">
        <!-- Main row -->
        <pre>event: {{event}}</pre>
        <pre>apply: {{processApply}}</pre>
        <!-- <pre>event: {{event}}</pre> -->
        <div class="row">
          <!-- 活動內容編輯 -->
          <div class="col-lg-12">
            <div class="box">
              <div class="box-header">
                <h3 class="box-title">活動內容新增</h3>
              </div>
              <div class="box-body">
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動名稱</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <input
                        type="text"
                        class="form-control"
                        name="event_title"
                        placeholder="活動名稱(限150字)"
                        maxlength="150"
                        v-model="title"
                      >
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動主題</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <v-select :options="topics" label="label" v-model="topicOption"></v-select>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動時間</font>
                  </div>
                  <div class="col-md-10">
                    {{eventDateTime}}
                    <div class="form-group">
                      <date-range-picker
                        :opens="dateTimeOptions.opens"
                        :locale-data="dateTimeOptions.locale"
                        :singleDatePicker="dateTimeOptions.singleDatePicker"
                        :timePicker="dateTimeOptions.timePicker"
                        :timePicker24Hour="dateTimeOptions.timePicker24Hour"
                        :showWeekNumbers="dateTimeOptions.showWeekNumbers"
                        :showDropdowns="dateTimeOptions.showDropdowns"
                        :autoApply="dateTimeOptions.autoApply"
                        :ranges="dateTimeOptions.ranges"
                        v-model="eventDateTime"
                      ></date-range-picker>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-2">活動地點</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <v-select :options="places" label="label" v-model="placeOption"></v-select>
                    </div>
                  </div>
                </div>
                <div>
                  活動內容
                  <trumbowyg
                    v-model="desc"
                    :config="editorConfig"
                    class="form-control"
                    name="content"
                  ></trumbowyg>
                </div>

                <div class="row">
                  <div class="col-md-2">講師</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <v-select :options="speakers" multiple label="name" v-model="speakerOption"></v-select>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">助教</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <v-select :options="speakers" multiple label="name" v-model="assistantOption"></v-select>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">活動領域</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <v-select multiple :options="fields" label="name" v-model="fieldOption"></v-select>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
              </div>
              <div class="box-footer">
                <!-- <button type="submit" class="btn btn-primary">儲存</button> -->
              </div>
            </div>
          </div>
          <!-- 活動內容編輯 -->

          <!-- 報名頁 -->
          <div class="col-lg-12">
            <div class="nav-tabs-custom">
              <ul class="nav nav-tabs">
                <li
                  v-for="(apply, index) in vueModel.apply"
                  :key="index"
                  v-bind:class="{ 'active': index === vueModel.applySelected }"
                >
                  <a :href="'#tab_'+index" data-toggle="tab">報名方式 {{index + 1}}</a>
                </li>
                <li class="pull-right">
                  <a class="text-muted" @click="addApply">
                    <i class="fa fa-plus-square"></i> 新增報名方式
                  </a>
                </li>
              </ul>
              <div class="tab-content">
                <div
                  class="tab-pane"
                  v-for="(apply, index) in processApply"
                  :key="index"
                  v-bind:class="{ 'active': index === vueModel.applySelected }"
                  :id="'tab_'+index"
                >
                  <!--報名tab -->
                  <div class="row">
                    <div class="col-md-2">負責單位</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        {{apply.host}}
                        <input
                          type="text"
                          class="form-control"
                          name="sign_host"
                          maxlength="150"
                          placeholder="主辦單位(限150字)"
                          v-model="apply.host"
                          @input="apply.host === $event.target.value"
                        >
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名管道</div>
                    <div class="col-md-10">
                      {{apply.channel }}
                      <div class="form-group">
                        <div class="radio" v-for="type in applyChannelType" :key="type.key">
                          <label>
                            <input
                              type="radio"
                              :name="'type_'+index"
                              :id="'channel_'+index +'_'+type.key"
                              :value="type.key"
                              :checked="apply.channel == type.key"
                              v-model="apply.channel"
                            >
                            {{type.name}}
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名方式</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <div class="radio" v-for="type in applyType" :key="type.key">
                          <label>
                            <input
                              type="radio"
                              :name="'channel_'+index"
                              :id="'type_'+ index +'_'+type.key"
                              :value="type.key"
                              :checked="apply.type == type.key"
                              v-model="apply.type"
                            >
                            {{type.name}}
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名網址</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control"
                          name="signup_url"
                          placeholder="報名網址"
                          v-model="apply.url"
                        >
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名時間</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <date-range-picker
                          :opens="dateTimeOptions.opens"
                          :locale-data="dateTimeOptions.locale"
                          :singleDatePicker="dateTimeOptions.singleDatePicker"
                          :timePicker="dateTimeOptions.timePicker"
                          :timePicker24Hour="dateTimeOptions.timePicker24Hour"
                          :showWeekNumbers="dateTimeOptions.showWeekNumbers"
                          :showDropdowns="dateTimeOptions.showDropdowns"
                          :autoApply="dateTimeOptions.autoApply"
                          :ranges="dateTimeOptions.ranges"
                          v-model="apply.applyDateTime"
                        ></date-range-picker>
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名費用</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control"
                          name="signup_price"
                          placeholder="報名費用"
                          v-model="apply.price"
                        >
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名對象</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control"
                          name="signup_limit"
                          placeholder="報名對象"
                          v-model="apply.limit"
                        >
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <!-- /.tab-content -->
          </div>
          <!-- 報名頁 -->
          <!-- 投影片 -->
          <div class="col-lg-12">
            <div class="box">
              <div class="box-header">
                <h3 class="box-title">投影片/資源</h3>
              </div>
              <!-- /.box-header -->
              <div class="box-body no-padding">
                <table class="table table-striped">
                  <thead>
                    <tr>
                      <th style="width: 10px">#</th>
                      <th>投影片/資源名稱</th>
                      <th>投影片/資源類型</th>
                      <th style="width: 40px">
                        <a data-toggle="modal" data-target="#slide_add">
                          <span class="badge bg-light-blue">新增</span>
                        </a>
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in vueModel.slide_resources" :key="index">
                      <td>{{index + 1}}</td>
                      <td>
                        <a :href="item.url" target="_blank">{{item.title}}</a>
                      </td>
                      <td>{{RESOURCE_TYPE[item.type]}}</td>
                      <td>
                        <span class="badge bg-red">刪除</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <!-- /.box-body -->
            </div>
            <!-- /.box -->
          </div>
          <!-- 投影片 -->
        </div>
        <!-- /.row (main row) -->
        <div class="row">
          <div class="col-lg-12">
            <button type="submit" class="btn btn-primary">儲存</button>
          </div>
        </div>
      </section>
    </form>
    <!-- Modal -->
    <div id="slide_add" class="modal fade" role="dialog">
      <div class="modal-dialog">
        <!-- Modal content-->
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal">&times;</button>
            <h4 class="modal-title">新增投影片 / 資源</h4>
          </div>
          <div class="modal-body">
            <div class="form-inline">
              <div class="form-group">
                <div class="radio">
                  <label>
                    <input
                      type="radio"
                      name="optionsRadios"
                      id="optionsRadios1"
                      value="option1"
                      checked
                    >
                    新投影片
                  </label>
                </div>
              </div>
              <div class="form-group">
                <div class="radio">
                  <label>
                    <input
                      type="radio"
                      name="optionsRadios"
                      id="optionsRadios2"
                      value="option2"
                      checked
                    >
                    新資源
                  </label>
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-3">名稱</div>
              <div class="col-md-9">
                <div class="form-group">
                  <input
                    type="text"
                    class="form-control"
                    name="signup_price"
                    placeholder="投影片名稱"
                    value="Git 上半場"
                  >
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-3">網址</div>
              <div class="col-md-9">
                <div class="form-group">
                  <input
                    type="text"
                    class="form-control"
                    name="signup_price"
                    placeholder="投影片網址"
                    value="https://www.google.com"
                  >
                </div>
              </div>
            </div>

            <div class="radio">
              <label style="width: 100%">
                <input type="radio" name="optionsRadios" id="optionsRadios2" value="option2">
                從已有投影片/資源選擇
                <v-select :options="slide_resources" label="title" v-model="slideResourceOption"></v-select>
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-primary" data-dismiss="modal">儲存</button>
            <button type="button" class="btn btn-default" data-dismiss="modal">關閉</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal END -->
  </div>
</template>
<script>
import moment from "moment";
import Vue from "vue";
import vSelect from "vue-select";
import DateRangePicker from "vue2-daterange-picker";
import Trumbowyg from "vue-trumbowyg";
import { RESOURCE_TYPE, APPLY_TYPE, CHANNEL_TYPE } from "../../config/constant";

import store from "../../store";
import { mapState, mapActions } from "vuex";

export default {
  name: "EventEdit",
  filters: {
    date(value) {
      let options = { year: "numeric", month: "long", day: "numeric" };
      return Intl.DateTimeFormat("en-US", options).format(value);
    }
  },
  components: { "v-select": vSelect, DateRangePicker, Trumbowyg },
  created() {
    this.getData(this.$route.params.id);
  },
  data: function() {
    return {
      RESOURCE_TYPE: RESOURCE_TYPE,
      APPLY_TYPE: APPLY_TYPE,
      CHANNEL_TYPE: CHANNEL_TYPE,
      dateTimeOptions: {
        opens: "center",
        locale: { firstDay: 0, format: "YYYY-MM-DD HH:mm" },
        singleDatePicker: false,
        timePicker: true,
        timePicker24Hour: true,
        showWeekNumbers: false,
        showDropdowns: false,
        autoApply: false,
        ranges: false
      },
      editorConfig: {},
      slideResourceOption: {}
      // eventDateTime1: { startDate: moment(), endDate: moment() }
    };
  },
  computed: {
    ...mapState([
      "topics",
      "places",
      "speakers",
      "fields",
      "slide_resources",
      "event"
    ]),
    applyChannelType: function() {
      return Object.keys(this.CHANNEL_TYPE).map(key => {
        return { key: key, name: CHANNEL_TYPE[key] };
      });
    },
    applyType: function() {
      return Object.keys(this.APPLY_TYPE).map(key => {
        return { key: key, name: APPLY_TYPE[key] };
      });
    },
    title: {
      get: function() {
        return this.event.title;
      },
      set: function(newValue) {
        this.event.title = newValue;
      }
    },
    desc: {
      get: function() {
        return this.event.desc;
      },
      set: function(newValue) {
        this.event.desc = newValue;
      }
    },
    eventDateTime: {
      get: function() {
        if (this.event.start_date) {
          return {
            startDate: moment(
              `${this.event.start_date} ${this.event.start_time}`
            ),
            endDate: moment(`${this.event.end_date} ${this.event.end_time}`)
          };
        }
      },
      set: function(newValue) {
        this.event.start_date = moment(newValue.startDate).format("YYYY-MM-DD");
        this.event.start_time = moment(newValue.startDate).format("HH:mm");
        this.event.end_date = moment(newValue.endDate).format("YYYY-MM-DD");
        this.event.end_time = moment(newValue.endDate).format("HH:mm");
      }
    },
    vueModel: {
      get: function() {
        return {
          eventDateTime: {
            startDate: moment(
              `${this.event.start_date} ${this.event.start_time}`
            ).toDate(),
            endDate: moment(
              `${this.event.end_date} ${this.event.end_time}`
            ).toDate()
          },
          title: this.event.title,
          topic_id: this.event.topic_id,
          start_date: this.event.start_date,
          start_time: this.event.start_time,
          end_date: this.event.end_date,
          end_time: this.event.end_time,
          desc: this.event.desc,
          place_id: this.event.place_id,
          speaker_ids: this.event.speaker_ids,
          assistant_ids: this.event.assistant_ids,
          field_ids: this.event.field_ids,
          slide_resources: this.event.slide_resources,
          applySelected: 0,
          apply: this.event.apply
        };
      }
    },
    processApply: {
      get: function() {
        return this.vueModel.apply
          ? this.vueModel.apply.map(a => ({
              host: a.host,
              channel: a.channel,
              type: a.type,
              applyDateTime: {
                startDate: moment(a.start_time).toDate(),
                endDate: moment(a.end_time).toDate()
              },
              start_time: a.start_time,
              end_time: a.end_time,
              price: a.price,
              limit: a.limit,
              url: a.url
            }))
          : [];
      },
      set: function(newValue) {
        console.log(newValue);
        this.vueModel.apply = newValue.map(a => ({
          host: a.host,
          channel: a.channel,
          type: a.type,
          start_time: moment(a.applyDateTime.startDate).format(
            "YYYY-MM-DD HH:mm"
          ),
          end_time: moment(a.applyDateTime.endDate).format("YYYY-MM-DD HH:mm"),
          price: a.place,
          limit: a.limit,
          url: a.url
        }));
        // console.log(this.vueModel.apply);
      }
    },
    placeOption: {
      get: function() {
        const default_place = {
          id: 37,
          name: "未定",
          addr: "未定",
          label: "37 未定"
        };

        if (this.event.place_info && this.event.place_info.id) {
          const place = this.places.filter(
            p => p.id === this.event.place_info.id
          );
          if (place.length > 0) {
            return place;
          } else {
            return default_place;
          }
        } else {
          return default_place;
        }
      },
      set: function(newValue) {
        this.event.place_info = {
          id: newValue.id,
          name: newValue.name
        };
      }
    },
    topicOption: {
      get: function() {
        if (this.event.topic_id) {
          const topic = this.topics.filter(t => t.id === this.event.topic_id);
          if (topic.length > 0) {
            return topic;
          } else {
            return null;
          }
        } else {
          return null;
        }
      },
      set: function(newValue) {
        this.event.topic_id = newValue.id;
      }
    },
    speakerOption: {
      get: function() {
        if (this.event.speakers) {
          const event_speakers_id = this.event.speakers.map(s => s.id);
          const a = this.speakers.reduce((acc, item, index) => {
            if (event_speakers_id.indexOf(item.id) >= 0) {
              return [...acc, this.speakers[index]];
            }
            return acc;
          }, []);
          return a;
        }
        return [];
      },
      set: function(newValue) {
        this.vueModel.speaker_ids = newValue.map(s => s.id);
        this.event.speakers = newValue.map(s => ({
          id: s.id,
          name: s.name
        }));
      }
    },
    assistantOption: {
      get: function() {
        if (this.event.assistants) {
          const event_assistants_id = this.event.assistants.map(s => s.id);
          return this.speakers.reduce((acc, item, index) => {
            if (event_assistants_id.indexOf(item.id) >= 0) {
              return [...acc, this.speakers[index]];
            }
            return acc;
          }, []);
        }
        return [];
      },
      set: function(newValue) {
        this.vueModel.assistant_ids = newValue.map(s => s.id);
        this.event.assistants = newValue.map(s => ({
          id: s.id,
          name: s.name
        }));
      }
    },
    fieldOption: {
      get: function() {
        if (this.event.field) {
          return this.fields.reduce((acc, item, index) => {
            if (this.event.field.indexOf(item.id) >= 0) {
              return [...acc, this.fields[index]];
            }
            return acc;
          }, []);
        }
        return [];
      },
      set: function(newValue) {
        this.vueModel.field = newValue.map(s => s.id);
        this.event.field = newValue.map(s => s.id);
      }
    }
  },
  watch: {
    processApply(newValue) {
      console.log(newValue);
    }
  },
  methods: {
    ...mapActions([
      "getTopics",
      "getPlaces",
      "getSpeakers",
      "getDefinitions",
      "getSlideResources",
      "getEvent"
    ]),
    clearInput(vueModel) {
      vueModel = {};
    },
    getData(id) {
      this.getTopics();
      this.getPlaces();
      this.getSpeakers();
      this.getDefinitions();
      this.getSlideResources();
      this.getEvent(id);
    },
    addApply() {
      this.vueModel.apply.push({
        host: "",
        channel: null,
        type: null,
        applyDateTime: null,
        start_time: "",
        end_time: "",
        price: "",
        limit: "",
        url: ""
      });
      this.vueModel.applySelected = this.vueModel.apply.length - 1;
    },
    submit() {
      // check required data
      // convert data
      //call api
    }
  }
};
</script>

