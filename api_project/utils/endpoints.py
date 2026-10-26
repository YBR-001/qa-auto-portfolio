from enum import Enum

class Endpoints(str, Enum):
    PET = "/pet"
    PET_FIND_BY_STATUS = "/pet/findByStatus"
    STORE_ORDER = "/store/order"
    STORE_INVENTORY = "/store/inventory"
    USER = "/user"
    USER_LOGIN = "/user/login"
    USER_LOGOUT = "/user/logout"
    USER_CREATE_WITH_LIST = "/user/createWithList"
