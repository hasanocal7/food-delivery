import pytest
from apps.accounts.models import Account


@pytest.fixture
def personal_account(db):
    return Account.objects.create_user(
        email="test@test.com",
        password="test",
        first_name="Test",
        last_name="Login",
        account_type="CUSTOMER",
        phone_number="5123456789",
    )
