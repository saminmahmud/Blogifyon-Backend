from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    post_image_url = models.ImageField(upload_to='post_cover_images/')
    title = models.CharField(max_length=255)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post')
    categories = models.ManyToManyField(Category)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['-created_at']

    def total_likes(self):
        return [{'id':likes.id, 'user_id':likes.user.id} for likes in self.likes.all()]

    def total_comments(self):
        from like_comment.models import CommentReply

        comment_count = self.comments.count()
        
        reply_count = CommentReply.objects.filter(comment__post=self).count()
        return comment_count + reply_count

    def total_saved(self):
        return [{'id':saved_post.id, 'user_id':saved_post.user.id} for saved_post in self.saved_posts.all()]


class SavedPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='saved_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id}) User: {self.user.username} --> Post: {self.post.title}'

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']