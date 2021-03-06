import csv
import os

from app import create_app
from app.exceptions import OK, RECORD_IS_EXIST


class TestCheckInListApi:
    def setup(self):
        self.app = create_app('test')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.db.create_all()
        self.test_client = self.app.test_client()

    def teardown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()
        self.app_context.pop()

    def test_upload(self):
        event_basic_id = 100
        url = '/cms/api/check-in-list/upload/{event_basic_id}'.format(event_basic_id=event_basic_id)

        headers = {
            'Content-Type': 'multipart/form-data'
        }
        form_data = {'files': open('{path}/sample/accupass_user_list.csv'.format(path=os.path.dirname(os.path.realpath(__file__))), 'rb')}
        upload_res = self.test_client.post(url, headers=headers, data=form_data)

        assert upload_res.json['info']['code'] == OK.code

        get_url = '/cms/api/check-in-list/event/{event_basic_id}'.format(event_basic_id=event_basic_id)
        get_res = self.test_client.get(get_url)

        assert get_res.json['info']['code'] == OK.code

        with open('{path}/sample/accupass_user_list.csv'.format(path=os.path.dirname(os.path.realpath(__file__))), newline='') as f:
            have_title_rows = csv.reader(f)
            total_count = sum([1 for _ in have_title_rows]) - 1
            valid_data_count = total_count - 3  # three invalid records
            assert valid_data_count == len(get_res.json['data'])

    def test_duplicate_upload(self):
        event_basic_id = 100
        url = '/cms/api/check-in-list/upload/{event_basic_id}'.format(event_basic_id=event_basic_id)

        headers = {
            'Content-Type': 'multipart/form-data'
        }
        first_form_data = {'files': open('{path}/sample/accupass_user_list.csv'.format(path=os.path.dirname(os.path.realpath(__file__))), 'rb')}
        first_upload = self.test_client.post(url, headers=headers, data=first_form_data)
        assert first_upload.json['info']['code'] == OK.code

        second_form_data = {'files': open('{path}/sample/accupass_user_list.csv'.format(path=os.path.dirname(os.path.realpath(__file__))), 'rb')}
        second_upload = self.test_client.post(url, headers=headers, data=second_form_data)
        assert second_upload.json['info']['code'] == RECORD_IS_EXIST.code

    def test_create(self):
        event_basic_id = 100

        post_url = '/cms/api/check-in-list'.format(event_basic_id=event_basic_id)
        payload = {
            'event_basic_id': event_basic_id,
            'name': 'test1234',
            'mail': 'test1234@demo.com',
            'phone': '886911111111',
            'ticket_type': 1,
            'ticket_amount': 20,
            'remark': 'test1234',
            'status': 1
        }

        post_res = self.test_client.post(post_url, json=payload)
        assert post_res.json['info']['code'] == OK.code

        new_id = post_res.json['data']['id']

        get_url = '/cms/api/check-in-list/event/{event_basic_id}'.format(event_basic_id=event_basic_id)
        get_res = self.test_client.get(get_url)
        assert get_res.json['info']['code'] == OK.code

        create_success = False
        new_info = dict()
        for info in get_res.json['data']:
            if info['id'] == new_id:
                create_success = True
                new_info = info
                break

        new_info.pop('id', None)
        new_info.pop('user_id', None)
        assert new_info == payload
        assert create_success

        return new_id

    def test_update(self):
        check_in_list_id = self.test_create()

        event_basic_id = 100

        put_url = '/cms/api/check-in-list/{check_in_list_id}'.format(check_in_list_id=check_in_list_id)
        payload = {
            'name': 'test5566',
            'mail': 'test5566@demo.com',
            'phone': '886922222222',
            'ticket_type': 1,
            'ticket_amount': 20,
            'remark': 'test5566',
            'status': 1
        }

        put_res = self.test_client.put(put_url, json=payload)
        assert put_res.json['info']['code'] == OK.code
        assert put_res.json['data']['id'] == check_in_list_id

        get_url = '/cms/api/check-in-list/event/{event_basic_id}'.format(event_basic_id=event_basic_id)
        get_res = self.test_client.get(get_url)
        assert get_res.json['info']['code'] == OK.code

        data_is_exist = False
        for info in get_res.json['data']:
            if info['id'] != check_in_list_id:
                continue
            for k, v in payload.items():
                assert info[k] == v
            data_is_exist = True
            break

        assert data_is_exist

    def test_delete(self):
        check_in_list_id = self.test_create()

        event_basic_id = 100

        delete_url = '/cms/api/check-in-list/{check_in_list_id}'.format(check_in_list_id=check_in_list_id)

        delete_res = self.test_client.delete(delete_url)
        assert delete_res.json['info']['code'] == OK.code

        get_url = '/cms/api/check-in-list/event/{event_basic_id}'.format(event_basic_id=event_basic_id)
        get_res = self.test_client.get(get_url)
        assert get_res.json['info']['code'] == OK.code

        delete_success = True
        for info in get_res.json['data']:
            if info['id'] == check_in_list_id:
                delete_success = False
                break

        assert delete_success
