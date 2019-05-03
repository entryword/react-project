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
                <h3 class="box-title">活動內容新增</h3>
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
                      >
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
                    </div>
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
                <button type="submit" class="btn btn-primary pull-right">儲存</button>
              </div>
            </div>
          </div>
          <!-- 活動內容編輯 -->
        </div>
      </section>
    </form>
  </div>
</template>
<script>
import moment from "moment";
import Vue from "vue";
import vSelect from "vue-select";
import DateRangePicker from "vue2-daterange-picker";
import Trumbowyg from "vue-trumbowyg";
import { RESOURCE_TYPE, APPLY_TYPE } from "../../config/constant";

import store from "../../store";
import { mapState, mapActions } from "vuex";

export default {
  name: "EventAdd",
  filters: {
    date(value) {
      let options = { year: "numeric", month: "long", day: "numeric" };
      return Intl.DateTimeFormat("en-US", options).format(value);
    }
  },
  components: { "v-select": vSelect, DateRangePicker, Trumbowyg },
  created() {
    this.getData();
  },
  data: function() {
    return {
      errors: {
        title: false,
        topic: false,
        eventDateTime: false
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
        field_ids: []
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
      slideResourceOption: {}
    };
  },
  computed: {
    ...mapState([
      "topics",
      "places",
      "speakers",
      "fields",
      "slide_resources",
      "post_event_result"
    ]),
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
    placeOption: {
      get: function() {
        const default_place = {
          id: 37,
          name: "未定",
          addr: "未定",
          label: "37 未定"
        };

        if (this.vueModel.place_info && this.vueModel.place_info.id) {
          const place = this.places.filter(
            p => p.id === this.vueModel.place_info.id
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
        if (newValue) {
          this.vueModel.place_id = newValue.id;
        } else {
          this.vueModel.place_id = 37;
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
        if (newValue) {
          this.errors.topic = false;
          this.vueModel.topic_id = newValue.id;
        } else {
          this.vueModel.topic_id = null;
        }
      }
    },
    speakerOption: {
      get: function() {
        if (this.vueModel.speaker_ids.length > 0) {
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
        this.vueModel.speaker_ids = newValue.map(s => s.id);
      }
    },
    assistantOption: {
      get: function() {
        if (this.vueModel.assistant_ids.length > 0) {
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
        this.vueModel.assistant_ids = newValue.map(s => s.id);
      }
    },
    fieldOption: {
      get: function() {
        if (this.vueModel.field_ids.length > 0) {
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
        this.vueModel.field_ids = newValue.map(s => s.id);
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
      "postEvent"
    ]),
    clearInput(vueModel) {
      vueModel = {};
    },
    getData() {
      this.getTopics();
      this.getPlaces();
      this.getSpeakers();
      this.getDefinitions();
      this.getSlideResources();
    },
    submit(e) {
      e.preventDefault();
      let hasError = false;
      if (!this.vueModel.title || this.vueModel.title.trim().length <= 0) {
        this.errors.title = true;
        hasError = true;
      }
      if (!this.vueModel.topic_id || this.vueModel.topic_id.length <= 0) {
        this.errors.topic = true;
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
      if (hasError) {
        document.getElementById("basic_info").scrollIntoView();
      } else {
        // submit data
        const submitData = { data: JSON.parse(JSON.stringify(this.vueModel)) };
        this.postEvent(submitData).then(() => {
          this.$router.push("/event-list");
        });
      }
    }
  }
};
</script>

