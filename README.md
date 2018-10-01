# res(ts)

`rests` takes `django rest framework` serializers and auto-generates the
following:

1. A TypeScript "model" and queryset for each serializer's model, and
2. Django views and URL patterns for handling model (get, create...)
   and queryset (filter, exclude...) logic.

## Example

Given the following models:

```python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

```

the TypeScript file [models.ts](https://github.com/peter-woyzbun/rests/blob/master/example/ts/models.ts)
is generated.

## Basic Usage

Install `rests` via pip:

```
pip install https://github.com/peter-woyzbun/rests.git
```

Then add `rests` to `INSTALLED_APPS` in `settings.py`.

In your `django` app, create a file, `interface.py`, with the following
structure:

```python
from rests import interface

from .serializers import ObjectSerializer


class Interface(interface.Interface):
    objects = interface.Type(ObjectSerializer)

```

then, in `urls.py`:

```python

from .interface import Interface

urlpatterns = Interface.urlpatterns()

```

In `settings.py`, add the following, replacing the appropriate values:

```

# Other settings...


RESTS = {
    'TRANSPILE_DEST': <path to transpile to>,
    'BASE_URL': '<base url of your interface>',
    'POST_TRANSPILE_COMMAND': None,
    'INTERFACE_SRC': '<module.path.to.your.Interface>',
    'MODELS_FILENAME': 'models.ts'
}


```
