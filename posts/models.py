from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from common.models import CommonModel


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(CommonModel):
    class StatusChoices(models.IntegerChoices):
        DRAFT = 0
        PUBLISHED = 1

    title = models.TextField(verbose_name="제목", max_length=250)
    slug = models.SlugField(
        verbose_name="슬러그",
        max_length=250,
        unique=True,
        allow_unicode=True,
        unique_for_date="publish",
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="posts",
    )
    body = models.TextField(verbose_name="본문")
    status = models.IntegerField(
        verbose_name="게시상태", default=0, choices=StatusChoices.choices
    )
    publish = models.DateTimeField(default=timezone.now)

    tags = TaggableManager()

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def unique_slug_generator(self, new_slug=None):
        slug = slugify(self.title, allow_unicode=True)
        new_slug = slug
        numb = 1
        while Post.objects.filter(slug=new_slug).exists():
            new_slug = "{slug}-{num}".format(slug=slug, num=numb)
            numb += 1
        return new_slug

    def save(self, *args, **kwargs):
        self.slug = self.unique_slug_generator()
        super().save(*args, **kwargs)


class Comment(CommonModel):
    post = models.ForeignKey(
        Post, verbose_name="댓글", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        "users.User",
        verbose_name="작성자",
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField(verbose_name="본문")

    class Meta:
        verbose_name = "게시글"
        verbose_name_plural = "게시글 목록"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return f"{self.body[:10]}.." if len(self.body) > 10 else self.body
