<template>
  <div>
    <form @submit="submit">
      <section class="content">
        <!-- Main row -->
        <!-- <pre>vueModel: {{vueModel}}</pre> -->
        <div class="row">
          <!-- 場地資訊編輯 -->
          <div class="col-lg-12">
            <div class="box" id="place_info">
              <div class="box-header">
                <h3 class="box-title">場地資訊新增</h3>
              </div>
              <div class="box-body">
                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*名稱</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group" v-bind:class="{ 'has-error': errors.name }">
                      <input
                        type="text"
                        class="form-control"
                        name="place_name"
                        placeholder="名稱(限150字，不得與已存在的名稱相同。)"
                        maxlength="150"
                        v-model="name"
                      >
                      <div v-if="errors.name" class="help-block">請填寫名稱</div>
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
                <div class="row">
                  <div class="col-md-2">
                    <font>地圖網址</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <input
                        type="text"
                        class="form-control"
                        name="place_map"
                        placeholder="地圖網址"
                        v-model="map"
                      >
                    </div>
                    <div style="font-size: 12px; color: rgb(170, 170, 170);">
                      有靜態頁的地點使用以下 url:
                      <br />美國創新中心 AIC: venue/aic.html
                      <br />臺北市婦女館: venue/tpewomen.html
                      <br />
                    </div>
                  </div>
                </div>
              </div>
              <div class="box-footer">
                <button type="submit" class="btn btn-primary">新增</button>
                <button @click="redirect" class="btn btn-warning">取消</button>
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
import Trumbowyg from "vue-trumbowyg";
import { RESOURCE_TYPE, APPLY_TYPE } from "../../config/constant";

import store from "../../store";
import { mapState, mapActions } from "vuex";

export default {
  name: "PlaceAdd",
  components: { Trumbowyg },
  data: function() {
    return {
      errors: {
        name: false,
        addr: false
      },
      vueModel: {
        name: null,
        addr: null,
        map: ""
      },
      editorConfig: {}
    };
  },
  computed: {
    ...mapState(["post_place_result"]),
    name: {
      get: function() {
        return this.vueModel.name;
      },
      set: function(newValue) {
        this.errors.name = false;
        this.vueModel.name = newValue;
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
    map: {
      get: function() {
        return this.vueModel.map;
      },
      set: function(newValue) {
        this.vueModel.map = newValue || "";
      }
    }
  },
  methods: {
    ...mapActions(["postPlace"]),
    clearInput(vueModel) {
      vueModel = {};
    },
    submit(e) {
      console.log("submit", e)
      e.preventDefault();
      // check required data
      let hasError = false;
      if (!this.vueModel.name || this.vueModel.name.trim().length <= 0) {
        this.errors.name = true;
        hasError = true;
      }
      if (!this.vueModel.addr || this.vueModel.addr.trim().length <= 0) {
        this.errors.addr = true;
        hasError = true;
      }

      //call api
      if (hasError) {
        document.getElementById("place_info").scrollIntoView();
      } else {
        // submit data
        const submitData = { data: JSON.parse(JSON.stringify(this.vueModel)) };
        console.log(submitData);
        this.postPlace(submitData).then(
          () => {
            this.$router.push("/place-list");
          }
        );
      }
    },
    redirect(e) {
      console.log("redirect", e)
      this.$router.push("/place-list");
    }
  }
};
</script>

