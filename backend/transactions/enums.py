from django_enumfield import enum


class TransactionTypes(enum.Enum):
    INTERNAL = 0
    EXTERNAL = 1
    FEE = 2


class AccountStatuses(enum.Enum):
    ACTIVE = 0
    SUSPENDED = 1
    BLOCKED = 2


class Currencies(enum.Enum):
    USD = 0
    EUR = 1
    CNY = 2
