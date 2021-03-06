import uuid
import pytest
from django.urls import reverse
from django.core.management import call_command
from rest_framework.authtoken.models import Token

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()

@pytest.fixture
def test_password():
   return 'strong-test-pass'

@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests/test_data.json')

@pytest.fixture
def get_or_create_token(db, create_user):
   user = create_user()
   token, _ = Token.objects.get_or_create(user=user)
   return token
   
# Test for 401 Unauthorized Error when no Token is not present
@pytest.mark.django_db
def test_unauthed_request(api_client):
   url = reverse('Random')
   response = api_client.get(url)
   assert response.status_code == 401

# Test that Random gets some data and returns properly
@pytest.mark.django_db
def test_random_request(api_client, get_or_create_token):
   url = reverse('Random')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   assert len(response.data) == 9

# Test that CardSet gets 10 Cards
@pytest.mark.django_db
def test_cardset_request(api_client, get_or_create_token):
   url = reverse('CardSet')
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get(url)
   assert response.status_code == 200
   assert len(response.data) == 10
   
# Test that Card/[id] gets the correct stuff
@pytest.mark.django_db
def test_specific_card_request(api_client, get_or_create_token):
   should_be = {'id': 2, 'uuid': '11356037-c8d8-4217-83d9-3703aea6ead7', 'card_name': 'Envoy', 'set_num': 0, 'set_name': 'Promo', 'type': 'Action', 'is_kingdom_card': True, 'cost': '$4', 'card_text': 'Reveal the top 5 cards of your deck. The player to your left chooses one for you to discard. Draw the rest.'}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.get('/cards/2/')
   print(response.data)
   assert response.status_code == 200
   assert len(response.data) == 9
   assert response.data == should_be

# Test that POST card works
@pytest.mark.django_db
def test_card_creation(api_client, get_or_create_token):
   new_card = { 'uuid': '82f9bcc1-9ab9-4856-b04f-aace09668e21', 'card_name': 'New Card', 'set_num': 0, 'set_name': 'Promo', 'type': 'Action', 'cost': '$3', 'card_text': 'Sample Card Text'}
   token = get_or_create_token
   api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
   response = api_client.post('/cards/')
   print(response.data)
   assert response.status_code == 201
   assert len(response.data) == 9