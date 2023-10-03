from django.db import models


class Course(models.Model):

    name = models.CharField(max_length=100, verbose_name='Name')
    preview = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Preview')
    description = models.TextField(null=True, blank=True, verbose_name='Description')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'


class Lesson(models.Model):

    name = models.CharField(max_length=50, verbose_name='Name')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    preview = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Preview')
    video = models.URLField(null=True, blank=True, max_length=300, verbose_name='Video')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
