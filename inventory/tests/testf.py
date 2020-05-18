from app import app
import unittest
import pytest

@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    testing_client = flask_app.test_client()
    c = flask_app.app_context()
    c.push()
    yield testing_client  
    c.pop()


def test_product_summary(test_client):
    '''
    test for product summary 
    '''
    resp = test_client.get('/')
    assert resp.status_code == 200
    assert b'Summary' in resp.data

def test_product_detail_get(test_client):
    '''
    get product detail on product id
    '''
    resp = test_client.get('/product')
    assert resp.status_code == 200
    assert b'Product Details' in resp.data


def test_bad_product_detail_post(test_client):
    '''
    test product without product details
    '''
    resp = test_client.post('/product')
    assert resp.status_code == 400

def test_product_details_post(test_client, capsys):
    '''
    Provide unique prod_name because product name should be unique.
    '''
    resp = test_client.post('/product',data=dict(prod_name='Test1',
                                          prod_quantity=3,
                                          prod_price=100,
                                          description="This is test"),
                                          follow_redirects=True)

    assert resp.status_code == 200
    captured = capsys.readouterr()
    assert 'Test1 added successfully\n' in captured.out


def test_product_details_with_delete(test_client):
    '''
    delete product using product id
    '''
    resp = test_client.get('/delete?prod_id=4', follow_redirects=True)
    assert resp.status_code == 200

def test__get_product_detail_on_id(test_client):
    '''
    get product detail using product id
    '''
    resp = test_client.get('/get_product_details_on_id?prod_id=9', follow_redirects=True)
    assert resp.status_code == 200

def test__edit_product_details(test_client):
    '''
    edit or modification of product details
    '''
    resp = test_client.post('/edit', 
    data=dict(prod_id=19,prod_name='cda',prod_quantity=3,prodss_price=130),
    follow_redirects=True)
    assert resp.status_code == 200



