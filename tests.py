import decimal
import re
import unittest

import spitobj


class Place:
    name = ''

    def __init__(self, name):
        self.name = name


class PlaceSpitter(spitobj.Spitobj):
    obj_class = Place
    fields = (
        ('name', spitobj.StringGenerator()),
    )


class Person:
    nickname = ''
    birth_place = None
    spouse = None
    gender = ''
    friends = []

    def __init__(self, nickname, birth_place, spouse, gender):
        self.nickname = nickname
        self.birth_place = birth_place
        self.spouse = spouse
        self.gender = gender


class PersonSpitter(spitobj.Spitobj):
    obj_class = Person
    fields = (
        ('nickname', spitobj.StringGenerator()),
        ('birth_place', spitobj.ObjectGenerator(PlaceSpitter)),
        ('spouse', spitobj.ObjectGenerator("Self", spouse=None)),
        ('gender', 'male'),
    )


class TestSpitobj(unittest.TestCase):
    def test_one_gives_single_object(self):
        spitter = PersonSpitter()

        person = spitter.get()

        assert person.nickname != ''

    def test_spitobj_works_when_field_is_const(self):
        spitter = PersonSpitter()

        person = spitter.get()
        assert person.gender == "male"

        person2 = spitter.get()
        assert person2.gender == "male"
        assert person2.gender != person.nickname

    def test_generated_value_can_be_overridden(self):
        expected = 'Sussy'
        spitter = PersonSpitter()

        person = spitter.get(nickname=expected)

        assert person.nickname == expected

    def test_spitobj_generates_object_with_subspitobj(self):
        spitter = PersonSpitter()

        person = spitter.get()

        assert person.birth_place != None
        assert person.birth_place.name != None

    def test_subspitobj_value_can_be_overriden(self):
        expected_place = PlaceSpitter().get()

        person = PersonSpitter().get(birth_place=expected_place)

        assert person.birth_place.name == expected_place.name

    def test_subspitobj_generates_recurrsion_by_self_attribute(self):
        spitter = PersonSpitter()

        person = spitter.get()

        assert person.spouse != None
        assert person.spouse.nickname != None


class TestCounterGenerator(unittest.TestCase):
    def test_counter_starts_from_0(self):
        expected = 0
        gen = spitobj.CounterGenerator()

        value = next(gen)

        assert value == expected

    def test_counter_start_is_settable(self):
        expected = 0
        gen = spitobj.CounterGenerator(start=expected)

        value = next(gen)

        assert value == expected


    def test_counter_spit_increased_values(self):
        expected = 0
        gen = spitobj.CounterGenerator(start=expected)

        assert next(gen) == 0
        assert next(gen) == 1


class TestStringGenerator(unittest.TestCase):
    def test_length_is_settable(self):
        expected = 10
        gen = spitobj.StringGenerator(length=expected)

        value = next(gen)

        assert len(value) == expected

    def test_alphabet_is_settable(self):
        alphabet = 'a'
        gen = spitobj.StringGenerator(alphabet=alphabet)

        value = next(gen)

        assert value == (alphabet * gen.length)

    def test_values_are_random(self):
        gen = spitobj.StringGenerator()

        value = next(gen)
        value2 = next(gen)

        assert value != value2


class TestCountedTextGenerator(unittest.TestCase):
    def test_counter_return_correct_value(self):
        text = "my-counted-{idx}"
        gen = spitobj.CountedTextGenerator(text)

        value = next(gen)

        assert value == text.format(idx=0)


class TestDecimalGenerator(unittest.TestCase):
    def test_return_value_is_decimal(self):
        gen = spitobj.DecimalGenerator(10)

        value = next(gen)

        assert isinstance(value, decimal.Decimal)

    def test_precision_set_works(self):
        gen = spitobj.DecimalGenerator(10, precision=2)

        value = str(next(gen))

        pattern = r'\d\.\d{1,2}'
        msg = "value {!r} not match pattern {!r}".format(value, pattern)
        assert re.match(pattern, value), msg


if __name__ == '__main__':
    unittest.main()
