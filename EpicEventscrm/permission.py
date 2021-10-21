def allowed_users(user, allowed_roles: list) -> bool:
    groups = [group.name for group in user.groups.all()]
    for roles in allowed_roles:
        if roles in groups:
            return True
    return False