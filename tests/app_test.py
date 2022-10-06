"""The tests to run in this project.
To run the tests type,
$ nosetests --verbose
"""

from nose.tools import assert_true
import requests

BASE_URL = "http://localhost:3333"


class NewUUID():  # pylint: disable=too-few-public-methods
    """The new uuid created when creating a new book request.
    The NewUUID is used for further tests
    """

    value = None

    def __init__(self, value):
        self.value = value


def test_get_all_requests():
    "Test getting all requests"
    response = requests.get('%s/workshopfollowers' % (BASE_URL))
    assert_true(response.ok)


def test_get_individual_request():
    "Test getting an individual request"
    response = requests.get(
        '%s/workshopfollowers/8c36e86c-13b9-4102-a44f-646015dfd981' % (BASE_URL))
    assert_true(response.ok)


def test_get_individual_request_404():
    "Test getting a non existent request"
    response = requests.get('%s/workshopfollowers/an_incorrect_id' % (BASE_URL))
    assert_true(response.status_code == 404)


def test_add_new_record():
    "Test adding a new record"
    payload = {'name': 'Taiwoni Wegski', 'email': 'testuser3@test.com'}
    response = requests.post('%s/workshopfollowers' % (BASE_URL), json=payload)
    NewUUID.value = str(response.json()['id'])
    print(NewUUID.value)
    assert_true(response.status_code == 201)


def test_get_new_record():
    "Test getting the new record"
    url = '%s/workshopfollowers/%s' % (BASE_URL, NewUUID.value)
    response = requests.get(url)
    assert_true(response.ok)


def test_edit_new_record_title():
    "Test editing the new records title"
    payload = {'name': 'Taiwoni Wegski',
               'email': 'testuser3@test.com'}
    response = requests.put('%s/workshopfollowers/%s' %
                            (BASE_URL, NewUUID.value), json=payload)
    assert_true(response.json()['name'] == "Taiwoni Wegski")


def test_edit_new_record_email():
    "Test editing the new records email"
    payload = {'name': 'Taiwoni Wegski',
               'email': 'testuser4@test.com'}
    response = requests.put('%s/workshopfollowers/%s' %
                            (BASE_URL, NewUUID.value), json=payload)
    assert_true(response.json()['email'] == "testuser4@test.com")


def test_add_new_record_bad_email_format():
    "Test adding a new record with a bad email"
    payload = {'name': 'Taiwoni Wegski', 'email': 'badEmailFormat'}
    response = requests.post('%s/workshopfollowers' % (BASE_URL), json=payload)
    assert_true(response.status_code == 400)


def test_add_new_record_bad_title_key():
    "Test adding a new record with a bad title"
    payload = {'badNameKey': 'Taiwoni Wegski', 'email': 'testuser4@test.com'}
    response = requests.post('%s/workshopfollowers' % (BASE_URL), json=payload)
    assert_true(response.status_code == 400)


def test_add_new_record_no_email_key():
    "Test adding a new record no email"
    payload = {'name': 'Good & Bad Book'}
    response = requests.post('%s/workshopfollowers' % (BASE_URL), json=payload)
    assert_true(response.status_code == 400)


def test_add_new_record_no_title_key():
    "Test adding a new record no title"
    payload = {'email': 'testuser5@test.com'}
    response = requests.post('%s/workshopfollowers' % (BASE_URL), json=payload)
    assert_true(response.status_code == 400)

def test_add_new_record_no_payload():
    "Test adding a new record with no payload"
    payload = None
    response = requests.post('%s/workshopfollowers' % (BASE_URL), json=payload)
    assert_true(response.status_code == 400)


def test_delete_new_record():
    "Test deleting the new record"
    response = requests.delete('%s/workshopfollowers/%s' % (BASE_URL, NewUUID.value))
    assert_true(response.status_code == 204)


def test_delete_new_record_404():
    "Test deleting the new record that was already deleted"
    response = requests.delete('%s/workshopfollowers/%s' % (BASE_URL, NewUUID.value))
    assert_true(response.status_code == 404)
