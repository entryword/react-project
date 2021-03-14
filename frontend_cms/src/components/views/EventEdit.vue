<template>
  <div>
    <form @submit="submit">
      <section class="content">
        <!-- Main row -->
        <!-- <pre>vueModel: {{vueModel}}</pre> -->
        <div class="row">
          <!-- 活動內容編輯 -->
          <div class="col-lg-12">
            <div class="box" id="basic_info">
              <div class="box-header">
                <h3 class="box-title" v-if="isEdit">活動內容編輯</h3>
                <button
                  v-if="isEdit"
                  class="btn btn-primary pull-right"
                  @click.stop.prevent="goCopy"
                >複製此活動</button>
                <h3 class="box-title" v-if="!isEdit">活動內容複製 - 從活動 {{id}} 複製</h3>
              </div>
              <div class="box-body">
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動名稱</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.title }">
                      <input
                        type="text"
                        class="form-control"
                        name="event_title"
                        placeholder="活動名稱(限150字)"
                        maxlength="150"
                        v-model="title"
                      />
                      <div v-if="errors.title" class="help-block">請填寫活動名稱</div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動主題</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.topic }">
                      <v-select
                        :options="topics"
                        :clearable="false"
                        label="label"
                        v-model="topicOption"
                      ></v-select>
                      <div v-if="errors.topic" class="help-block">請選擇活動主題</div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動時間</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.eventDateTime }">
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
                      <div v-if="errors.eventDateTime" class="help-block">請選擇活動時間 (點選 Apply)</div>
                      <div style="font-size: 12px;color:#aaa;">如果活動在同一天，同一個日期要按兩次代表開始和結束日期</div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動領域</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.fields }">
                      <v-select multiple :options="fields" label="name" v-model="fieldOption"></v-select>
                      <div v-if="errors.fields" class="help-block">請選擇活動領域</div>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">活動地點</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <v-select
                        :options="places"
                        :clearable="false"
                        label="label"
                        v-model="placeOption"
                      ></v-select>
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
              <ul class="nav nav-tabs apply-tabs">
                <li
                  v-for="(apply, index) in processApply"
                  :key="index"
                  v-bind:class="{ 'active': index === applySelected }"
                >
                  <a
                    :href="'#tab_'+index"
                    data-toggle="tab"
                    @click="applySelected=index"
                  >報名方式 {{index + 1}}</a>
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
                  v-bind:class="{ 'active': index === applySelected }"
                  :id="'tab_'+index"
                >
                  <!--報名tab -->
                  <div class="row">
                    <div class="col-md-2">負責單位</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control"
                          name="sign_host"
                          maxlength="150"
                          placeholder="主辦單位(限150字)"
                          v-model="apply.host"
                          v-on:keyup="applyChange(index, 'host', apply.host)"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名管道</div>
                    <div class="col-md-10">
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
                              @change="applyChange(index, 'channel', type.key)"
                            />
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
                              @change="applyChange(index, 'type', type.key)"
                            />
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
                          v-on:keyup="applyChange(index, 'url', apply.url)"
                        />
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
                          @update="applyDataTimeChange(index, apply.applyDateTime)"
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
                          v-on:keyup="applyChange(index, 'price', apply.price)"
                        />
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
                          v-on:keyup="applyChange(index, 'limit', apply.limit)"
                        />
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-12" style="text-align:right">
                      <span class="badge bg-red" @click="deleteApply(index)">刪除</span>
                      <span style="color: #666;font-size: 12px;">(刪除此報名方式後會無法復原，請謹慎處理)</span>
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
                      <th style="width: 10px">id</th>
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
                    <tr v-for="(item, index) in slide_resources_list" :key="index">
                      <td>{{item.id}}</td>
                      <td>
                        <a :href="item.url" target="_blank">{{item.title}}</a>
                      </td>
                      <td>{{RESOURCE_TYPE[item.type]}}</td>
                      <td>
                        <span class="badge bg-red" @click="deleteSlide(index)">刪除</span>
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
            <div class="box-footer">
              <button type="submit" class="btn btn-primary pull-right">儲存</button>
            </div>
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
            <!-- <pre>{{newSlide}}</pre> -->
            <div class="form-inline">
              <div class="form-group">
                <div class="radio">
                  <input
                    type="radio"
                    name="optionsRadios"
                    id="optionsRadios1"
                    value="slide"
                    :checked="newSlide.type == 'slide'"
                    v-model="newSlide.type"
                  />
                  新投影片
                </div>
              </div>
              <div class="form-group">
                <div class="radio">
                  <input
                    type="radio"
                    name="optionsRadios"
                    id="optionsRadios2"
                    value="resource"
                    :checked="newSlide.type == 'resource'"
                    v-model="newSlide.type"
                  />
                  新資源
                </div>
              </div>
            </div>
            <div class="row">
              <div class="col-md-3">名稱</div>
              <div class="col-md-9">
                <div class="form-group">
                  <label>
                    <input
                      type="text"
                      class="form-control"
                      name="signup_price"
                      placeholder="投影片名稱"
                      v-model="newSlide.title"
                    />
                  </label>
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
                    v-model="newSlide.url"
                  />
                </div>
              </div>
            </div>

            <div class="radio">
              <label style="width: 100%" for="optionsRadios3">
                <input
                  type="radio"
                  name="optionsRadios"
                  id="optionsRadios3"
                  value="exist"
                  v-model="newSlide.type"
                />
                從已有投影片/資源選擇
                <v-select :options="slide_resources" label="title" v-model="newSlide.selectedSlide"></v-select>
              </label>
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-primary"
              data-dismiss="modal"
              @click="addNewSlide"
            >儲存</button>
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
      id: this.$route.params.id,
      isEdit: /event-edit/.test(this.$route.path),
      errors: {
        title: false,
        topic: false,
        eventDateTime: false,
        fields: false
      },
      vueModel: {
        title: null,
        topic_id: null,
        start_date: null,
        start_time: null,
        end_date: null,
        end_time: null,
        place_id: 37,
        desc: null,
        speaker_ids: [],
        assistant_ids: [],
        field_ids: [],
        slide_resource_ids: [],
        apply: []
      },
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
      newSlide: {
        title: null,
        url: "",
        type: null,
        selectedSlide: null
      },
      applySelected: 0
    };
  },
  computed: {
    ...mapState([
      "topics",
      "places",
      "speakers",
      "fields",
      "slide_resources",
      "event",
      "put_event_result",
      "post_event_result",
      "post_slide_result"
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
        return this.vueModel.title;
      },
      set: function(newValue) {
        this.errors.title = false;
        this.vueModel.title = newValue;
      }
    },
    desc: {
      get: function() {
        return this.vueModel.desc;
      },
      set: function(newValue) {
        this.vueModel.desc = newValue;
      }
    },
    eventDateTime: {
      get: function() {
        if (this.vueModel.start_date) {
          return {
            startDate: moment(
              `${this.vueModel.start_date} ${this.vueModel.start_time}`
            ),
            endDate: moment(
              `${this.vueModel.end_date} ${this.vueModel.end_time}`
            )
          };
        }
      },
      set: function(newValue) {
        this.errors.eventDateTime = false;
        this.vueModel.start_date = moment(newValue.startDate).format(
          "YYYY-MM-DD"
        );
        this.vueModel.start_time = moment(newValue.startDate).format("HH:mm");
        this.vueModel.end_date = moment(newValue.endDate).format("YYYY-MM-DD");
        this.vueModel.end_time = moment(newValue.endDate).format("HH:mm");
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
        // this.event.apply = [...this.vueModel.appy];
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

        if (this.vueModel.place_id) {
          const place = this.places.filter(
            p => p.id === this.vueModel.place_id
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
        if (!newValue) {
          this.vueModel.place_id = 37;
        } else {
          this.vueModel.place_id = newValue.id;
        }
      }
    },
    topicOption: {
      get: function() {
        if (this.vueModel.topic_id) {
          const topic = this.topics.filter(
            t => t.id === this.vueModel.topic_id
          );
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
        if (!newValue) {
          this.vueModel.topic_id = null;
        } else {
          this.errors.topic = false;
          this.vueModel.topic_id = newValue.id;
        }
      }
    },
    speakerOption: {
      get: function() {
        if (this.vueModel.speaker_ids) {
          return this.speakers.reduce((acc, item, index) => {
            if (this.vueModel.speaker_ids.indexOf(item.id) >= 0) {
              return [...acc, this.speakers[index]];
            }
            return acc;
          }, []);
        }
        return [];
      },
      set: function(newValue) {
        if (newValue) {
          this.vueModel.speaker_ids = newValue.map(s => s.id);
        } else {
          this.vueModel.speaker_ids = [];
        }
      }
    },
    assistantOption: {
      get: function() {
        if (this.vueModel.assistant_ids) {
          return this.speakers.reduce((acc, item, index) => {
            if (this.vueModel.assistant_ids.indexOf(item.id) >= 0) {
              return [...acc, this.speakers[index]];
            }
            return acc;
          }, []);
        }
        return [];
      },
      set: function(newValue) {
        if (newValue) {
          this.vueModel.assistant_ids = newValue.map(s => s.id);
        } else {
          this.vueModel.assistant_ids = [];
        }
      }
    },
    fieldOption: {
      get: function() {
        if (this.vueModel.field_ids) {
          return this.fields.reduce((acc, item, index) => {
            if (this.vueModel.field_ids.indexOf(item.id) >= 0) {
              return [...acc, this.fields[index]];
            }
            return acc;
          }, []);
        }
        return [];
      },
      set: function(newValue) {
        this.errors.fields = false;
        if (newValue) {
          this.vueModel.field_ids = newValue.map(s => s.id);
        } else {
          this.vueModel.field_ids = [];
        }
      }
    },
    slide_resources_list: {
      get: function() {
        if (
          this.vueModel.slide_resource_ids &&
          this.vueModel.slide_resource_ids.length > 0
        ) {
          return this.slide_resources.filter(s => {
            const id = parseInt(s.id, 10);
            return this.vueModel.slide_resource_ids.indexOf(id) >= 0;
          });
        } else {
          return [];
        }
      },
      set: function(newValue) {
        if (newValue) {
          this.vueModel.slide_resource_ids = newValue.map(s =>
            parseInt(s.id, 10)
          );
          this.event.slide_resources = newValue;
        } else {
          this.vueModel.slide_resource_ids = [];
          this.event.slide_resources = null;
        }
      }
    }
  },
  methods: {
    ...mapActions([
      "getTopics",
      "getPlaces",
      "getSpeakers",
      "getDefinitions",
      "getSlideResources",
      "getEvent",
      "postEvent",
      "putEvent",
      "postSlide"
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
      this.getEvent(id).then(() => {
        // console.log(this.event);
        this.title = this.event.title;
        this.desc = this.event.desc;
        this.eventDateTime = this.event.start_date
          ? {
              startDate: moment(
                `${this.event.start_date} ${this.event.start_time}`
              ),
              endDate: moment(`${this.event.end_date} ${this.event.end_time}`)
            }
          : null;
        this.vueModel.place_id = this.event.place_info.id;
        this.vueModel.topic_id = this.event.topic_id;
        this.vueModel.speaker_ids = this.event.speakers.map(s => s.id);
        this.vueModel.assistant_ids = this.event.assistants.map(s => s.id);
        this.vueModel.field_ids = this.event.fields;
        this.vueModel.slide_resource_ids = this.event.slide_resources.map(
          s => s.id
        );
        this.vueModel.apply = this.event.apply;
      });
    },
    addApply() {
      var now = moment().format("YYYY-MM-DD HH:mm");
      this.vueModel.apply.push({
        host: "",
        channel: null,
        type: null,
        applyDateTime: null,
        start_time: now,
        end_time: now,
        price: "",
        limit: "",
        url: ""
      });
      this.applySelected = this.vueModel.apply.length - 1;
    },
    deleteApply(index) {
      Vue.delete(this.vueModel.apply, index);
      this.$nextTick(function() {
        this.applySelected = 0;
      });
    },
    addNewSlide() {
      if (!this.newSlide.type) {
        alert("投影片 / 資源 類型 沒選");
      } else if (this.newSlide.type === "exist") {
        this.addExitSlide();
      } else if (!this.newSlide.title || !this.newSlide.url) {
        alert("新投影片 / 資源 標題 或 url 需填寫");
      } else {
        //add slide api
        const new_data = {
          data: {
            type: this.newSlide.type,
            title: this.newSlide.title,
            url: this.newSlide.url
          }
        };
        this.postSlide(new_data).then(() => {
          Vue.set(
            this.vueModel.slide_resource_ids,
            this.vueModel.slide_resource_ids.length,
            this.post_slide_result.id
          );
          // 新增的資源是第一筆資料
          this.slide_resources.unshift(this.post_slide_result);
        });
      }
    },
    addExitSlide() {
      if (this.newSlide.type === "exist" && !this.newSlide.selectedSlide) {
        alert("選擇已存在投影片 / 資源");
      } else {
        Vue.set(
          this.vueModel.slide_resource_ids,
          this.vueModel.slide_resource_ids.length,
          parseInt(this.newSlide.selectedSlide.id, 10)
        );
      }
    },
    deleteSlide(index) {
      Vue.delete(this.vueModel.slide_resource_ids, index);
    },
    applyChange(index, key, value) {
      Vue.set(this.vueModel.apply[index], key, value);
    },
    applyDataTimeChange(index, value) {
      const start_time = moment(value.startDate).format("YYYY-MM-DD HH:mm");
      const end_time = moment(value.endDate).format("YYYY-MM-DD HH:mm");

      Vue.set(this.vueModel.apply[index], "start_time", start_time);
      Vue.set(this.vueModel.apply[index], "end_time", end_time);
    },
    submit(e) {
      e.preventDefault();
      // check required data
      let hasError = false;
      if (!this.vueModel.title || this.vueModel.title.trim().length <= 0) {
        this.errors.title = true;
        hasError = true;
      }
      if (!this.vueModel.topic_id || this.vueModel.topic_id.length <= 0) {
        this.errors.topic = true;
        hasError = true;
      }
      if (!this.vueModel.field_ids || this.vueModel.field_ids.length <= 0) {
        this.errors.fields = true;
        hasError = true;
      }
      if (
        !this.vueModel.start_date ||
        !this.vueModel.start_time ||
        !this.vueModel.end_date ||
        !this.vueModel.end_time
      ) {
        this.errors.eventDateTime = true;
        hasError = true;
      }
      //call api
      if (hasError) {
        document.getElementById("basic_info").scrollIntoView();
      } else if (this.isEdit) {
        // submit data 編輯
        const submitData = JSON.parse(JSON.stringify(this.vueModel));
        this.putEvent({ data: submitData, id: this.$route.params.id }).then(
          () => {
            alert("編輯完成");
            this.$router.push("/event-edit/" + this.put_event_result.id);
            this.$nextTick(() => {
              window.location.reload();
            });
          }
        );
      } else {
        // 複製 變成新增一筆
        const submitData = JSON.parse(JSON.stringify(this.vueModel));
        this.postEvent(submitData).then(() => {
          alert("複製完成");
          this.$router.push("/event-edit/" + this.post_event_result.id);
          this.$nextTick(() => {
            window.location.reload();
          });
        });
      }
    },
    goCopy() {
      this.$router.push("/event-copy/" + this.id);
      this.$nextTick(() => {
        window.location.reload();
      });
    }
  }
};
</script>
