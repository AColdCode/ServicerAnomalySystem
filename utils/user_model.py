from PySide6.QtCore import Qt, QAbstractListModel, QModelIndex


class UserModel(QAbstractListModel):
    UsernameRole = Qt.UserRole + 1
    RoleRole = Qt.UserRole + 2
    CreatedAtRole = Qt.UserRole + 3
    IsActiveRole = Qt.UserRole + 4
    ParentAdmin = Qt.UserRole + 5

    def __init__(self, users=None):
        super().__init__()
        self._users = users or []

    def rowCount(self, parent=QModelIndex()):
        return len(self._users)

    def data(self, index, role):
        if not index.isValid():
            return None

        user = self._users[index.row()]

        if role == self.UsernameRole:
            return user.get("username", "")
        elif role == self.RoleRole:
            return user.get("role", "")
        elif role == self.CreatedAtRole:
            return user.get("created_at", "")
        elif role == self.IsActiveRole:
            return user.get("is_active", 0)
        elif role == self.ParentAdmin:
            return user.get("parent_admin", "")

        return None

    def roleNames(self):
        return {
            self.UsernameRole: b"username",
            self.RoleRole: b"role",
            self.CreatedAtRole: b"created_at",
            self.IsActiveRole: b"is_active",
            self.ParentAdmin: b"parent_admin"
        }

    def setUsers(self, users):
        self.beginResetModel()
        self._users = users
        self.endResetModel()
