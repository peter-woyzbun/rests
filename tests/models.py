from django.db import models
from rest_framework import serializers


# =================================
# Base Test Model
# ---------------------------------

class TestModel(models.Model):

    """
    Abstract base model for providing app label.

    """

    class Meta:
        abstract = True
        app_label = 'tests'


# =================================
# Test Models
# ---------------------------------

class Thing(TestModel):
    name = models.CharField(null=True, max_length=200)
    number = models.IntegerField(null=True)


class ThingChild(TestModel):
    parent = models.ForeignKey(Thing, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    number = models.IntegerField(null=True)


class ThingChildChild(TestModel):
    parent = models.ForeignKey(ThingChild, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    number = models.IntegerField(null=True)


class ThingChildChildChild(TestModel):
    parent = models.ForeignKey(ThingChildChild, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(null=True, max_length=200)
    number = models.IntegerField(null=True)


class GenericModel(TestModel):
    name = models.CharField(null=True, max_length=200)


# =================================
# Serializers
# ---------------------------------


class ThingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Thing
        fields = '__all__'


class ThingChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThingChild
        fields = '__all__'


class GenericModelSeriaizer(serializers.ModelSerializer):
    class Meta:
        model = GenericModel
        fields = '__all__'