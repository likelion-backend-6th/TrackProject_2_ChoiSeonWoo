from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from common.models import CommonModel


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(CommonModel, models.Model):
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
        on_delete=models.SET_NULL,
        null=True,
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

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)
