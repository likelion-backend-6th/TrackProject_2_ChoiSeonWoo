from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from posts.models import Like, Post, Comment


@receiver([post_save, post_delete], sender=Like)
def update_like_count(sender, instance, **kwargs):
    content_type = instance.content_type
    object_id = instance.object_id

    if content_type.model == "post":
        post = Post.objects.get(id=object_id)
        post.like_count = post.likes.count()
        post.save()

    elif content_type.model == "comment":
        comment = Comment.objects.get(id=object_id)
        comment.like_count = comment.likes.count()
        comment.save()
