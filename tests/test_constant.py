import pytest

from injection import constant, get_instance


class TestConstant:
    def test_constant_with_success(self):
        @constant
        class SomeInjectable:
            pass

        instance_1 = get_instance(SomeInjectable)
        instance_2 = get_instance(SomeInjectable)
        assert instance_1 is instance_2

    def test_constant_with_recipe(self):
        class SomeClass:
            pass

        @constant
        def recipe() -> SomeClass:
            return SomeClass()

        instance_1 = get_instance(SomeClass)
        instance_2 = get_instance(SomeClass)
        assert instance_1 is instance_2

    def test_constant_with_recipe_and_no_return_type(self):
        class SomeClass:
            pass

        @constant
        def recipe():
            return SomeClass()  # pragma: no cover

        instance_1 = get_instance(SomeClass)
        instance_2 = get_instance(SomeClass)
        assert instance_1 is instance_2

    def test_constant_with_on(self):
        class A:
            pass

        @constant(on=A)
        class B(A):
            pass

        a = get_instance(A)
        assert isinstance(a, B)

    def test_constant_with_on_and_several_classes(self):
        class A:
            pass

        class B(A):
            pass

        @constant(on=(A, B))
        class C(B):
            pass

        a = get_instance(A)
        b = get_instance(B)
        assert isinstance(a, C)
        assert isinstance(b, C)
        assert a is b

    def test_constant_with_injectable_already_exist_raise_runtime_error(self):
        class A:
            pass

        @constant(on=A)
        class B(A):
            pass

        with pytest.raises(RuntimeError):

            @constant(on=A)
            class C(A):
                pass

    def test_constant_with_override(self):
        @constant
        class A:
            pass

        @constant(on=A, mode="override")
        class B(A):
            pass

        a = get_instance(A)
        assert isinstance(a, B)

    def test_constant_with_multiple_override(self):
        @constant
        class A:
            pass

        @constant(on=A, mode="override")
        class B(A):
            pass

        @constant(on=A, mode="override")
        class C(B):
            pass

        a = get_instance(A)
        assert isinstance(a, C)