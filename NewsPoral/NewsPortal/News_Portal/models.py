from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse

article = 'AR'
news = 'NR'

POST = [
    (article, 'Статья'),
    (news, 'Новости')
]

class Author(models.Model):
    user = models.OneToOneField(max_length=50, blank=False, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.00)


   def update_rating(self):
        author_posts_rating = Post.objects.filter(author_id=self.pk).aggregate(
            post_rating_sum=Coalesce(Sum('rating') * 3, 0))
        author_comment_rating = Comment.objects.filter(user_id=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))
        author_post_comment_rating = Comment.objects.filter(post__author__user=self.user).aggregate(
            comments_rating_sum=Coalesce(Sum('rating'), 0))
        print(author_posts_rating)
        print(author_post_comment_rating)
        print(author_post_comment_rating)
        self.rate = author_posts_rating['post_rating_sum'] + author_comment_rating['comments_rating_sum'] \
            + author_post_comment_rating['comments_rating_sum']
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=220, unique=True)

    def __str__(self):
        return self.name_category

class Post(models.Model):
    article = 'AR'
    news = 'NW'

    objects = None
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    choice_title = models.DateTimeField(auto_now_add=True)
    create_date = models.ManyToManyField(Category, through='PostCatedory')
    head_name = models.CharField(max_length=250, unique=True)
    article_text = models.TextField()
    post_rating = models.FloatField(default=0.00)

    def __str__(self):
        return self.head_name

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        article_text = self.article_text
        preview = article_text[0:124]
        points = "..."
        return preview + points




class PostCategory(models.Model):
    author = models.ForeignKey(Post, on_delete=models.CASCADE)
    rating = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):

    objects = None
    comment = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    text_in_comment = models.DateTimeField(auto_now_add=True)
    rating_comment = models.IntegerField(default=0)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def like(self):
        self.rating_comment += 1
        self.save()

    def dislike(self):
        self.rating_comment -= 1
        self.save()


# Create your models here.
