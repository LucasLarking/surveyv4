from django.contrib.auth.models import User
from rest_framework import status
import pytest
from model_bakery import baker
from base.models import Survey
@pytest.fixture
def create_collection(api_client):
    def do_create_survey(survey):
        return api_client.post('/surveys/', survey)
    return do_create_survey


        

@pytest.mark.django_db
class TestCreateSurvey:
    def test_if_user_is_anonymous_returns_401(self, api_client, create_collection):
        responese = create_collection({'survey': 'a', 'description': 'b'})
        response = api_client.post('/surveys/',)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    

    def test_if_user_is_not_admin_returns_403(self, authenticate, api_client, create_collection):
        authenticate(is_staff=False)
        # response = api_client.post('/surveys/', {'survey': 'a', 'description': 'b'})
        response = create_collection({'survey': 'a', 'description': 'b'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_returns_400(self, authenticate, api_client, create_collection):
        authenticate(is_staff=True)
        # response = api_client.post('/surveys/', {'survey': '', 'description': 'b'})
        response = create_collection({'survey': '', 'description': 'b'})


        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_data_is_valid_returns_201(self, authenticate, api_client, create_collection):

        
        authenticate(is_staff=True)
        # response = api_client.post('/surveys/', {'survey': 'a', 'description': 'b'})
        response = create_collection({'survey': 'a', 'description': 'b'})


        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0


@pytest.mark.django_db
class TestRetrieveSurvey:
    def test_if_survey_exists_returns_200(self, api_client):
        obj = baker.make(Survey)

        response = api_client.get(f"/surveys/{obj.id}")
        assert response.status_code == status.HTTP__200_OK
        assert response.data['id'] == obj.id

        