from app.sqldb.models import CheckInList, User, db


class TicketType:
    COMMON = 1  # 一般人
    STUDENT = 2  # 學生
    OTHER = 3  # 其他


class AccupassCsvProcessor:
    """
        TODO db query的部分要搬到api.py
        處理Accupass輸出的csv報名表

        results = AccupassCsvProcessor(event_basic_sn, csv_file).get()
    """

    _allow_columns = {
        '參加人姓名',
        '參加人Email',
        '參加人電話',
        '票券名稱',
        '票價(NT)',
    }

    _allow_status = {
        '已付款'
    }

    _ticket_type_maps = {
        '一般人': TicketType.COMMON,
        '學生票': TicketType.STUDENT
    }

    def __init__(self, event_basic_sn, csv_reader):
        self.event_basic_sn = event_basic_sn
        self.csv_reader = csv_reader
        self.results = list()

        self._exec()

    def _extract_row(self, row):
        for k, v in row.items():
            if k not in self._allow_columns:
                continue
            row[k] = v or None
        return row

    def _get_existed_user_dict(self, emails):
        users = User.query.filter(User.mail.in_(emails)).all()
        return {user.mail: user.sn for user in users}

    def _convert_ticket_type(self, origin):
        if not origin or origin not in self._ticket_type_maps:
            return TicketType.OTHER
        return self._ticket_type_maps[origin]

    def _insert_new_user(self, email):
        user = User(
            name=email,
            mail=email,
        )
        db.session.add(user)
        db.session.flush()
        return user.sn

    def _create_check_member(self, row, user_dict):
        email = row.get('參加人Email')
        ticket_type = self._convert_ticket_type(origin=row.get('票券名稱'))
        ticket_amount = int(row.get('票價(NT)'))
        user_sn = user_dict[email] if email in user_dict else self._insert_new_user(email=email)

        check_in_list = CheckInList(
            event_basic_sn=self.event_basic_sn,
            user_sn=user_sn,
            name=row.get('參加人姓名'),
            mail=email,
            phone=row.get('參加人電話'),
            ticket_type=ticket_type,
            ticket_amount=ticket_amount
        )
        db.session.add(check_in_list)
        db.session.flush()

        schema = {
            'sn': check_in_list.sn,
            'event_basic_sn': check_in_list.event_basic_sn,
            'user_sn': check_in_list.user_sn,
            'name': check_in_list.name,
            'mail': check_in_list.mail,
            'phone': check_in_list.phone,
            'ticket_type': check_in_list.ticket_type,
            'ticket_amount': check_in_list.ticket_amount,
            'remark': check_in_list.remark,
            'status': check_in_list.status,
        }
        return schema

    def _yield_row(self, csv_reader):
        for index, row in enumerate(csv_reader):
            if row['狀態'] in self._allow_status:
                yield index, row

    def _collect_emails(self, csv_reader):
        emails = set()
        for index, row in self._yield_row(csv_reader):
            row_dict = self._extract_row(row=row)
            emails.add(row_dict['參加人Email'])
        return emails

    def _exec(self):
        emails = self._collect_emails(csv_reader=self.csv_reader)
        user_dict = self._get_existed_user_dict(emails=emails)

        for index, row in self._yield_row(csv_reader=self.csv_reader):
            row_dict = self._extract_row(row=row)
            data = self._create_check_member(row=row_dict, user_dict=user_dict)
            self.results.append(data)

        db.session.commit()

        return self

    def get(self):
        return self.results
