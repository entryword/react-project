<template>
  <section class="content">
    <div class="row center-block">
      <div class="col-md-12">
        <div class="box">
          <div class="box-header">
            <router-link tag="button" class="btn btn-primary" to="/event-add">建立活動</router-link>
          </div>
          <!-- /.box-header -->
          <div class="box-body">
            <div class="dataTables_wrapper form-inline dt-bootstrap" id="example1_wrapper">
              <div class="row">
                <div class="col-sm-6">
                  <div id="example1_length" class="dataTables_length"></div>
                </div>
              </div>

              <div class="row">
                <div class="col-sm-12 table-responsive">
                  <table id="example1" class="table table-bordered table-striped">
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
                      <tr>
                        <td>
                          <a href="/event-edit" target="_blank">137</a>
                        </td>
                        <td>Python入門(週末密集充實版) 台北-01</td>
                        <td>AppWorks</td>
                        <td>2019-03-09 (六) 14:00-17:00</td>
                        <td>V</td>
                        <td>V</td>
                      </tr>
                      <tr>
                        <td>
                          <a href="/event-edit" target="_blank">138</a>
                        </td>
                        <td>Python入門(週末密集充實版) 台北-02</td>
                        <td>AppWorks</td>
                        <td>2019-03-10 (日) 14:00-17:00</td>
                        <td>V</td>
                        <td>V</td>
                      </tr>
                      <tr>
                        <td>
                          <a href="/event-edit" target="_blank">141</a>
                        </td>
                        <td>Python入門(週末密集充實版) 高雄-01</td>
                        <td>X</td>
                        <td>2019-04-27 (六) 14:00-17:00</td>
                        <td>X</td>
                        <td>V</td>
                      </tr>
                      <tr>
                        <td>
                          <a href="/event-edit" target="_blank">148</a>
                        </td>
                        <td>業界常用工具與技術分享 Devops CI/CD</td>
                        <td>美國創新中心AIC</td>
                        <td>2019-03-24 (日) 14:00-17:00</td>
                        <td>X</td>
                        <td>V</td>
                      </tr>
                      <tr>
                        <td>
                          <a href="/event-edit" target="_blank">149</a>
                        </td>
                        <td>業界常用工具與技術分享 Business Intelligence</td>
                        <td>美國創新中心AIC</td>
                        <td>2019-04-20 (六) 14:00-17:00</td>
                        <td>X</td>
                        <td>V</td>
                      </tr>
                      <tr>
                        <td>
                          <a href="/event-edit" target="_blank">150</a>
                        </td>
                        <td>業界常用工具與技術分享 Distributed Task Queue/Scheduler/Monitor</td>
                        <td>美國創新中心AIC</td>
                        <td>2019-05-26 (日) 13:00-17:00</td>
                        <td>X</td>
                        <td>V</td>
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

export default {
  name: "EventList",
  mounted() {
    this.$nextTick(() => {
      $("#example1").DataTable();
    });
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

@import url("/static/js/plugins/datatables/dataTables.bootstrap.css");

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
