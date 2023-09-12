from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.response import Response

from posts.models import Post


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


class PostViewSetpViewTest(APITestCase):
    # Set up
    @classmethod
    def setUpTestData(cls):
        cls.test_model = Post
        cls.user_model = get_user_model()
        cls.test_url = reverse("post-list")
        cls.user01 = cls.user_model.objects.create_user(
            email="user01@test.com",
            fullname="User01",
            phone="010-1111-1111",
            password="1234",
        )
        cls.post01 = cls.test_model.objects.create(
            title="어제01",
            author=cls.user01,
            body="어제작성한글",
        )
        cls.post02 = cls.test_model.objects.create(
            title="오늘01",
            author=cls.user01,
            body="오늘작성한글",
        )
        cls.post03 = cls.test_model.objects.create(
            title="내일01",
            author=cls.user01,
            body="내일작성한글",
        )
        cls.post01.tags.add("어제", "날씨", "프로젝트", "평일")
        cls.post02.tags.add("오늘", "날씨", "휴식", "주말")
        cls.post03.tags.add("내일", "날씨", "프로젝트", "주말")

        cls.post_data = {
            "title": "새글",
            "author": cls.user01.id,
            "body": "새글 작성 완료",
        }

    def test_create_Data(self):
        client = APIClient()
        client.force_authenticate(user=self.user01)
        res: Response = client.post(self.test_url, self.post_data)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_model.objects.count(), 4)

    def test_list_all_data(self):
        res: Response = self.client.get(self.test_url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.test_model.objects.count(), 3)

    def test_list_filter_data(self):
        query_params = {"tags": "날씨,주말"}
        res: Response = self.client.get(self.test_url, data=query_params)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {post["id"] for post in res.data}, {self.post02.id, self.post03.id}
        )
