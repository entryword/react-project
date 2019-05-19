<template>
  <section class="content">
    <div class="row center-block">
      <div class="col-md-12">
        <div class="box">
          <div class="box-header">
            <router-link tag="button" class="btn btn-primary" to="event-add">建立活動</router-link>
          </div>
          <!-- /.box-header -->
          <div class="box-body">
            <div class="dataTables_wrapper form-inline dt-bootstrap" id="events_wrapper">
              <div class="row">
                <div class="col-sm-6">
                  <div id="events_length" class="dataTables_length"></div>
                </div>
              </div>

              <div class="row">
                <div class="col-sm-12 table-responsive">
                  <table id="events" class="table table-bordered table-striped">
                    <thead>
                      <tr>
                        <th>編號</th>
                        <th>名稱</th>
                        <th>地點</th>
                        <th>時間</th>
                        <th>報名頁</th>
                        <th>講師</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="event in events" :key="event.id">
                        <td>
                          <!-- <a :href="'event-edit/' + event.id">{{event.id}}</a> -->
                          <router-link
                            tag="button"
                            class="btn btn-link"
                            :to="{name:'活動編輯',  params: {id: event.id}}"
                          >{{event.id}}</router-link>
                        </td>
                        <td>{{event.title}}</td>
                        <td>{{event.place.name}}</td>
                        <td>{{event.date}} ({{event.weekday}}) {{event.start_time}}-{{event.end_time}}</td>
                        <td>
                          <template v-if="event.event_apply_exist">V</template>
                          <template v-if="!event.event_apply_exist">X</template>
                        </td>
                        <td>
                          <template v-if="event.speaker_exist">V</template>
                          <template v-if="!event.speaker_exist">X</template>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <!-- /.box-body -->
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import $ from "jquery";
// Require needed datatables modules
require("datatables.net");
require("datatables.net-bs");
import store from "../../store";
import { mapState, mapActions } from "vuex";
export default {
  name: "EventList",
  store: store,
  created() {
    this.getData();
  },
  data: {
    function() {
      return {
        route_base: process.env.ROUTE_BASE
      };
    }
  },
  computed: {
    ...mapState(["events"])
    // events: function() {
    //   console.log(this.$store.state.events);
    //   return this.$store.state.events;
    // }
  },
  watch: {
    events: function(newEvents, oldEvents) {
      if (newEvents !== oldEvents) {
        this.$nextTick(() => {
          $("#events").DataTable();
        });
      }
    }
  },
  methods: {
    ...mapActions(["getEvents"]),
    getData() {
      this.getEvents();
    }
  }
};
</script>

<style>
/* Using the bootstrap style, but overriding the font to not draw in
   the Glyphicons Halflings font as an additional requirement for sorting icons.

   An alternative to the solution active below is to use the jquery style
   which uses images, but the color on the images does not match adminlte.

@import url('/static/js/plugins/datatables/jquery.dataTables.min.css');
*/

@import url("/cms/static/js/plugins/datatables/dataTables.bootstrap.css");

table.dataTable thead .sorting:after,
table.dataTable thead .sorting_asc:after,
table.dataTable thead .sorting_desc:after {
  font-family: "FontAwesome";
}

table.dataTable thead .sorting:after {
  content: "\f0dc";
}

table.dataTable thead .sorting_asc:after {
  content: "\f0dd";
}

table.dataTable thead .sorting_desc:after {
  content: "\f0de";
}
</style>
