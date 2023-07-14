# Injection

Fast and easy dependency injection framework.

## Quick start

⚠️ _Requires Python 3.10 or higher_

```bash
pip install injection
```

## How to use

### Create an injectable

If you wish to inject a singleton, use `unique` decorator.

```python
from injection import unique

@unique
class MyClass:
    """ class implementation """
```

If you wish to inject a new instance each time, use `new` decorator.

```python
from injection import new

@new
class MyClass:
    """ class implementation """
```

### Inject an instance

To inject one or several instances, use `inject` decorator.
_Don't forget to annotate type of parameter to inject._

```python
from injection import inject

@inject
def my_function(instance: MyClass):
    """ function implementation """
```

### Inheritance

In the case of inheritance, you can use the decorator parameters `reference` or `references` to link the injection to 
one or several other classes.

**Warning: if the child class is in another file, make sure that file is imported before injection.**

_`reference` parameter example:_

```python
from injection import unique

class A:
    ...

@unique(reference=A)
class B(A):
    ...
```

_`references` parameter example:_

```python
from injection import unique

class A:
    ...

class B(A):
    ...

@unique(references=(A, B))
class C(B):
    ...
```

### Recipes

A recipe is a function that tells the injector how to construct the instance to be injected. It is important to specify 
the reference class(es) when defining the recipe.

```python
from injection import unique

@unique(reference=MyClass)
def my_recipe() -> MyClass:
    """ recipe implementation """
```
