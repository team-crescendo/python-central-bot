def get_uuid(db, user):
    _, data = db.rnf(f"SELECT uuid FROM discord WHERE discord_id='{user}';")

    if data:
        return data[0][0]

    else:
        return None

def get_point(db, user):
    if len(user) == 18:
        user = get_uuid(db, user)

    _, data = db.rnf(f"SELECT point FROM uuid WHERE uuid='{user}';")

    if data:
        return data[0][0]

    else:
        return None
