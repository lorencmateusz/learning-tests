from unittest.mock import patch, Mock

import pytest

from item_db import ItemDB
from shopping_cart import ShoppingCart


@pytest.fixture
def cart():
    return ShoppingCart(4)


def mock_get_price(item: str):
    if item == 'pear':
        return 2
    if item == 'banana':
        return 3


def test_can_add_item_to_card(cart):
    cart.add('pear')

    assert cart.size() == 1


def test_when_item_added_then_cart_contains_item(cart):
    cart.add('raspberry')

    assert 'raspberry' in cart.get_items()


def test_when_more_than_max_size_should_fail(cart):
    [cart.add('pear') for x in range(4)]
    with pytest.raises(OverflowError):
        cart.add('pear')


def test_can_get_total_price(cart):
    cart.add('pear')
    cart.add('banana')

    price_map = {
        'pear': 2,
        'banana': 3
    }

    assert cart.get_total_price(price_map=price_map) == 5


def test_can_get_price_using_db(cart):
    cart.add('pear')
    cart.add('banana')

    item_db = ItemDB()
    item_db.get = Mock(side_effect=mock_get_price)

    assert cart.get_total_price(price_map=item_db) == 5

