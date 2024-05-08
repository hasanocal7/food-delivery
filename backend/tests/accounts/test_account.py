import os

import jwt
from strawberry_django.test.client import TestClient
from tests.fixtures.account_fixtures import personal_account


def test_create_address(personal_account):
    mutation = """
        mutation create_address($payload: AddressInput!){
          createAddress(payload: $payload){
            __typename
            ... on AddressError{
              message
            }
            ... on AddressSuccess{
              success
              address{
                neighborhood
                street
                buildingNumber
                district
                city
              }
            }
          }
        }
    """
    token = jwt.encode({"userId": personal_account.id}, key=os.environ["SECRET_KEY"])

    headers = {"Authorization": token}
    client = TestClient("/graphql/")
    res = client.query(
        mutation,
        variables={
            "payload": {
                "neighborhood": "Test",
                "street": "Test",
                "buildingNumber": "Test",
                "zipCode": "Test",
                "district": "Test",
                "city": "Test",
                "addressDetail": "TestTestTest",
            }
        },
        headers=headers,
    )
    assert res.errors is None
    assert res.data["createAddress"]["__typename"] == "AddressSuccess"


def test_update_user_info(personal_account):
    mutation = """
        mutation update_account_info($payload: AccountPartialInput!){
          updateAccountInfo(payload: $payload){
            __typename
            ... on UpdateAccountError{
              message
            }
            ... on UpdateAccountSuccess{
              id
              success
            }
          }
        }
    """
    token = jwt.encode({"userId": personal_account.id}, key=os.environ["SECRET_KEY"])

    headers = {"Authorization": token}
    client = TestClient("/graphql/")
    res = client.query(
        mutation,
        variables={
            "payload": {
                "firstName": "Test2",
                "lastName": "Test2",
                "phoneNumber": "5445454455",
            }
        },
        headers=headers,
    )
    assert res.errors is None
    assert res.data["updateAccountInfo"]["__typename"] == "UpdateAccountSuccess"
