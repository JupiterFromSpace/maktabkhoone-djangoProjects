import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from tasks.models import Task

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
def other_user(db):
    return User.objects.create_user(
        email='other@test.com',
        password='testpass123',
    )


@pytest.fixture
def token(client, user):
    response = client.post('/accounts/api/v1/auth/create/', {
        'email': 'test@test.com',
        'password': 'testpass123',
    })
    return response.data['access']


@pytest.fixture
def auth_client(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


@pytest.fixture
def task(db, user):
    return Task.objects.create(
        user=user,
        title='تسک تست',
        description='توضیحات تست',
    )


class TestTaskList:
    def test_list_success(self, auth_client, task, db):
        response = auth_client.get('/tasks/api/v1/tasks/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_list_unauthorized(self, client, db):
        response = client.get('/tasks/api/v1/tasks/')
        assert response.status_code == 401

    def test_list_only_own_tasks(self, auth_client, user, other_user, db):
        Task.objects.create(user=user, title='تسک من')
        Task.objects.create(user=other_user, title='تسک دیگری')
        response = auth_client.get('/tasks/api/v1/tasks/')
        assert len(response.data) == 1


class TestTaskCreate:
    def test_create_success(self, auth_client, db):
        response = auth_client.post('/tasks/api/v1/tasks/', {
            'title': 'تسک جدید',
            'description': 'توضیحات',
        })
        assert response.status_code == 201
        assert response.data['title'] == 'تسک جدید'

    def test_create_without_title(self, auth_client, db):
        response = auth_client.post('/tasks/api/v1/tasks/', {
            'description': 'توضیحات',
        })
        assert response.status_code == 400

    def test_create_unauthorized(self, client, db):
        response = client.post('/tasks/api/v1/tasks/', {
            'title': 'تسک جدید',
        })
        assert response.status_code == 401


class TestTaskDetail:
    def test_retrieve_success(self, auth_client, task, db):
        response = auth_client.get(f'/tasks/api/v1/tasks/{task.id}/')
        assert response.status_code == 200
        assert response.data['title'] == task.title

    def test_retrieve_other_user_task(self, auth_client, other_user, db):
        other_task = Task.objects.create(user=other_user, title='تسک دیگری')
        response = auth_client.get(f'/tasks/api/v1/tasks/{other_task.id}/')
        assert response.status_code == 404


class TestTaskUpdate:
    def test_update_success(self, auth_client, task, db):
        response = auth_client.put(f'/tasks/api/v1/tasks/{task.id}/', {
            'title': 'تسک ویرایش شده',
            'description': 'توضیحات جدید',
        })
        assert response.status_code == 200
        assert response.data['title'] == 'تسک ویرایش شده'

    def test_partial_update_success(self, auth_client, task, db):
        response = auth_client.patch(f'/tasks/api/v1/tasks/{task.id}/', {
            'is_done': True,
        })
        assert response.status_code == 200
        assert response.data['is_done'] is True

    def test_update_other_user_task(self, auth_client, other_user, db):
        other_task = Task.objects.create(user=other_user, title='تسک دیگری')
        response = auth_client.put(f'/tasks/api/v1/tasks/{other_task.id}/', {
            'title': 'هک',
        })
        assert response.status_code == 404


class TestTaskDelete:
    def test_delete_success(self, auth_client, task, db):
        response = auth_client.delete(f'/tasks/api/v1/tasks/{task.id}/')
        assert response.status_code == 204
        assert Task.objects.count() == 0

    def test_delete_other_user_task(self, auth_client, other_user, db):
        other_task = Task.objects.create(user=other_user, title='تسک دیگری')
        response = auth_client.delete(f'/tasks/api/v1/tasks/{other_task.id}/')
        assert response.status_code == 404