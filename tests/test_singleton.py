from dataclasses import dataclass

import pytest
from pydantic import BaseModel

from injection import aget_instance, get_instance, singleton


class TestSingleton:
    def test_singleton_with_success(self):
        @singleton
        class SomeInjectable: ...

        instance_1 = get_instance(SomeInjectable)
        instance_2 = get_instance(SomeInjectable)
        assert instance_1 is instance_2

    def test_singleton_with_recipe(self):
        class SomeClass: ...

        @singleton
        def recipe() -> SomeClass:
            return SomeClass()

        instance_1 = get_instance(SomeClass)
        instance_2 = get_instance(SomeClass)
        assert instance_1 is instance_2

    async def test_singleton_with_async_recipe(self):
        class SomeClass: ...

        @singleton
        async def recipe() -> SomeClass:
            return SomeClass()

        with pytest.raises(RuntimeError):
            get_instance(SomeClass)

        instance_1 = await aget_instance(SomeClass)
        instance_2 = get_instance(SomeClass)
        assert instance_1 is instance_2

    def test_singleton_with_recipe_and_union(self):
        class A: ...

        class B(A): ...

        @singleton
        def recipe() -> A | B:
            return B()

        a = get_instance(A)
        b = get_instance(B)
        assert a is b
        assert isinstance(a, B)

    def test_singleton_with_recipe_and_no_return_type(self):
        class SomeClass: ...

        @singleton
        def recipe():
            return SomeClass()  # pragma: no cover

        assert get_instance(SomeClass) is None

    def test_singleton_with_on(self):
        class A: ...

        @singleton(on=A)
        class B(A): ...

        a = get_instance(A)
        assert isinstance(a, B)

    def test_singleton_with_on_and_several_classes(self):
        class A: ...

        class B(A): ...

        @singleton(on=(A, B))
        class C(B): ...

        a = get_instance(A)
        b = get_instance(B)
        assert isinstance(a, C)
        assert isinstance(b, C)
        assert a is b

    def test_singleton_with_inject(self):
        @singleton
        class A: ...

        @singleton
        class B:
            def __init__(self, __a: A):
                self.a = __a

        a = get_instance(A)
        b = get_instance(B)
        assert isinstance(a, A)
        assert isinstance(b, B)
        assert isinstance(b.a, A)
        assert a is b.a

    def test_singleton_with_dataclass_and_inject(self):
        @singleton
        class A: ...

        @singleton
        @dataclass(frozen=True, slots=True)
        class B:
            a: A

        a = get_instance(A)
        b = get_instance(B)
        assert isinstance(a, A)
        assert isinstance(b, B)
        assert isinstance(b.a, A)
        assert a is b.a

    def test_singleton_with_pydantic_model_and_inject(self):
        @singleton
        class A(BaseModel): ...

        @singleton
        class B(BaseModel):
            a: A

        a = get_instance(A)
        b = get_instance(B)
        assert isinstance(a, A)
        assert isinstance(b, B)
        assert isinstance(b.a, A)
        assert a is b.a

    def test_singleton_with_recipe_and_inject(self):
        @singleton
        class A: ...

        class B: ...

        @singleton
        def recipe(__a: A) -> B:
            assert isinstance(__a, A)
            assert __a is a
            return B()

        a = get_instance(A)
        b = get_instance(B)
        assert isinstance(a, A)
        assert isinstance(b, B)

    def test_singleton_with_injectable_already_exist_raise_runtime_error(self):
        class A: ...

        @singleton(on=A)
        class B(A): ...

        with pytest.raises(RuntimeError):

            @singleton(on=A)
            class C(A): ...

    def test_singleton_with_override(self):
        @singleton
        class A: ...

        @singleton(on=A, mode="override")
        class B(A): ...

        a = get_instance(A)
        assert isinstance(a, B)

    def test_singleton_with_multiple_override(self):
        @singleton
        class A: ...

        @singleton(on=A, mode="override")
        class B(A): ...

        @singleton(on=A, mode="override")
        class C(B): ...

        a = get_instance(A)
        assert isinstance(a, C)
