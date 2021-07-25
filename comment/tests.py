import json
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse

from comment.models import Comment
from post.models import Post


class CommentCreateAndList(APITestCase):
    url_login = reverse("token_obtain_pair")
    url_create = reverse("comment:create")
    url_list = reverse("comment:list")

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

    def test_comment_create_valid(self):
        data ={
            "content":"denemeyorum",
            "user":self.user.pk,
            "post":self.post.pk,
            "parent":""
        }
        response = self.client.post(self.url_create,data)
        self.assertEqual(201,response.status_code)


    def test_comment_list(self):
        self.test_comment_create_valid()
        response = self.client.get(self.url_list,{"q": self.post.pk})
        self.assertTrue(response.data["count"] == Comment.objects.filter(post=self.post.pk).count())


class CommentUpdateDelete(APITestCase):
    url_login = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "muhammedtestuser"
        self.password = "test123"
        self.post = Post.objects.create(title="Başlık",content="içerik" )
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.user2 = User.objects.create_user(username="muhammedafha", password=self.password)
        self.comment = Comment.objects.create(content="dsgsg",post=self.post,user=self.user)
        self.url=reverse("comment:update",kwargs={"pk":self.comment.pk})
        self.test_jwt_authentication()

    def test_jwt_authentication(self,username="muhammedtestuser",password="test123"):
        response = self.client.post(self.url_login,data={"username":username,"password":password})
        self.assertEqual(200,response.status_code)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer "+self.token)



    #yorum silme testi 204 dönecek
    def test_delete_comment(self):
        response = self.client.delete(self.url)
        self.assertEqual(204,response.status_code)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())


    #kendimize ait olmayan yorumu silme testi
    def test_delete_comment_different_user(self):
        self.test_jwt_authentication("muhammedafha")
        response = self.client.delete(self.url)
        self.assertEqual(403, response.status_code)
        self.assertTrue(Comment.objects.get(pk=self.comment.pk))


    #update comment test of mine
    def test_update_comment(self):
        data={
            "content":"sjsgjğosıgn"
        }
        response = self.client.put(self.url,data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(Comment.objects.get(pk=self.comment.pk).content ,data["content"])


    # update comment test of mine
    def test_update_comment_different_user(self):
        self.test_jwt_authentication("muhammedafha")
        data = {
            "content": "sjsgjğosıgn"
        }
        response = self.client.put(self.url, data)
        self.assertEqual(403, response.status_code)
        self.assertNotEqual(Comment.objects.get(pk=self.comment.pk).content ,data["content"])


    def test_unauthorization(self):
        self.client.credentials()           #giriş çıkış işlemlerini sonlandırır
        response = self.client.get(self.url)
        self.assertEqual(401, response.status_code)