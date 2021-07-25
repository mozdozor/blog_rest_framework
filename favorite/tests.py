import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

from favorite.models import Favourite
from post.models import Post


class FavouriteCreateList(APITestCase):
    url = reverse("favorite:list-create")
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.post = Post.objects.create(title="Başlık",content="içerik" )
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login,data={"username":self.username,"password":self.password})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.token)

    #favlama
    def test_add_favourite(self):
        data = {
            "content": "İçerik güzel favla",
            "user": self.user.pk,
            "post": self.post.pk
        }

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    #user favlarını kontrol etme
    def  test_user_favs(self):
        self.test_add_favourite()
        response = self.client.get(self.url)
     #   print(json.loads(response.content)["count"])               ya bu satırdaki gibi yada aşağıdaki saturdaki gibi kullanabilrsin
     #   print(len(json.loads(response.content)["results"]) )
        self.assertTrue(len(json.loads(response.content)["results"]) == Favourite.objects.filter(user = self.user).count())



class FavouriteUpdateDelete(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.post = Post.objects.create(title="Başlık", content="içerik")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="desdesdes", password=self.password)
        self.favourite=Favourite.objects.create(content="deneme",user=self.user,post=self.post)
        self.url=reverse("favorite:update",kwargs={"pk":self.favourite.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self,username="muhammedtestuser",password="test123"):
        response = self.client.post(self.url_login, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)


    def test_delete_fav(self):
        response = self.client.delete(self.url)
        self.assertEqual(204,response.status_code)


    #başkası benim yerime silememeli
    def test_delete_fav_different_user(self):
        self.test_jwt_authentication("desdesdes")
        response = self.client.delete(self.url)
        self.assertEqual(403,response.status_code)

    #düzenleme işlemi
    def test_fav_update(self):
        data = {
            "content":"xxxxx",
        }
        response = self.client.put(self.url,data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(Favourite.objects.get(id = self.favourite.pk).content == data["content"])

    #başkası bizim favımızı update etmesin
    def test_fav_update_different_user(self):
        self.test_jwt_authentication("desdesdes")
        data = {
            "content":"xxxxx",
            "user":self.user2.pk
        }
        response = self.client.put(self.url,data)
        self.assertEqual(403, response.status_code)
       # self.assertTrue(Favourite.objects.get(id = self.favourite.pk).content == data["content"])


    #giriş yapmadan link görülemez
    def test_fav_update_Unauthorized(self):
        self.client.credentials()   #bu şekilde boş bir şekilde yazılırsa oturum kapatılır demek
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)

