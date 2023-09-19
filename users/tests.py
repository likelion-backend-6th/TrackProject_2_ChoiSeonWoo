from datetime import datetime
from unittest.mock import patch, MagicMock

from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.response import Response
from common.test import create_sample_image

from posts.models import Comment, Post
from users.models import Follow, Profile


class SignUpViewTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = get_user_model()
        cls.test_url = reverse("signup")
        cls.test_user = cls.test_model.objects.create_user(
            email="test@example.com",
            fullname="Test User",
            phone="01012345678",
            password="password",
        )
        cls.valid_user_data = {
            "email": "valid_user@test.com",
            "fullname": "Valid User",
            "phone": "01099999999",
            "password": "qwer1234!",
        }
        cls.invalid_user_data1 = {
            "email": "invalid_user1",
            "fullname": "Invalid User1",
            "phone": "01099999998",
            "password": "qwer1234!",
        }
        cls.invalid_user_data2 = {
            "email": "invalid_user2@test.com",
            "fullname": "",
            "phone": "01099999997",
            "password": "qwer1234!",
        }
        cls.invalid_user_data3 = {
            "email": "invalid_user3@test.com",
            "fullname": "Invalid User3",
            "phone": "01012345678",
            "password": "qwer1234!",
        }
        cls.invalid_user_data4 = {
            "email": "invalid_user4@test.com",
            "fullname": "Invalid User4",
            "phone": "01099999995",
            "password": "",
        }

    def test_signup_valid_data(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.valid_user_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_model.objects.count(), 2)

    def test_signup_invalid_email(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.invalid_user_data1)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_model.objects.count(), 1)

    def test_signup_invalid_fullname(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.invalid_user_data2)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_model.objects.count(), 1)

    def test_signup_invalid_phone(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.invalid_user_data3)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_model.objects.count(), 1)

    def test_signup_invalid_password(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.invalid_user_data4)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.test_model.objects.count(), 1)


class LoginViewTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = get_user_model()
        cls.test_url = reverse("login")
        cls.test_user = cls.test_model.objects.create_user(
            email="test@example.com",
            fullname="Test User",
            phone="01293845642",
            password="password",
        )
        cls.valid_user_data = {
            "email": "test@example.com",
            "password": "password",
        }
        cls.invalid_user_data = {
            "email": "test@example.com",
            "password": "invalid_password",
        }

    def test_login_valid_data(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.valid_user_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("access", res.data.get("token"))
        self.assertIn("refresh", res.data.get("token"))

    def test_login_invalid_password(self):
        client = APIClient()
        res: Response = client.post(self.test_url, self.invalid_user_data)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("token", res.data)


class UserViewSetTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = get_user_model()
        cls.admin_user = cls.test_model.objects.create(
            email="admin@example.com",
            fullname="Admin User",
            phone="01000000000",
            password="password",
            is_admin=True,
        )
        cls.user01 = cls.test_model.objects.create(
            email="user01@example.com",
            fullname="User01",
            phone="01111111111",
            password="password",
        )
        cls.user02 = cls.test_model.objects.create(
            email="user02@example.com",
            fullname="User02",
            phone="01222222222",
            password="password",
        )
        cls.user03 = cls.test_model.objects.create(
            email="user03@example.com",
            fullname="User03",
            phone="0133333333",
            password="password",
        )
        cls.user01_profile = Profile.objects.create(
            user=cls.user01, nickname="TestUser", birthday=datetime.now().date()
        )
        cls.follow01 = Follow.objects.create(
            user_from=cls.admin_user, user_to=cls.user01
        )
        cls.follow02 = Follow.objects.create(
            user_from=cls.admin_user, user_to=cls.user02
        )
        cls.follow03 = Follow.objects.create(
            user_from=cls.user03, user_to=cls.admin_user
        )
        cls.post01 = Post.objects.create(
            title="user01-post01",
            author=cls.user01,
            body="user01의 1번째 작성 글",
        )
        cls.post02 = Post.objects.create(
            title="user01-post02",
            author=cls.user01,
            body="user01의 2번째 작성 글",
        )
        cls.post03 = Post.objects.create(
            title="user02-post01",
            author=cls.user02,
            body="user02의 1번째 작성 글",
        )
        cls.comment01 = Comment.objects.create(
            post=cls.post02,
            author=cls.user01,
            body="user01의 post02에 대한 1번째 댓글",
        )
        cls.comment02 = Comment.objects.create(
            post=cls.post02,
            author=cls.user01,
            body="user01의 post02에 대한 2번째 댓글",
        )
        cls.comment03 = Comment.objects.create(
            post=cls.post01,
            author=cls.user02,
            body="user02의 post01에 대한 1번째 작성 글",
        )

        cls.user04_data = {
            "email": "user04@example.com",
            "fullname": "User04",
            "phone": "01344444444",
            "password": "password",
        }

        cls.user05_data = {
            "email": "user05@example.com",
            "fullname": "User04",
            "phone": "01000000000",
            "password": "password",
        }
        cls.user01_modifying_data = {
            "fullname": "User01",
            "phone": "01242339421",
            "password": "password",
        }

    def test_list_data(self):
        test_url = reverse("user-list")
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), self.test_model.objects.count())

    def test_list_with_filter(self):
        query_params = {"fullname": "Admin"}
        test_url = reverse("user-list")
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url, data=query_params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res.data),
            self.test_model.objects.filter(fullname__icontains="Admin").count(),
        )

    def test_retrieve_data(self):
        test_url = reverse("user-detail", args=[self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.user01.pk)

    def test_update_data(self):
        test_url = reverse("user-detail", args=[self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.put(test_url, self.user01_modifying_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("phone"), self.user01_modifying_data["phone"])

    def test_delete_data(self):
        test_url = reverse("user-detail", args=[self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.delete(test_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_model.objects.count(), 3)
        with self.assertRaises(self.test_model.DoesNotExist):
            self.test_model.objects.get(id=self.user01.pk)

    def test_post_follow(self):
        test_url = reverse("user-follow", args=[self.admin_user.pk, self.user03.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.post(test_url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 4)

    def test_post_unfollow(self):
        test_url = reverse("user-follow", args=[self.admin_user.pk, self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.post(test_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 2)

    def test_get_following(self):
        test_url = reverse("user-following", args=[self.admin_user.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Follow.objects.filter(user_from=self.admin_user).count(), len(res.data)
        )

    def test_get_follower(self):
        test_url = reverse("user-follower", args=[self.admin_user.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Follow.objects.filter(user_to=self.admin_user).count(), len(res.data)
        )

    def test_get_posts(self):
        test_url = reverse("user-posts", args=[self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_get_feed(self):
        test_url = reverse("user-feed", args=[self.admin_user.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_get_comments(self):
        test_url = reverse("user-comments", args=[self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)


class ProfileViewTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = Profile
        cls.user_model = get_user_model()
        cls.admin_user = cls.user_model.objects.create(
            email="admin@example.com",
            fullname="Admin User",
            phone="01000000000",
            password="password",
            is_admin=True,
        )
        cls.profile00 = cls.test_model.objects.create(
            user=cls.admin_user, nickname="AdminUser", birthday=datetime.now().date()
        )
        cls.user01 = cls.user_model.objects.create(
            email="user01@example.com",
            fullname="User01",
            phone="01000000001",
            password="password",
        )
        cls.profile01 = cls.test_model.objects.create(
            user=cls.user01, nickname="TestUser01", birthday=datetime.now().date()
        )
        cls.user02 = cls.user_model.objects.create(
            email="user02@example.com",
            fullname="User02",
            phone="01000000002",
            password="password",
        )
        cls.user02_profile_data = {
            "nickname": "TestUser02",
            "birthday": datetime.now().date(),
        }
        cls.profile01_modifying_data = {
            "nickname": "TestUser01_modified",
            "birthday": datetime.now().date(),
        }

    def test_get_data(self):
        test_url = reverse("user-profile", args=[self.admin_user.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("nickname"), self.profile00.nickname)

    @patch("common.utils.Image.s3_client")
    def test_post_data(self, s3_client: MagicMock):
        test_url = reverse("user-profile", args=[self.user02.pk])

        s3_client.upload_fileobj.return_value = None
        s3_client.put_object_acl.return_value = None

        client = APIClient()
        client.force_authenticate(user=self.admin_user)

        sample_image = create_sample_image()

        data = self.user02_profile_data
        data["user_id"] = self.user02.id
        data["image"] = sample_image
        res: Response = client.post(test_url, data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            res.data.get("nickname"), self.user02_profile_data.get("nickname")
        )

        s3_client.upload_fileobj.assert_called_once()
        s3_client.put_object_acl.assert_called_once()

    @patch("common.utils.Image.s3_client")
    def test_put_image(self, s3_client: MagicMock):
        test_url = reverse("user-profile", args=[self.user01.pk])

        s3_client.upload_fileobj.return_value = None
        s3_client.put_object_acl.return_value = None

        client = APIClient()
        client.force_authenticate(user=self.admin_user)

        sample_image = create_sample_image()

        data = {
            "user": self.user01.id,
            "nickname": "user01profile",
            "birthday": datetime.now().date(),
            "image": sample_image,
        }
        res = client.put(test_url, data=data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(
            res.data.get("image_url").startswith("https://kr.object.ncloudstorage.com")
        )

        s3_client.upload_fileobj.assert_called_once()
        s3_client.put_object_acl.assert_called_once()

    def test_delete_data(self):
        test_url = reverse("user-profile", args=[self.user01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.delete(test_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_model.objects.count(), 1)
        with self.assertRaises(self.test_model.DoesNotExist):
            self.test_model.objects.get(user_id=self.user01.pk)


class FollowListViewTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = Follow
        cls.user_model = get_user_model()
        cls.admin_user = cls.user_model.objects.create(
            email="admin@example.com",
            fullname="AdminUser",
            phone="01111111111",
            password="password",
            is_admin=True,
        )
        cls.user01 = cls.user_model.objects.create(
            email="user01@example.com",
            fullname="User01",
            phone="01111111112",
            password="password",
        )
        cls.user02 = cls.user_model.objects.create(
            email="user02@example.com",
            fullname="User02",
            phone="01222222223",
            password="password",
        )
        cls.user03 = cls.user_model.objects.create(
            email="user03@example.com",
            fullname="User03",
            phone="01333333334",
            password="password",
        )
        cls.follow01 = cls.test_model.objects.create(
            user_from=cls.admin_user, user_to=cls.user01
        )
        cls.follow02 = cls.test_model.objects.create(
            user_from=cls.admin_user, user_to=cls.user02
        )
        cls.follow03 = cls.test_model.objects.create(
            user_from=cls.user01, user_to=cls.user02
        )
        cls.follow04 = cls.test_model.objects.create(
            user_from=cls.user01, user_to=cls.admin_user
        )
        cls.follow05 = cls.test_model.objects.create(
            user_from=cls.user02, user_to=cls.user03
        )

    def test_list_data(self):
        test_url = reverse("user-follow-list")
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), self.test_model.objects.count())

    def test_list_with_filter(self):
        test_url = reverse("user-follow-list")
        query_params = {"user_from": self.admin_user.id}
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.get(test_url, data=query_params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res.data),
            self.test_model.objects.filter(user_from=self.admin_user).count(),
        )


class OtherUserRelatedViewTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = get_user_model()
        cls.user01 = cls.test_model.objects.create(
            email="user01@example.com",
            fullname="User01",
            phone="01111111111",
            password="password",
        )
        cls.user02 = cls.test_model.objects.create(
            email="user02@example.com",
            fullname="User02",
            phone="01222222222",
            password="password",
        )
        cls.user03 = cls.test_model.objects.create(
            email="user03@example.com",
            fullname="User03",
            phone="0133333333",
            password="password",
        )
        cls.user04 = cls.test_model.objects.create(
            email="user04@example.com",
            fullname="User04",
            phone="01222222223",
            password="password",
        )
        cls.user05 = cls.test_model.objects.create(
            email="user05@example.com",
            fullname="User05",
            phone="0133333335",
            password="password",
        )

        cls.user05_modifying_data = {
            "phone": "01333434343",
            "password": "password",
        }

        cls.profile01 = Profile.objects.create(
            user=cls.user01, nickname="UserProfile01", birthday=datetime.now().date()
        )
        cls.profile02 = Profile.objects.create(
            user=cls.user02, nickname="TestProfile02", birthday=datetime.now().date()
        )
        cls.profile03 = Profile.objects.create(
            user=cls.user03, nickname="UserProfile03", birthday=datetime.now().date()
        )
        cls.profile04 = Profile.objects.create(
            user=cls.user04, nickname="TestProfile04", birthday=datetime.now().date()
        )

        cls.profile05_data = {
            "nickname": "TestProfile05",
            "birthday": datetime.now().date(),
        }

        cls.profile04_modifying_data = {
            "nickname": "ModifiedTestProfile04",
            "birthday": datetime.now().date(),
        }

        cls.follow01 = Follow.objects.create(user_from=cls.user01, user_to=cls.user02)
        cls.follow02 = Follow.objects.create(user_from=cls.user01, user_to=cls.user03)
        cls.follow03 = Follow.objects.create(user_from=cls.user01, user_to=cls.user04)
        cls.follow04 = Follow.objects.create(user_from=cls.user02, user_to=cls.user01)
        cls.follow05 = Follow.objects.create(user_from=cls.user02, user_to=cls.user03)
        cls.follow06 = Follow.objects.create(user_from=cls.user03, user_to=cls.user05)

    def test_other_user_info_view(self):
        test_url = reverse("other_users")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res.data), self.test_model.objects.exclude(id=self.user01.id).count()
        )

    def test_my_info_view_get(self):
        test_url = reverse("my_info")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.user01.id)

    def test_my_info_view_patch(self):
        test_url = reverse("my_info")
        client = APIClient()
        client.force_authenticate(user=self.user05)
        res: Response = client.patch(test_url, self.user05_modifying_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("phone"), self.user05_modifying_data["phone"])

    def test_other_profile_view(self):
        test_url = reverse("other_profile")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res.data), Profile.objects.exclude(user=self.user01).count()
        )

    def test_my_profile_view_get(self):
        test_url = reverse("my_profile")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.user01.profile.id)

    def test_my_profile_view_post(self):
        test_url = reverse("my_profile")
        client = APIClient()
        client.force_authenticate(user=self.user05)
        res: Response = client.post(test_url, self.profile05_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(Profile.objects.count(), 5)

    def test_my_profile_view_patch(self):
        test_url = reverse("my_profile")
        client = APIClient()
        client.force_authenticate(user=self.user04)
        res: Response = client.patch(test_url, self.profile04_modifying_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data.get("nickname"), self.profile04_modifying_data["nickname"]
        )

    def test_my_follow_view_follow(self):
        test_url = reverse("my_follow", args=[self.user05.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.post(test_url)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Follow.objects.count(), 7)

    def test_my_follow_view_unfollow(self):
        test_url = reverse("my_follow", args=[self.user02.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.post(test_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Follow.objects.count(), 5)

    def test_my_following_view(self):
        test_url = reverse("my_following")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_my_follower_view(self):
        test_url = reverse("my_follower")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
