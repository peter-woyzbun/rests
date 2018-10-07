# res(ts): Auto-generate TypeScript models for Django projects

*Note: this is an early prototype*

`rests` generates TypeScript "models" and querysets, and corresponding
Django URLs/Views. The TypeScript models and querysets are functionally
similar to their Django equivalents.

## Table of Contents

- [Features](#features)
- [Usage Example](#usage-example)
- [Full Example](#full-example)
- [Requirements](#requirements)
- [Basic Usage](#basic-usage)


## Features

* Create/update/delete/filter/exclude Django models via TypeScript.
* The URLs/views for the functionality of the above are auto-generated.
* All queryset "lookup" keys are generated, allowing for type hints in
TypeScript akin to what you would expect in an IDE with Django support.
* Filter relations.
* Automatic retrieval of foreign key relations (i.e on `get`).
* The generated TypeScript code is self-contained: there is no package to
innstall.

## Usage Example


In Python/Django:

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

In TypeScript:

```typescript

// Create a Question instance.
const newQuestion = await Question.objects.create({question_test: 'Question?'})

// Get a Question instance.
const question = await Question.objects.get(1)

// Get choices of question with more than 3 votes.
const choices = await question.choices({votes__gt: 3}).retrieve()


```


## Full Example

A full example can be found in the `example` directory of this project.
The Django project is found [here](https://github.com/peter-woyzbun/rests/tree/master/example/example) and the
corresponding (generated) TypeScript code is found [here](https://github.com/peter-woyzbun/rests/tree/master/example/ts/server).

## Requirements

### Python

`rests` requires `django` version `2.0` or greater, and the Django REST
framework.

### TypeScript

The generated TypeScript requires `experimentalDecorators` set to `true`
in `tsconfig.json`.

## Basic Usage

### Setup

Install `rests` via pip:

```
pip install git+https://github.com/peter-woyzbun/rests.git
```

Then add `rests` to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = (
            'django.contrib.auth',
            ...
            'rests',
        )

```

### Serializers

`rests` requires Django Rest Framework serializers. DRF permission check
classes can also optionally be provided.

### Interface Definition

In your `django` app, create a file, `interface.py`, with the following
structure:

```python
from rests import interface

from .serializers import ObjectSerializer


class Interface(interface.Interface):
    objects = interface.Type(ObjectSerializer)

```

Each class property of the `Interface` class should be an `interface.Type`
instance with a serializer whose model you want exposed in your TypeScript
code.

Queryset lookups and relations will only be generated for/between models
contained in your interface definition.

Next, register your `Interface`'s url patterns in `urls.py`:

```python

from .interface import Interface

urlpatterns = Interface.urlpatterns()

```
Note: `Interface.urlpatterns()` returns a list of Django URL patterns,
so you can use it in `include(...)`.


In `settings.py`, add the following, replacing the appropriate values:

```

# Other settings...


RESTS = {
    'TRANSPILE_DEST': <path to transpile to>,
    'BASE_URL': '<base url of your interface, e.g: "http://localhost:5000/">',
    'INTERFACE_SRC': '<module.path.to.your.interface>',
}

```
The `BASE_URL` setting should reflect where you registered your
`Interface`'s url patterns. The `TRANSPILE_DEST` setting defines where
to put the TypeScript generated for your `Interface`. The `INTERFACE_SRC`
setting points to the python file containing your `Interface` class.

### Transpile

Finally, to generate the TypeScript code, in your project directory
(containing `manage.py`) use

```
python manage.py transpile
```