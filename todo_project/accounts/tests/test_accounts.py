import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        email='test@test.com',
        password='testpass123',
    )


@pytest.fixture
def token(client, user):
    response = client.post('/accounts/api/v1/auth/create/', {
        'email': 'test@test.com',
        'password': 'testpass123',
    })
    return response.data['access']


# تست ثبت‌نام
class TestRegister:
    def test_register_success(self, client, db):
        response = client.post('/accounts/api/v1/auth/register/', {
            'email': 'new@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        assert response.status_code == 201
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_register_password_mismatch(self, client, db):
        response = client.post('/accounts/api/v1/auth/register/', {
            'email': 'new@test.com',
            'password1': 'testpass123',
            'password2': 'wrongpass',
        })
        assert response.status_code == 400

    def test_register_duplicate_email(self, client, user, db):
        response = client.post('/accounts/api/v1/auth/register/', {
            'email': 'test@test.com',
            'password1': 'testpass123',
            'password2': 'testpass123',
        })
        assert response.status_code == 400


# تست JWT
class TestJWT:
    def test_jwt_create_success(self, client, user, db):
        response = client.post('/accounts/api/v1/auth/create/', {
            'email': 'test@test.com',
            'password': 'testpass123',
        })
        assert response.status_code == 200
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_jwt_create_wrong_password(self, client, user, db):
        response = client.post('/accounts/api/v1/auth/create/', {
            'email': 'test@test.com',
            'password': 'wrongpass',
        })
        assert response.status_code == 401


# تست تغییر پسورد
class TestChangePassword:
    def test_change_password_success(self, client, user, token, db):
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.put('/accounts/api/v1/change-password/', {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123',
        })
        assert response.status_code == 200

    def test_change_password_wrong_old(self, client, user, token, db):
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = client.put('/accounts/api/v1/change-password/', {
            'old_password': 'wrongpass',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123',
        })
        assert response.status_code == 400

    def test_change_password_unauthorized(self, client, db):
        response = client.put('/accounts/api/v1/change-password/', {
            'old_password': 'testpass123',
            'new_password': 'newpass123',
            'new_password_confirm': 'newpass123',
        })
        assert response.status_code == 401