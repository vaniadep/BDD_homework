import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--url",
        action="store",
        default="https://petstore.swagger.io/v2",
        help="Base URL for Petstore API"
    )

@pytest.fixture
def base_url(request):
    return request.config.getoption("--url")

@pytest.fixture
def api_context():
    """Словарь для хранения состояния между шагами (ID питомцев, заказов и т.д.)"""
    return {}