<template>
  <div>
  <section class="content">
    <div class="row">
      <div class="col-lg-12">
        <div class="nav-tabs-custom">
          <ul class="nav nav-tabs">
            <li v-for="role in roles" :key="role.id" @click="onClickTab(role.id)" v-bind:class="{active: role.id === current}"><a>{{role.name}}</a></li>
            <li class="pull-right"><a class="text-muted" data-toggle="modal" data-target="#role_add"><i class="fa fa-plus-square"></i> 新增角色</a></li>
          </ul>
          <div class="tab-content">
            <div class="tab-pane active" v-if="current > -1">
              <form @submit="submitEditRole">
                <div class="row" v-for="permission in initPermissions" :key="permission.code">
                  <div class="col-md-2">{{permission.name}}</div>
                  <div class="col-md-10">
                    <div class="form-group permission-radio">
                      <label v-for="action in initActions" :key="action.code">
                        <input type="radio"
                               :checked="permissions.find((element) => element.code === permission.code && element.value === action.code)"
                               :value="action.code"
                               @change="onUpdatePermission(permission.code, $event.target.value)"> {{action.name}}
                      </label>
                    </div>
                  </div>
                </div>
                <button type="submit" class="btn btn-primary">儲存</button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
  <div id="role_add" class="modal fade" role="dialog" aria-hidden="true" style="display: none;">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <button type="button" class="close" data-dismiss="modal">×</button>
          <h4 class="modal-title">新增角色</h4>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <div class="radio">
              <label>
                <input type="radio" name="optionsRadios" id="optionsRadios1" value="option1" checked="">
                角色名稱
                <input type="text" class="form-control" name="signup_price" placeholder="角色名稱" v-model="vueModel.name">
              </label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-primary" @click="submitNewRole" data-dismiss="modal">儲存</button>
          <button type="button" class="btn btn-default" data-dismiss="modal">關閉</button>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>
<script>
  import store from "../../store";
  import { mapState, mapActions } from "vuex";

  export default {
    name: 'Role',
    store: store,
    created() {
      this.getData();
    },
    data () {
      return {
        initPermissions: [
          {code: 'EventList', name: '活動列表 EventList'},
          {code: 'Event', name: '活動內容 Event'},
          {code: 'EventRegister', name: '活動報名 EventRegister'},
          {code: 'SpeakerList', name: '講師列表 SpeakerList'},
          {code: 'Speaker', name: '講師說明 Speaker'},
          {code: 'PlaceList', name: '場地列表 PlaceList'},
          {code: 'Place', name: '場地說明 Place'},
          {code: 'UserList', name: '用戶列表 UserList'},
          {code: 'Role', name: '角色編輯 Role'}
        ],
        initActions: [
          {code: '0', name: 'No Access'},
          {code: '1', name: 'Read'},
          {code: '2', name: 'Write'}
        ],
        vueModel: {
          name: '',
          permissions: []
        },
        current: -1
      };
    },
    watch: {
      roles: function (newRoles, oldRoles) {
        if (this.current === -1 && newRoles.length > 0){
          this.onClickTab(newRoles[0].id);
        }
      }
    },
    computed: {
      ...mapState(["roles"]),
      permissions: {
        get: function() {
          return this.vueModel.permissions;
        },
        set: function(newValue) {
          this.vueModel.permissions = newValue;
        }
      }
    },
    methods: {
      ...mapActions([
        "getRoles",
        "putRole",
        "postRole"
      ]),
      onUpdatePermission(code, value) {
        let _permissions = this.vueModel.permissions;
        let _index = _permissions.findIndex((element) => element.code === code);

        if (_index > -1) {
          _permissions[_index].value = value;
          return _permissions;
        } else {
          return _permissions.push({code, value})
        }
      },
      onClickTab(id) {
        let _roles = JSON.parse(JSON.stringify(this.roles));
        let role = _roles.find((element) => element.id === id);
        this.current = role.id;
        this.vueModel.permissions = Object.keys(role.permission).map((key) => ({
          code: key,
          value: role.permissions[key]
        }));
      },
      getData() {
        this.getRoles();
      },
      submitEditRole(e) {
        e.preventDefault();
        let _roles = JSON.parse(JSON.stringify(this.roles));
        let role = _roles.find((element) => element.id === this.current);
        let permission = {};
        this.vueModel.permissions.map((e) => {
          permission[e.code] = e.value;
        });
        this.putRole({id: role.id, data: {name: role.name, permission: permission}}).then(
            () => {
              alert("更新完成");
              this.$nextTick(() => {
                window.location.reload();
              });
            }
        );
      },
      submitNewRole(e) {
        e.preventDefault();
        let hasError = false;
        if (this.vueModel.name === '') {
          alert("請輸入名稱");
          hasError = true;
          e.stopPropagation();
        }
        if (hasError) {} else {
          this.postRole({name: this.vueModel.name, permission: {}}).then(() => {
            alert("新增完成");
            this.$nextTick(() => {
              window.location.reload();
            });
          });
        }
      }
    }
  }
</script>
<style>
.permission-radio label {
  margin-right: 20px;
}
</style>
