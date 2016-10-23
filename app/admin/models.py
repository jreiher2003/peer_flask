from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

class AdminPage(AdminIndexView):
    def is_accessible(self):
        return current_user.has_role('admin')

class UserAdmin(ModelView):
    column_exclude_list = list = ('password',)
    def is_accessible(self):
        return current_user.has_role('admin')