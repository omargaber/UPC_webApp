# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=12)
    logged_in = models.BooleanField(default=False)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.email


class Professor(Student):

    def __str__(self):
        """Unicode representation of Course."""
        return self.name


class OfficeHours(models.Model):
    student_id = models.CharField(max_length=100)
    #student_name = models.CharField(max_length=100)
    professor_needed = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor)

    def __str__(self):
        """Unicode representation of Request."""
        pass


class Slot(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        """Unicode representation of Course."""
        return self.title


class Course(models.Model):
    """Model definition for Course."""
    name = models.CharField(max_length=100)

    # TODO: Define fields here

    class Meta:
        """Meta definition for Course."""

        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        """Unicode representation of Course."""
        return self.name


class Day(models.Model):
    """Model definition for Day."""
    name = models.CharField(max_length=100)

    class Meta:
        """Meta definition for Day."""

        verbose_name = 'Day'
        verbose_name_plural = 'Days'

    def __str__(self):
        """Unicode representation of Day."""
        return self.name


class Table(models.Model):
    """Model definition for Table."""
    Day = models.ForeignKey(Day, on_delete=models.CASCADE, related_name='day')
    Slot = models.ForeignKey(
        Slot, on_delete=models.CASCADE, related_name='slot')
    Course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='course')
    # TODO: Define fields here

    class Meta:
        """Meta definition for Table."""
        unique_together = (('Day', 'Slot', 'Course'),)
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'

    def __str__(self):
        return self.Day.name+","+self.Slot.title
