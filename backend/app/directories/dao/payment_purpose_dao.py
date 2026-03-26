from common.base_dao import BaseDao
from app.directories.model.payment_purpose import PaymentPurpose

class PaymentPurposeDao(BaseDao[PaymentPurpose]):
    pass

payment_purpose_dao: PaymentPurposeDao = PaymentPurposeDao(PaymentPurpose)