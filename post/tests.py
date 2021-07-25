import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse


from post.models import Post


class PostCreateAndListTest(APITestCase):
    url_login = reverse("token_obtain_pair")
    url_create = reverse("post:create")
    url_list = reverse("post:list")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_jwt_authentication()

    def test_jwt_authentication(self):
        response = self.client.post(self.url_login,data={"username":self.username,"password":self.password})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.token)


    def test_post_create(self):
        data = {
        "title": "sdfsf",
        "content": "dsfsdf",
        "image": ""
        }
        response = self.client.post(self.url_create,data)
        self.assertEqual(201,response.status_code)


    #giriş yapmadan post oluşturmaya çalışmak
    def test_post_create(self):
        self.client.credentials()
        data = {
            "title": "sdfsf",
            "content": "dsfsdf",
            "image": ""
        }
        response = self.client.post(self.url_create, data)
        self.assertEqual(401, response.status_code)


    #kendi yazdığımız postların listesi
    def test_lists_posts(self):
        self.test_post_create()
        response = self.client.get(self.url_list)
        self.assertTrue(json.loads(response.content)["count"] == Post.objects.filter(user=self.user.pk).count())




class PostUpdateDeleteTest(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.post = Post.objects.create(title="Başlık", content="içerik")
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="desdesdes", password=self.password)
        self.url=reverse("post:update",kwargs={"slug":self.post.slug})
        self.test_jwt_authentication()

    def test_jwt_authentication(self,username="muhammedtestuser",password="test123"):
        response = self.client.post(self.url_login, data={"username": username, "password": password})
        self.assertEqual(200, response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)


    def test_delete_post(self):
        response = self.client.delete(self.url)
        self.assertEqual(204, response.status_code)

    def test_delete_post_different_user(self):
        self.test_jwt_authentication("desdesdes")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)


    def test_update_post(self):
        data = {

            "title": "enesad",
            "content": "contensdt"

        }
        response = self.client.put(self.url,data)
        self.assertEqual(200,response.status_code)
        self.assertTrue(Post.objects.get(id = self.post.pk).content == data["content"])


    def test_update_post_different_user(self):
        self.test_jwt_authentication("desdesdes")
        data = {

            "title": "enesad",
            "content": "contensdt"

        }
        response = self.client.put(self.url,data)
        self.assertEqual(403,response.status_code)
        self.assertFalse(Post.objects.get(id = self.post.pk).content == data["content"])

        # giriş yapmadan link görülemez

    def test_post_update_Unauthorized(self):
        self.client.credentials()  # bu şekilde boş bir şekilde yazılırsa oturum kapatılır demek
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)
