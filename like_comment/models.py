from django.db import models
from django.contrib.auth import get_user_model
from post.models import Post
 
User = get_user_model()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} {self.user.username} liked {self.post.title}'
    
    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-created_at']


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} {self.user.username} commented on {self.post.title}'
    
    class Meta:
        ordering = ['-created_at']



class CommentReply(models.Model):
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.comment:
            return f'{self.id} {self.user.username} replied to comment: {self.comment.body}'
        return f'{self.id} {self.user.username} replied to reply ID: {self.parent.id}'
    
    class Meta:
        ordering = ['created_at']