Feature: Petstore API BDD Tests
  As a tester
  I want to test CRUD operations for pets, store orders, and users in Petstore API
  So that I can ensure the service works correctly

  Scenario: Add a new pet to the store
    When I send a POST request to "/pet" with name "Barsik" and status "available"
    Then the response status code should be 200
    And the response should contain pet name "Barsik"

  Scenario: Find pet by ID
    Given I have a created pet with name "Rex" and status "available"
    When I send a GET request to the pet endpoint
    Then the response status code should be 200
    And the response pet name should be "Rex"

  Scenario: Update an existing pet
    Given I have a created pet with name "Tuzik" and status "available"
    When I send a PUT request to update pet name to "Sharik" and status "sold"
    Then the response status code should be 200
    And the response pet name should be "Sharik"

  Scenario: Find pets by status
    When I send a GET request to "/pet/findByStatus?status=available"
    Then the response status code should be 200
    And the response should be a list of pets

  Scenario: Delete a pet
    Given I have a created pet with name "TempPet" and status "available"
    When I send a DELETE request to remove the pet
    Then the response status code should be 200

  Scenario: Place an order for a pet
    When I send a POST request to "/store/order" with petId 1 and quantity 2
    Then the response status code should be 200
    And the response order status should be "placed"

  Scenario: Find purchase order by ID
    Given I have placed an order for petId 1
    When I send a GET request to the order endpoint
    Then the response status code should be 200
    And the order ID in response should match

  Scenario: Delete an order by ID
    Given I have placed an order for petId 1
    When I send a DELETE request to remove the order
    Then the response status code should be 200

  Scenario: Create a new user
    When I send a POST request to "/user" with username "testuser123"
    Then the response status code should be 200

  Scenario: User login
    Given I have a registered user with username "testuser123" and password "password123"
    When I send a GET request to login with username "testuser123" and password "password123"
    Then the response status code should be 200
    And the login message should contain session token