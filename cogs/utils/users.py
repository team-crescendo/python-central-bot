from discord import User

def get_uuid(db, user):
    if len(user) == 36:
        _, data = db.rnf(f"SELECT discord_id FROM discord WHERE uuid='{user}';")
        print(" Fetched using uuid ", user, ", and data as: ", data)

        if data:
            return data[0][0], user
    else:
        _, data = db.rnf(f"SELECT uuid FROM discord WHERE discord_id='{user}';")
        print(" Fetched using dsid ", user, ", and data as: ", data)

        if data:
            return user, data[0][0]

    return None, None

def get_point(db, user):
    if len(user) == 18:
        user, _ = get_uuid(db, user)

    _, data = db.rnf(f"SELECT point FROM uuid WHERE uuid='{user}';")

    if data:
        return data[0][0]

    else:
        return None

def parse_mention(user):
    print(user)
    if isinstance(user, User):
        user = user.id
    if user[:2] == "<@" and user[-1:] == ">":
        user = user[2:-1]

        if user[0] == "!":
            user = user[1:]

    return user
