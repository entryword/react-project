<template>
  <div>
    <form @submit="submit">
      <section class="content">
        <!-- Main row -->
        <!-- <pre>vueModel: {{vueModel}}</pre> -->
        <div class="row">
          <!-- 場地資訊編輯 -->
          <div class="col-lg-12">
            <div class="box" id="basic_info">
              <div class="box-header">
                <h3 class="box-title">場地資訊編輯</h3>
              </div>
              <div class="box-body">
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*名稱</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.title }">
                      <input
                        type="text"
                        class="form-control"
                        name="place_title"
                        placeholder="名稱(限150字)"
                        maxlength="150"
                        v-model="title"
                      >
                      <div v-if="errors.title" class="help-block">請填寫名稱</div>
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*地址</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.addr }">
                      <input
                        type="text"
                        class="form-control"
                        name="place_addr"
                        placeholder="地址"
                        v-model="addr"
                      >
                      <div v-if="errors.addr" class="help-block">請填寫地址</div>
                    </div>
                  </div>
                </div>
                <div>
                  路線指引
                  <trumbowyg
                    v-model="desc"
                    :config="editorConfig"
                    class="form-control"
                    name="content"
                  ></trumbowyg>
                </div>
              </div>
              <div class="box-footer">
                <button type="submit" class="btn btn-primary">儲存</button>
              </div>
            </div>
          </div>
          <!-- 場地資訊編輯 -->
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
import { RESOURCE_TYPE, APPLY_TYPE, CHANNEL_TYPE } from "../../config/constant";

import store from "../../store";
import { mapState, mapActions } from "vuex";

export default {
  name: "PlaceEdit",
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
      errors: {
        title: false,
        addr: false
      },
      vueModel: {
        title: null,
        addr: null,
        desc: null
      },
      editorConfig: {}
    };
  },
  computed: {
    ...mapState([
      "place",
      "put_place_result"
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
    addr: {
      get: function() {
        return this.vueModel.addr;
      },
      set: function(newValue) {
        this.errors.addr = false;
        this.vueModel.addr = newValue;
      }
    },
    desc: {
      get: function() {
        return this.vueModel.desc;
      },
      set: function(newValue) {
        this.vueModel.desc = newValue;
      }
    }
  },
  methods: {
    ...mapActions([
      "getPlace",
      "putPlace"
    ]),
    clearInput(vueModel) {
      vueModel = {};
    },
    getData(id) {
      this.getPlace(id).then(() => {
        // console.log(this.place);
        this.title = this.vueModel.title;
        this.addr = this.vueModel.addr;
        this.desc = this.vueModel.desc;
      });
    },
    submit(e) {
      e.preventDefault();
      // check required data
      let hasError = false;
      if (!this.vueModel.title || this.vueModel.title.trim().length <= 0) {
        this.errors.title = true;
        hasError = true;
      }
      if (!this.vueModel.addr || this.vueModel.addr.trim().length <= 0) {
        this.errors.addr = true;
        hasError = true;
      }

      //call api
      if (hasError) {
        document.getElementById("basic_info").scrollIntoView();
      } else {
        // submit data
        const submitData = { data: JSON.parse(JSON.stringify(this.vueModel)) };
        this.putPlace({ data: submitData, id: this.$route.params.id }).then(
          () => {
            this.$router.push("/place-list");
          }
        );
      }
    }
  }
};
</script>
