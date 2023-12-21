from enum import Enum


class PaymentType(str, Enum):
    PRODUCT = "product"
    DIGITAL_PRODUCT = "digital_product"
    SUBSCRIPTION = "subscription"
    SERVICE = "service"
