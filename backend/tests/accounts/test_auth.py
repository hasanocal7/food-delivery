import os

import jwt
from strawberry_django.test.client import TestClient
from tests.fixtures.account_fixtures import personal_account


def test_login(personal_account):
    mutation = """
        mutation login($email: String!, $password: String!){
            login(email: $email, password: $password){
              __typename
              ... on LoginError{
                message
              }
              ... on LoginSuccess{
                token
                user{
                  id
                  firstName
                  lastName
                  phoneNumber
                  addresses{
                    neighborhood
                    street
                    buildingNumber
                    district
                    city
                  }
                }
              }
            }
    }
    """
    client = TestClient("/graphql/")
    res = client.query(
        mutation, variables={"email": "test@test.com", "password": "test"}
    )
    assert res.errors is None
    assert res.data["login"]["__typename"] == "LoginSuccess"


def test_register(db):
    mutation = """
      mutation register($payload: AccountInput!){
       register(payload: $payload){
      	__typename
        ... on RegisterAccountError{
          message
        }
        ... on RegisterAccountSuccess{
          user{
            firstName
            lastName
          }
        }
      }
      }
    """
    client = TestClient("/graphql/")
    res = client.query(
        mutation,
        variables={
            "payload": {
                "firstName": "Test1",
                "lastName": "Test",
                "email": "test@test.com",
                "password": "test",
                "confirmPassword": "test",
                "accountType": "CUSTOMER",
            }
        },
    )
    assert res.errors is None
    assert res.data["register"]["__typename"] == "RegisterAccountSuccess"


def test_forgot_password(personal_account):
    mutation = """
        mutation{
      forgotPassword(email: "test@test.com"){
        __typename
        ... on ForgotPasswordError{
          message
        }
        ... on ForgotPasswordSuccess{
          success
        }
      }
    }
    """
    client = TestClient("/graphql/")
    res = client.query(mutation)
    assert res.errors is None
    assert res.data["forgotPassword"]["success"] == True


def test_reset_password(personal_account):
    mutation = """
    mutation reset_password($token: String!, $password: String!, $confirmPassword: String!){
      resetPassword(token: $token, password: $password, confirmPassword: $confirmPassword){
        __typename
        ... on ResetPasswordError{
          message
        }
        ... on ResetPasswordSuccess{
          success
        }
      }
    }
    """
    token = jwt.encode({"userId": personal_account.id}, key=os.environ["SECRET_KEY"])
    client = TestClient("/graphql/")
    res = client.query(
        mutation,
        variables={"token": token, "password": "test2", "confirmPassword": "test2"},
    )
    assert res.errors is None
    assert res.data["resetPassword"]["success"] == True
