<template>
  <div>
    <section class="content">
      <!-- Main row -->
      <div class="row">
        <!-- 活動內容編輯 -->
        <div class="col-lg-12">
          <div class="box">
            <div class="box-header">
              <h3 class="box-title">活動內容編輯</h3>
            </div>
            <div class="box-body">
              <form action="#" method="post">
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
                        value="Devops CI/CD"
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
                      <select class="form-control select2" style="width: 100%;">
                        <option>46 Python入門(週末密集充實版)</option>
                        <option selected="selected">47 業界常用工具與技術分享</option>
                        <option>45 Production TensorFlow</option>
                        <option>42 生活中的程式-Python自動化</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-2">
                    <font style="color:red">*活動時間</font>
                  </div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <div class="input-group">
                        <div class="input-group-addon">
                          <i class="fa fa-clock-o"></i>
                        </div>
                        <input type="text" class="form-control pull-right" id="event_time">
                      </div>
                      <!-- /.input group -->
                    </div>
                  </div>
                </div>

                <div class="row">
                  <div class="col-md-2">活動地點</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <select class="form-control select2" style="width: 100%;">
                        <option selected="selected">21 美國創新中心AIC</option>
                        <option>30 臺北市婦女館</option>
                        <option>39 AppWorks</option>
                      </select>
                    </div>
                  </div>
                </div>

                <div>
                  活動內容
                  <textarea
                    class="textarea"
                    placeholder="Message"
                    style="width: 100%; height: 125px; font-size: 14px; line-height: 18px; border: 1px solid #dddddd; padding: 10px;"
                  ></textarea>
                </div>

                <div class="row">
                  <div class="col-md-2">講師</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <select
                        class="form-control select2"
                        multiple="multiple"
                        data-placeholder="選擇講師"
                        style="width: 100%;"
                      >
                        <option>Mars</option>
                        <option>毛毛</option>
                        <option>柏憲</option>
                        <option>plum</option>
                      </select>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">助教</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <select
                        class="form-control select2"
                        multiple="multiple"
                        data-placeholder="選擇助教"
                        style="width: 100%;"
                      >
                        <option>龜珍</option>
                        <option>米卡</option>
                        <option>東曄</option>
                      </select>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-2">活動領域</div>
                  <div class="col-md-10">
                    <div class="form-group">
                      <select
                        class="form-control select2"
                        multiple="multiple"
                        data-placeholder="選擇領域"
                        style="width: 100%;"
                      >
                        <option>網頁爬蟲</option>
                        <option>業界分享</option>
                        <option>網站開發</option>
                        <option>資料科學</option>
                      </select>
                    </div>
                    <!-- /.form-group -->
                  </div>
                </div>
              </form>
            </div>
            <div class="box-footer">
              <button type="submit" class="btn btn-primary">儲存</button>
            </div>
          </div>
        </div>
        <!-- 活動內容編輯 -->

        <!-- 報名頁 -->
        <div class="col-lg-12">
          <div class="nav-tabs-custom">
            <ul class="nav nav-tabs">
              <li class="active">
                <a href="#tab_1" data-toggle="tab">報名方式1</a>
              </li>
              <li>
                <a href="#tab_2" data-toggle="tab">報名方式2</a>
              </li>
              <li class="pull-right">
                <a href="#" class="text-muted">
                  <i class="fa fa-plus-square"></i> 新增報名方式
                </a>
              </li>
            </ul>
            <div class="tab-content">
              <div class="tab-pane active" id="tab_1">
                <!--報名tab -->

                <form action="#" method="post">
                  <div class="row">
                    <div class="col-md-2">負責單位</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control"
                          name="sign_host"
                          placeholder="主辦單位(限150字)"
                          value="PyLadies Taiwan"
                        >
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名方式</div>
                    <div class="col-md-10">
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
                            一次報名整系列
                          </label>
                        </div>
                        <div class="radio">
                          <label>
                            <input
                              type="radio"
                              name="optionsRadios"
                              id="optionsRadios2"
                              value="option2"
                            >
                            每次分開報名
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
                          value="https://www.accupass.com/event/1902101412481181985260"
                        >
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">報名時間</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <div class="input-group">
                          <div class="input-group-addon">
                            <i class="fa fa-clock-o"></i>
                          </div>
                          <input type="text" class="form-control pull-right" id="signup_time">
                        </div>
                        <!-- /.input group -->
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
                          value="一般人400元，學生200元"
                        >
                      </div>
                    </div>
                  </div>
                  <div class="row">
                    <div class="col-md-2">!報名對象</div>
                    <div class="col-md-10">
                      <div class="form-group">
                        <input
                          type="text"
                          class="form-control"
                          name="signup_limit"
                          placeholder="報名對象"
                          value
                        >
                      </div>
                    </div>
                  </div>
                  <div>
                    !報名詳細說明：
                    <textarea
                      class="textarea"
                      placeholder="Message"
                      style="width: 100%; height: 125px; font-size: 14px; line-height: 18px; border: 1px solid #dddddd; padding: 10px;"
                    ></textarea>
                  </div>
                </form>
              </div>
              <button type="submit" class="btn btn-primary">儲存</button>
            </div>
            <!-- /.tab-pane -->
            <div class="tab-pane" id="tab_2"></div>
            <!-- /.tab-pane -->
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
                <tbody>
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
                  <tr>
                    <td>1.</td>
                    <td>
                      <a href>01-程式 與 Python 簡介</a>
                    </td>
                    <td>投影片</td>
                    <td>
                      <span class="badge bg-red">刪除</span>
                    </td>
                  </tr>
                  <tr>
                    <td>2.</td>
                    <td>
                      <a href>02-迴圈</a>
                    </td>
                    <td>投影片</td>
                    <td>
                      <span class="badge bg-red">刪除</span>
                    </td>
                  </tr>
                  <tr>
                    <td>3.</td>
                    <td>
                      <a href>03-Online Judge & 相關查詢資源</a>
                    </td>
                    <td>資源</td>
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
    </section>
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
              <label>
                <input type="radio" name="optionsRadios" id="optionsRadios2" value="option2">
                從已有投影片/資源選擇
                <select
                  class="form-control select2"
                  style="width: 100%;"
                >
                  <option>01-程式 與 Python 簡介</option>
                  <option selected="selected">02-迴圈</option>
                  <option>Anaconda 安裝</option>
                  <option>Unit Test in Python for Beginner</option>
                </select>
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
require("moment");

export default {
  name: "EventEdit",
  components: {},
  data: function() {
    return {
      styleObj: {}
    };
  },
  computed: {
    datetime() {
      return new Date();
    }
  },
  methods: {
    clearInput(vueModel) {
      vueModel = "";
    }
  }
};
</script>

<style>
.datetime-picker input {
  height: 4em !important;
}
</style>
