from datetime import datetime

from core.db_map import UsersTable, session_scope

values = ['2020', '12', '01', '00', '00', '00']
launch_date = datetime(*map(int, values))


def create_new_account(context, user):
    with session_scope() as session:
        data = UsersTable(id=user.id,
                          side=0)
        session.add(data)
        session.commit()


def calc_days():
    return (launch_date - datetime.now()).days
