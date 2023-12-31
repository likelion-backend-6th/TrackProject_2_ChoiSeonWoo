# Generated by Django 4.2.5 on 2023-09-16 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("posts", "0006_alter_comment_author_alter_post_author"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="comment",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "댓글",
                "verbose_name_plural": "댓글 목록",
            },
        ),
        migrations.AlterField(
            model_name="comment",
            name="post",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="comments",
                to="posts.post",
                verbose_name="게시글",
            ),
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.TextField(max_length=50, verbose_name="제목")),
                (
                    "image_url",
                    models.URLField(blank=True, null=True, verbose_name="이미지"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="활성 여부")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="생성일"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="작성자",
                    ),
                ),
                (
                    "post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="posts.post",
                        verbose_name="게시글",
                    ),
                ),
            ],
            options={
                "verbose_name": "이미지",
                "verbose_name_plural": "이미지 목록",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(
                        fields=["-created_at"], name="posts_image_created_fe2c50_idx"
                    )
                ],
            },
        ),
    ]
