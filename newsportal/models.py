from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author_id=self).aggregate(Sum('rating'))['rating__sum'] or 0
        comment_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))['rating__sum'] or 0
        post_comment_rating = Comment.objects.filter(post__author_id=self).aggregate(Sum('rating'))['rating__sum'] or 0

        self.rating = post_rating * 3 + comment_rating + post_comment_rating

        self.save()


class Category(models.Model):
    cat_name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.cat_name.title()


post = 'PO'
news = 'NE'

POST = [
    (post, 'Пост'),
    (news, 'Новость')
]


class Post(models.Model):
    author = models.ForeignKey('Author', on_delete=models.RESTRICT)
    post_type = models.CharField(max_length=2, choices=POST)
    post_data = models.DateTimeField(auto_now_add=True)
    head_text = models.CharField(max_length=100)
    text = models.TextField(max_length=1500, default='Lorem Ipsum')
    rating = models.SmallIntegerField(default=0)
    post_cat = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) > 20:
            return self.text[:20] + "..."
        else:
            return self.text.title()

    def __str__(self):
        date = self.post_data.strftime('%d-%m-%Y')
        return f'{self.head_text.title()}: {self.preview()} : {date}'


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    cat = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    comment = models.CharField(max_length=200, default='Lorem Ipsum')
    rating = models.SmallIntegerField(default=0)
    comment_data = models.DateTimeField(auto_now_add=True)

    def like(self):
        self.rating += self.rating
        self.save()

    def dislike(self):
        self.rating -= self.rating
        self.save()
