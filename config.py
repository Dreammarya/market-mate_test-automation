#URLS
BASE_URL = "https://grocerymate.masterschool.com"
AUTH_URL = f"{BASE_URL}/auth"
STORE_URL = f"{BASE_URL}/store"
CHECKOUT_URL = f"{BASE_URL}/checkout"
CART_URL = f"{BASE_URL}/cart"

# Timeouts
DEFAULT_TIMEOUT = 10
SHORT_TIMEOUT = 3
LONG_TIMEOUT = 20  

# Test checkout infos
TEST_CHECKOUT_DATA = {
    "street": "Test str. 1",
    "city": "Test",
    "postcode": "12323",
    "card_number": "1111111111111111",
    "card_name": "Maria Lazar",
    "card_expiry": "12/2032",
    "card_cvc": "123"
}

# Test login credentials
TEST_USER_CREDENTIALS = {
    "email": "maria3@gmail.com",
    "password": "maria3"
}

# Test date of birth
TEST_DOB = "01-01-2005"

INVALID_DOB = "32-12-2005"

#items
TEST_PRODUCTS = {
    "rating_product": "Ginger",
    "shipping_product": "Ginger",
    "cheap_product": "Kale"

}

#
SHIPPING_COST_EXPECTED = {
    "below_30": "8.00 €",
    "equal_30": "0.00 €",
    "above_30": "0.00 €"
}

