from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.response import Response

from posts.models import Comment, Post


class PostModelTestCase(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = Post
        cls.user_model = get_user_model()
        cls.user = cls.user_model.objects.create_user(
            email="test@test.com",
            fullname="테스터",
            phone="010-1111-1111",
            password="1234",
        )
        cls.post = cls.test_model.objects.create(
            title="test post title",
            body="test post body",
            author=cls.user,
            status=Post.StatusChoices.DRAFT,
            publish=timezone.now(),
        )
        cls.post.tags.add("tag1", "tag2", "tag3")

    def test_save_method_for_slug(self):
        expected_result = "test-post-title"
        self.assertEqual(self.post.slug, expected_result)

    def test_save_method_for_tags(self):
        tag_list = list(self.post.tags.values_list("name", flat=True))
        expected_result = ["tag1", "tag2", "tag3"]
        self.assertEqual(tag_list, expected_result)


class PostTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = Post
        cls.user_model = get_user_model()
        cls.admin_user = cls.user_model.objects.create(
            email="admin@example.com",
            fullname="Admin User",
            phone="01000000000",
            password="password",
            is_admin=True,
        )
        cls.user01 = cls.user_model.objects.create(
            email="user01@example.com",
            fullname="User01",
            phone="01111111111",
            password="password",
        )
        cls.user02 = cls.user_model.objects.create(
            email="user02@example.com",
            fullname="User02",
            phone="01222222222",
            password="password",
        )

        cls.post01 = cls.test_model.objects.create(
            title="어제01",
            author=cls.admin_user,
            body="어제작성한글",
        )
        cls.post02 = cls.test_model.objects.create(
            title="오늘01",
            author=cls.admin_user,
            body="오늘작성한글",
        )
        cls.post03 = cls.test_model.objects.create(
            title="내일01",
            author=cls.admin_user,
            body="내일작성한글",
        )
        cls.post04 = cls.test_model.objects.create(
            title="어제11",
            author=cls.user01,
            body="어제작성한글",
        )
        cls.post05 = cls.test_model.objects.create(
            title="오늘11",
            author=cls.user01,
            body="오늘작성한글",
        )
        cls.post06 = cls.test_model.objects.create(
            title="내일11",
            author=cls.user01,
            body="내일작성한글",
        )
        cls.post07 = cls.test_model.objects.create(
            title="어제21",
            author=cls.user01,
            body="어제작성한글",
        )
        cls.post08 = cls.test_model.objects.create(
            title="오늘21",
            author=cls.user02,
            body="오늘작성한글",
        )
        cls.post09 = cls.test_model.objects.create(
            title="내일21",
            author=cls.user02,
            body="내일작성한글",
        )

        cls.post01.tags.add("어제", "날씨", "프로젝트", "평일")
        cls.post02.tags.add("오늘", "날씨", "휴식", "주말")
        cls.post03.tags.add("내일", "날씨", "프로젝트", "주말")
        cls.post04.tags.add("어제", "날씨", "프로젝트", "평일")
        cls.post05.tags.add("오늘", "날씨", "휴식", "주말")
        cls.post06.tags.add("내일", "날씨", "프로젝트", "주말")
        cls.post07.tags.add("어제", "날씨", "프로젝트", "평일")
        cls.post08.tags.add("오늘", "날씨", "휴식", "주말")
        cls.post09.tags.add("내일", "날씨", "프로젝트", "주말")

        cls.post_data = {
            "title": "새글",
            "author": cls.user01.id,
            "body": "새글 작성 완료",
        }

        cls.post01_modifying_data = {
            "title": "수정된 글",
            "author": cls.user01.id,
            "body": "새글 수정 완료",
        }

        cls.user01_post_data = {
            "title": "새글",
            "body": "새글 작성 완료",
        }

        cls.user_02_post09_modifying_data = {
            "title": "수정된 글",
            "body": "새글 수정 완료",
        }

        cls.comment01 = Comment.objects.create(
            post=cls.post01, author=cls.user01, body="user01의 첫 번째 댓글"
        )
        cls.comment02 = Comment.objects.create(
            post=cls.post06, author=cls.user01, body="user01의 두 번째 댓글"
        )
        cls.comment03 = Comment.objects.create(
            post=cls.post09, author=cls.user01, body="user01의 세 번째 댓글"
        )
        cls.comment04 = Comment.objects.create(
            post=cls.post05, author=cls.user02, body="user02의 첫 번째 댓글"
        )
        cls.comment05 = Comment.objects.create(
            post=cls.post01, author=cls.user02, body="user02의 두 번째 댓글"
        )
        cls.comment06 = Comment.objects.create(
            post=cls.post08, author=cls.admin_user, body="admin_user의 첫 번째 댓글"
        )

        cls.comment_data = {
            "author": 2,
            "body": "새댓글 작성 완료",
        }

        cls.comment01_modifying_data = {
            "author": 2,
            "body": "댓글 수정 완료",
        }

    def test_post_list_data(self):
        test_url = reverse("post-list")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), self.test_model.objects.count())

    def test_post_list_with_filter(self):
        test_url = reverse("post-list")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        query_params = {"tags": "오늘,휴식"}
        res: Response = client.get(test_url, data=query_params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_post_create_data(self):
        test_url = reverse("post-list")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.post(test_url, self.post_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_model.objects.count(), 10)

    def test_post_retrieve_data(self):
        test_url = reverse("post-detail", args=[self.post01.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.post01.pk)

    def test_post_partial_update_data(self):
        test_url = reverse("post-detail", args=[self.post01.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.patch(test_url, self.post01_modifying_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("title"), self.post01_modifying_data["title"])

    def test_post_delete_data(self):
        test_url = reverse("post-detail", args=[self.post01.pk])
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.delete(test_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.test_model.objects.count(), 8)
        with self.assertRaises(self.test_model.DoesNotExist):
            self.test_model.objects.get(id=self.post01.pk)

    def test_comment_list_data(self):
        test_url = reverse("post-comments-list", args=[self.post01.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res.data), Comment.objects.filter(post_id=self.post01.pk).count()
        )

    def test_comment_list_with_filter(self):
        test_url = reverse("post-comments-list", args=[self.post01.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        query_params = {"body": "첫 번째"}
        res: Response = client.get(test_url, data=query_params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(res.data),
            Comment.objects.filter(
                post_id=self.post01.pk, body__icontains="첫 번째"
            ).count(),
        )

    def test_comment_create_data(self):
        test_url = reverse("post-comments-list", args=[self.post01.pk])
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.post(test_url, self.comment_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(post_id=self.post01.pk).count(), 3)

    def test_comment_retrieve_data(self):
        test_url = reverse(
            "post-comments-detail", args=[self.post01.pk, self.comment01.pk]
        )
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("id"), self.comment01.pk)

    def test_comment_partial_update_data(self):
        test_url = reverse(
            "post-comments-detail", args=[self.post01.pk, self.comment01.pk]
        )
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.patch(test_url, self.comment01_modifying_data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("body"), self.comment01_modifying_data["body"])

    def test_comment_delete_data(self):
        test_url = reverse(
            "post-comments-detail", args=[self.post01.pk, self.comment01.pk]
        )
        client = APIClient()
        client.force_authenticate(user=self.admin_user)
        res: Response = client.delete(test_url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 5)
        with self.assertRaises(self.test_model.DoesNotExist):
            self.test_model.objects.get(id=self.comment01.pk)

    def test_other_post_list(self):
        test_url = reverse("other_posts_list")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 5)

    def test_my_post_list(self):
        test_url = reverse("my_posts_list")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 4)

    def test_my_comment_list(self):
        test_url = reverse("my_comments_list")
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.get(test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)
