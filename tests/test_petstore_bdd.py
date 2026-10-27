import pytest
import requests
from pytest_bdd import scenarios, given, when, then, parsers

scenarios("../features/petstore.feature")

@pytest.fixture
def api_session():
    return requests.Session()

# --- Pet Steps ---
@when(parsers.parse('I send a POST request to "/pet" with name "{name}" and status "{status}"'))
def step_add_pet(base_url, api_session, api_context, name, status):
    url = f"{base_url}/pet"
    payload = {
        "id": 999111,
        "name": name,
        "status": status
    }
    response = api_session.post(url, json=payload)
    api_context["response"] = response
    api_context["pet_id"] = response.json().get("id")

@then("the response status code should be 200")
def check_status_200(api_context):
    assert api_context["response"].status_code == 200

@then(parsers.parse('the response should contain pet name "{name}"'))
def check_pet_name(api_context, name):
    assert api_context["response"].json().get("name") == name

@given(parsers.parse('I have a created pet with name "{name}" and status "{status}"'))
def create_pet(base_url, api_session, api_context, name, status):
    url = f"{base_url}/pet"
    payload = {"id": 999222, "name": name, "status": status}
    response = api_session.post(url, json=payload)
    api_context["pet_id"] = response.json().get("id")

@when("I send a GET request to the pet endpoint")
def get_pet_by_id(base_url, api_session, api_context):
    pet_id = api_context["pet_id"]
    url = f"{base_url}/pet/{pet_id}"
    response = api_session.get(url)
    api_context["response"] = response

@then(parsers.parse('the response pet name should be "{name}"'))
def check_response_pet_name(api_context, name):
    assert api_context["response"].json().get("name") == name

@when(parsers.parse('I send a PUT request to update pet name to "{name}" and status "{status}"'))
def update_pet(base_url, api_session, api_context, name, status):
    url = f"{base_url}/pet"
    payload = {"id": api_context["pet_id"], "name": name, "status": status}
    response = api_session.put(url, json=payload)
    api_context["response"] = response

@when(parsers.parse('I send a GET request to "{endpoint}"'))
def get_request_generic(base_url, api_session, api_context, endpoint):
    url = f"{base_url}{endpoint}"
    response = api_session.get(url)
    api_context["response"] = response

@then("the response should be a list of pets")
def check_is_list(api_context):
    data = api_context["response"].json()
    assert isinstance(data, list)

@when("I send a DELETE request to remove the pet")
def delete_pet(base_url, api_session, api_context):
    pet_id = api_context["pet_id"]
    url = f"{base_url}/pet/{pet_id}"
    response = api_session.delete(url)
    api_context["response"] = response

# --- Store Steps ---
@when(parsers.parse('I send a POST request to "/store/order" with petId {pet_id:d} and quantity {qty:d}'))
def create_order(base_url, api_session, api_context, pet_id, qty):
    url = f"{base_url}/store/order"
    payload = {"id": 10, "petId": pet_id, "quantity": qty, "status": "placed"}
    response = api_session.post(url, json=payload)
    api_context["response"] = response
    api_context["order_id"] = response.json().get("id")

@then(parsers.parse('the response order status should be "{status}"'))
def check_order_status(api_context, status):
    assert api_context["response"].json().get("status") == status

@given(parsers.parse('I have placed an order for petId {pet_id:d}'))
def place_order_helper(base_url, api_session, api_context, pet_id):
    url = f"{base_url}/store/order"
    payload = {"id": 11, "petId": pet_id, "quantity": 1, "status": "placed"}
    response = api_session.post(url, json=payload)
    api_context["order_id"] = response.json().get("id")

@when("I send a GET request to the order endpoint")
def get_order(base_url, api_session, api_context):
    order_id = api_context["order_id"]
    url = f"{base_url}/store/order/{order_id}"
    response = api_session.get(url)
    api_context["response"] = response

@then("the order ID in response should match")
def check_order_id(api_context):
    assert api_context["response"].json().get("id") == api_context["order_id"]

@when("I send a DELETE request to remove the order")
def delete_order(base_url, api_session, api_context):
    order_id = api_context["order_id"]
    url = f"{base_url}/store/order/{order_id}"
    response = api_session.delete(url)
    api_context["response"] = response

# --- User Steps ---
@when(parsers.parse('I send a POST request to "/user" with username "{username}"'))
def create_user(base_url, api_session, api_context, username):
    url = f"{base_url}/user"
    payload = {"id": 1234, "username": username, "firstName": "Test", "lastName": "User", "email": "test@test.com", "password": "password123", "phone": "123456789"}
    response = api_session.post(url, json=payload)
    api_context["response"] = response

@given(parsers.parse('I have a registered user with username "{username}" and password "{password}"'))
def register_user_helper(base_url, api_session, api_context, username, password):
    url = f"{base_url}/user"
    payload = {"id": 5678, "username": username, "password": password}
    api_session.post(url, json=payload)

@when(parsers.parse('I send a GET request to login with username "{username}" and password "{password}"'))
def user_login(base_url, api_session, api_context, username, password):
    url = f"{base_url}/user/login?username={username}&password={password}"
    response = api_session.get(url)
    api_context["response"] = response

@then("the login message should contain session token")
def check_login_message(api_context):
    message = api_context["response"].json().get("message")
    assert message is not None and "logged in user session" in message