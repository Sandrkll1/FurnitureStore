from database.models.user import Role
from database.services.CRUD import BaseCRUD


class RoleService(BaseCRUD):
    def __init__(self):
        super(RoleService, self).__init__(Role, Role.role_id.key)
