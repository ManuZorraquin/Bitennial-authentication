import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from authentication_app.models import User

# Creando un usuario
@pytest.mark.django_db    
def setUp(self):
    self.user_data = {
        'email': 'test@example.com',
        'password': 'TestPassword123',
        'first_name': 'Test',
        'last_name': 'User',
        'phone_number': '123456789',
        'birthdate': '01/01/2000',
    }
    self.user = User.objects.create_user(**self.user_data)


# REGISTER tests
    
# Test registro correto
@pytest.mark.django_db
def test_user_registration_view(self):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'NewUserPassword123',
        'password2': 'NewUserPassword123',
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': '1234567890',
        'birthdate': '02/02/2002',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn('id', response.data['data'])
    self.assertEqual(response.data['data']['email'], data['email'])
    self.assertEqual(response.data['data']['first_name'], data['first_name'])
    self.assertEqual(response.data['data']['last_name'], data['last_name'])
    self.assertEqual(response.data['data']['phone_number'], data['phone_number'])
    self.assertEqual(response.data['data']['birthdate'], data['birthdate'])
        
# Prueba de registro con un correo electrónico que ya existe
@pytest.mark.django_db
def test_user_registration_with_existing_email(self):
    url = reverse('register')
    data = {
        'email': 'test@example.com',  # Email ya existente
        'password': 'NewUserPassword123',
        'password2': 'NewUserPassword123',
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': '1234567890',
        'birthdate': '02/02/2002',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('email', response.data)
        
# Prueba de registro con una contraseña que no cumple con los requisitos del modelo de usuario (django validations)
@pytest.mark.django_db
def test_user_registration_with_django_invalid_password(self):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'a', # Contraseña muy corta
        'password2': 'a',
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': '1234567890',
        'birthdate': '02/02/2002',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('password', response.data)
    
# Prueba de registro con una contraseña que no coincide
@pytest.mark.django_db
def test_user_registration_with_different_passwords(self):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'NewUserPassword123',
        'password2': 'NewUserPassword321', # Contraseña diferente
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': '1234567890',
        'birthdate': '02/02/2002',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
# Prueba de registro con un numero de telefono inválido
@pytest.mark.django_db
def test_user_registration_with_invalid_phone_number(self):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'NewUserPassword123',
        'password2': 'NewUserPassword123',
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': 'invalid', # Tiene letras
        'birthdate': '02/02/2002',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
# Prueba de registro con una fecha de nacimiento inválida
@pytest.mark.django_db
def test_user_registration_with_invalid_birthdate(self):
    url = reverse('register')
    data = {
        'email': 'newuser@example.com',
        'password': 'NewUserPassword123',
        'password2': 'NewUserPassword123',
        'first_name': 'New',
        'last_name': 'User',
        'phone_number': '1234567890',
        'birthdate': 'invalid_date', # No es formato dd/mm/yyyy
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('birthdate', response.data)
        
        
# LOGIN tests    

# Login ok
@pytest.mark.django_db
def test_user_login_with_correct_credentials(self):
    url = reverse('login')
    data = {
        'email': 'test@example.com',
        'password': 'TestPassword123',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn('access_token', response.data['data'])
    self.assertIn('refresh_token', response.data['data'])

# Credenciales invalidas login
@pytest.mark.django_db
def test_user_login_with_incorrect_credentials(self):
    url = reverse('login')
    data = {
        'email': 'test@example.com',
        'password': 'IncorrectPassword',
    }

    response = self.client.post(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('message', response.data)
    self.assertEqual(response.data['message'], 'Incorrect email or password')
        
    
# VIEW PROFILE test token invalido

# Ver datos personales OK
@pytest.mark.django_db
def test_user_profile_view(self):
    url = reverse('profile')
    self.client.force_authenticate(user=self.user)
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Verifica las nuevas propiedades en el perfil del usuario
    self.assertEqual(response.data['email'], self.user_data['email'])
    self.assertEqual(response.data['first_name'], self.user_data['first_name'])
    self.assertEqual(response.data['last_name'], self.user_data['last_name'])
    self.assertEqual(response.data['phone_number'], self.user_data['phone_number'])
    self.assertEqual(response.data['birthdate'], self.user_data['birthdate'])

# Ver datos personales sin token
@pytest.mark.django_db    
def test_user_profile_without_token(self):
    url = reverse('profile')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    self.assertIn('not_authenticated', response.data['detail'].code)


# UPDATE PROFILE tests
        
# Proceso OK
@pytest.mark.django_db
def test_edit_profile_successfully(self):
    # Login para obtener token
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']

    # Set the authentication header with the obtained token
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('edit-profile')

    # Edit the profile
    updated_data = {
        'first_name': 'Updated',
        'last_name': 'User',
        'phone_number': '987654321',
        'birthdate': '02/02/2002',
    }
    response = self.client.patch(url, updated_data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['first_name'], updated_data['first_name'])
    self.assertEqual(response.data['last_name'], updated_data['last_name'])
    self.assertEqual(response.data['phone_number'], updated_data['phone_number'])
    self.assertEqual(response.data['birthdate'], updated_data['birthdate'])

# Sin cambios en los campos
@pytest.mark.django_db
def test_edit_profile_no_fields_to_update(self):
    # Login para obtener token
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']

    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('edit-profile')

    response = self.client.patch(url, {})
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertEqual(response.data['status'], 'success')
    self.assertEqual(response.data['message'], 'No fields to update. Please enter new values.')

# Datos invalidos
@pytest.mark.django_db
def test_edit_profile_invalid_data(self):
    # Login para obtener token
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']

    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('edit-profile')

    invalid_data = {
        'phone_number': 'invalid',  # Invalido, contiene letras
    }
    response = self.client.patch(url, invalid_data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
# CHANGE PASSWORD tests
    
# Proceso OK
@pytest.mark.django_db
def test_change_password_successfully(self):
    # Login para obtener token
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']
        
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('change-password')
        
    data = {
        "current_password": "TestPassword123",
        "new_password": "TestPassword321",
        "confirm_password": "TestPassword321"
    }
        
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

# Contraseña actual incorrecta
@pytest.mark.django_db
def test_change_password_incorrect_current(self):
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']
        
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('change-password')
        
    data = {
        "current_password": "TestPassword",
        "new_password": "TestPassword321",
        "confirm_password": "TestPassword321"
    }
        
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('Current', response.data['message'])
        
# Contraseñas nuevas no coinciden

@pytest.mark.django_db
def test_change_password_different_passwords(self):
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']
        
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('change-password')
        
    data = {
        "current_password": "TestPassword123",
        "new_password": "TestPassword321",
        "confirm_password": "TestPassword333"
    }
        
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertIn('do not match', response.data['message'])
        
# Contraseña nueva invalida
@pytest.mark.django_db
def test_change_password_different_passwords(self):
    url = reverse('login')
    login_data = {'email': 'test@example.com', 'password': 'TestPassword123'}
    response = self.client.post(url, login_data)
    token = response.data['data']['access_token']
        
    self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    url = reverse('change-password')
        
    data = {
        "current_password": "TestPassword123",
        "new_password": "TestPassword",
        "confirm_password": "TestPassword"
    }
        
    response = self.client.put(url, data)
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)