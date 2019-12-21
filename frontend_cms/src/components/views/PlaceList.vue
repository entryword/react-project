<template>
  <section class="content">
    <div class="row center-block">
      <div class="col-md-12">
        <div class="box">
          <div class="box-header">
            <router-link tag="button" class="btn btn-primary" to="place-add">建立場地</router-link>
          </div>
          <!-- /.box-header -->
          <div class="box-body">
            <div class="dataTables_wrapper form-inline dt-bootstrap" id="places_wrapper">
              <div class="row">
                <div class="col-sm-6">
                  <div id="places_length" class="dataTables_length"></div>
                </div>
              </div>

              <div class="row">
                <div class="col-sm-12 table-responsive">
                  <table id="places" class="table table-bordered table-striped">
                    <thead>
                      <tr>
                        <th>編號</th>
                        <th>名稱</th>
                        <th>地址</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="place in places" :key="place.id">
                        <td>
                          <!-- <a :href="'place-edit/' + place.id">{{place.id}}</a> -->
                          <router-link
                            tag="button"
                            class="btn btn-link"
                            :to="{name:'場地編輯',  params: {id: place.id}}"
                          >{{place.id}}</router-link>
                        </td>
                        <td>{{place.name}}</td>
                        <td>{{place.addr}}</td>
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
  name: "PlaceList",
  store: store,
  created() {
    this.getData();
  },
  computed: {
    ...mapState(["places"])
  },
  watch: {
    places: function(newPlaces, oldPlaces) {
      $("#places").css({ visibility: "hidden" });
      if (newPlaces !== oldPlaces) {
        this.$nextTick(() => {
          $("#places").DataTable({ order: [0, "desc"] });
          $("#places").css({ visibility: "visible" });
        });
      }
    }
  },
  methods: {
    ...mapActions(["getPlaces"]),
    getData() {
      this.getPlaces();
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
