import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse


#doğru veiriler ile kayıt işlemi yap
#şifre invalid olabilir
#kullanıcı adı kullanılmış olabilir
#üye girişi yaptıysak o sayfa gözüklmemeli
#token ile giriş işlemi yapılıydığında 403 hatası



class UserRegistirationTestCase(APITestCase):
    url = reverse("account:register")
    url_token = reverse("token_obtain_pair")

    def test_user_registiration(self):
        """
        doğru veiriler ile kayıt işlemi
        """
        data={
            "username":"muhammedtest",
            "password":"deneme123"
        }

        response = self.client.post(self.url,data)
        self.assertEqual(201,response.status_code)

    def test_user_invalid_password(self):
        """
        invalid password verisi ile kayıt işlemi
        """
        data={
            "username":"muhammedtest",
            "password":"1"
        }

        response = self.client.post(self.url,data)
        self.assertEqual(400,response.status_code)

    def test_unique_name(self):
        """
        invalid password verisi ile kayıt işlemi
        """
        self.test_user_registiration()

        data={
            "username":"muhammedtest",
            "password":"1ghmghmghmghmghm"
        }

        response = self.client.post(self.url,data)
        self.assertEqual(400,response.status_code)

    def test_user_authenticated_registration(self):
        """
        giriş yapmış kullanıcının kayıt oluşturma sayfasını görmesin
        """
        self.test_user_registiration()
        self.client.login(username="muhammedtest",password="deneme123")
        response = self.client.get(self.url)
        self.assertEqual(403, response.status_code)

    def test_user_authenticated_token_registration(self):
        """
        token ile giriş yapmış kullanıcının kayıt oluşturma sayfasını görmesin
        """
        self.test_user_registiration()
        data = {
            "username": "muhammedtest",
            "password": "deneme123"
        }
        response = self.client.post(self.url_token,data)
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+ token)
        response2 = self.client.get(self.url)
        self.assertEqual(403, response2.status_code)





class UserLoginTestCase(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.user = User.objects.create_user(username = self.username , password = self.password)

    def test_user_token(self):
        response = self.client.post(self.url_login, {"username":"muhammedtestuser","password":"test123"})
        self.assertEqual(200, response.status_code)
        #print(json.loads(response.content))
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        response = self.client.post(self.url_login, {"username": "yrty", "password": "test123"})
        self.assertEqual(401, response.status_code)


    def test_user_empty_data(self):
        response = self.client.post(self.url_login, {"username": "", "password": ""})
        self.assertEqual(400, response.status_code)





class UserPasswordChange(APITestCase):
    url = reverse("account:change-password")
    url_token = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.user = User.objects.create_user(username = self.username , password = self.password)

    def login_with_token(self):
        response = self.client.post(self.url_token, {"username":"muhammedtestuser","password":"test123"})
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

#oturum açılmadan giriş yapıldığında hata
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "old_password": "test123",
            "new_password": "45bnmgmkyukyuk"
        }
        response = self.client.put(self.url,data)
        self.assertEqual(204, response.status_code)

    def test_with_wrong_informations(self):
        self.login_with_token()
        data = {
            "old_password": "asfasfdg",
            "new_password": "45bnmgmkyukyuk"
        }
        response = self.client.put(self.url,data)
        self.assertEqual(400, response.status_code)




class UserProfileUpdate(APITestCase):
    url = reverse("account:me")
    url_token = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.user = User.objects.create_user(username = self.username , password = self.password)

    def login_with_token(self):
        response = self.client.post(self.url_token, {"username":"muhammedtestuser","password":"test123"})
        self.assertEqual(200, response.status_code)
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

#oturum açılmadan giriş yapıldığında hata
    def test_is_authenticated_user(self):
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

    def test_with_valid_informations(self):
        self.login_with_token()
        data = {
            "id": 1,
            "first_name": "Muhammed",
            "last_name": "Aydoğan",
            "profile": {
                "id": 1,
                "note": "heyo",
                "twitter": "sdf"
            }
        }
        response = self.client.put(self.url,data,format("json"))
        self.assertEqual(200, response.status_code)
        self.assertEqual(json.loads(response.content),data)
        #response.data demedik çünkü json formatında ise content demen gerek