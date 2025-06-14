def detectuser(user):
    if user.role == 1:
        user_url="vend_dashboard"
        return user_url
    elif user.role == 2:
        user_url="cust_dashboard"
        return user_url
    elif user.role == None and user.is_superadmin:
        user_url = "/admin"
        return user_url