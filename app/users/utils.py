def is_moderator_or_admin(user):
    return user.is_superuser or user.is_staff or user.is_moderator
