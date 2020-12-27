import csv

from app.constant import TicketType, CheckInListStatus


class AccupassCsvProcessor:
    """
        處理Accupass輸出的csv報名表

        results = AccupassCsvProcessor(event_basic_sn, csv_file).get()
    """

    _allow_columns = {
        '狀態': 'status',
        '參加人姓名': 'name',
        '參加人Email': 'mail',
        '參加人電話': 'phone',
        '票券名稱': 'ticket_type',
        '票價(NT)': 'ticket_amount',
    }

    _allow_status = {
        '已付款'
    }

    _ticket_type_maps = {
        '一般人': TicketType.COMMON,
        '學生票': TicketType.STUDENT
    }

    def __init__(self, manager, event_basic_sn, stream):
        self.manager = manager
        self.event_basic_sn = event_basic_sn
        self.csv_reader = self._get_csv_reader(stream=stream)

        self.emails = list()
        self.user_ids = list()

        self.results = list()

        self._exec()

    @staticmethod
    def _get_csv_reader(stream):
        csv_reader = csv.DictReader(
            (line.replace('\0', '') for line in stream),
            quotechar=','
        )
        return csv_reader

    @staticmethod
    def _clear(_str):
        return _str.strip().strip('"').strip().strip('"')

    def _extract_row(self, row):
        temp = dict()
        for key, value in row.items():
            key = self._clear(key)
            value = self._clear(value)
            if key not in self._allow_columns:
                continue
            new_key = self._allow_columns[key]
            temp[new_key] = value or None
        return temp

    def _get_existed_user_dict(self, emails):
        """
            TODO 待User table設計好後加入
        """
        return {}
        # users = self.manager.get_users_by_emails(emails=emails)
        # return {user.mail: user.sn for user in users}

    def _convert_ticket_type(self, origin):
        if not origin or origin not in self._ticket_type_maps:
            return TicketType.OTHER
        return self._ticket_type_maps[origin]

    def _insert_new_user(self, email):
        """
            TODO 待User table設計好後加入
        """
        return None
        # info = dict(
        #     name=email,
        #     mail=email
        # )
        # user_sn = self.manager.create_user(info=info, flush=True)
        # return user_sn

    def _create_check_member(self, row, user_dict):
        email = row.get('mail')
        ticket_type = self._convert_ticket_type(origin=row.get('ticket_type'))
        ticket_amount = int(row.get('ticket_amount'))
        user_sn = user_dict[email] if email in user_dict else self._insert_new_user(email=email)
        info = dict(
            event_basic_sn=self.event_basic_sn,
            user_sn=user_sn,
            name=row.get('name'),
            mail=email,
            phone=row.get('phone'),
            ticket_type=ticket_type,
            ticket_amount=ticket_amount,
            remark=None,
            status=CheckInListStatus.NO_CHECK_IN
        )
        check_in_list_sn = self.manager.create_check_in_list(info=info, flush=True)
        schema = {
            'sn': check_in_list_sn,
            **info
        }
        return schema

    def _collect_row(self, csv_reader):
        temp = list()
        for row in csv_reader:
            row_dict = self._extract_row(row=row)
            if row_dict['status'] not in self._allow_status:
                continue
            temp.append(row_dict)
            self.emails.append(row_dict['email'])
        return temp

    def _exec(self):
        new_rows = self._collect_row(csv_reader=self.csv_reader)

        user_dict = self._get_existed_user_dict(emails=self.emails)
        for new_row in new_rows:
            data = self._create_check_member(row=new_row, user_dict=user_dict)
            self.results.append(data)

        self.manager.session.commit()

    def get(self):
        return self.results
