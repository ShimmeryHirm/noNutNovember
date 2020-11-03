from core.db_map import UsersTable, session_scope


def create_new_account(context, user):
    with session_scope() as session:
        data = UsersTable(id=user.id,
                          side=0)
        session.add(data)
        session.commit()
