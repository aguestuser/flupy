"""
Corresponds to Part III, Ch 5 (pp. 137 - 166) of the book: 'First-Class Functions'
"""

from typing import Callable, Iterable
from functools import reduce
from operator import add
from fluent_python.french_deck import FrenchDeck


def factorial(n: int) -> int:
    '''returns n!'''
    return 1 if n < 2 else n * factorial(n - 1)


def test_factorial():
    assert factorial(
        42) == 1405006117752879898543142606244511569936384000000000
    assert factorial.__doc__ == 'returns n!'
    assert isinstance(factorial, Callable)

    fact = factorial

    assert fact(5) == 120
    assert list(map(factorial, range(11))) == [1, 1, 2, 6, 24, 120, 720,
                                               5040, 40320, 362880, 3628800]


def test_sorted():
    fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']

    assert sorted(fruits, key=len) == ['fig', 'apple', 'cherry', 'banana',
                                       'raspberry', 'strawberry']

    def reverse(word: str) -> str:
        return word[::-1]

    assert sorted(fruits, key=reverse) == ['banana', 'apple', 'fig',
                                           'raspberry', 'strawberry', 'cherry']


def test_listcomp_instead_of_HOC():
    fact = factorial

    res_1 = [1, 1, 2, 6, 24, 120]
    assert list(map(fact, range(6))) == res_1
    assert [fact(n) for n in range(6)] == res_1

    res_2 = [1, 6, 120]
    assert list(map(fact, filter(lambda n: n % 2, range(6)))) == res_2
    assert [fact(n) for n in range(6) if n % 2] == res_2


def test_alternatives_to__reduce():
    n = 4950

    assert reduce(add, range(100)) == n
    assert sum(range(100)) == n

    assert all([True, True]) == True
    assert all([True, False]) == False

    assert any([True, False]) == True
    assert any([False, False]) == False


def test_callable():
    assert not callable(True)

    # user defined-functions
    assert callable(factorial)
    # built-in-functions
    assert callable(len)

    # built-in methods (on class or instance)
    assert callable(dict.get)
    assert callable({'foo': 1, 'bar': 1}.get)

    # methods (on class or instance)
    assert callable(FrenchDeck.sorted)
    assert callable(FrenchDeck().sorted)

    # classes
    assert callable(FrenchDeck)

    # instances that implement __call__)
    # generator functions (which return a generator object)


def test_implementing_call():
    import random

    class BingoCage:

        def __init__(self, items: Iterable[int]) -> None:
            self._items = list(items)
            random.shuffle(self._items)

        def pick(self) -> int:
            try:
                return self._items.pop()
            except IndexError:
                raise LookupError('pick from empty BingoCage')

        def __call__(self) -> int:
            return self.pick()

    bingo = BingoCage(range(3))
    assert bingo.pick() in [0, 1, 2]
    assert bingo.pick() in [0, 1, 2]
    assert bingo.pick() in [0, 1, 2]
    assert callable(bingo)


def tag(name: str, *content: str, cls: str = None, **attrs: str) -> str:
    """Generate one or more HTML tags"""
    if cls is not None:
        attrs['class'] = cls

    attr_str = (
        '',
        ''.join(' %s="%s"' % (k, v) for k, v in sorted(attrs.items()))
    )[bool(attrs)]

    return (
        '<%s%s />' % (name, attr_str),
        '\n'.join('<%s%s>%s</%s>' % (name, attr_str, c, name)
                  for c in content),
    )[bool(content)]


def test_arg_types():
    assert tag('br') == '<br />'
    assert tag('p', 'hello') == '<p>hello</p>'
    assert tag('p', 'hello', 'world') == '<p>hello</p>\n<p>world</p>'
    assert tag('p', 'hello', id="33") == '<p id="33">hello</p>'

    assert tag('p', 'hello', 'world', cls='sidebar') == (
        '<p class="sidebar">hello</p>\n'
        '<p class="sidebar">world</p>')
    assert tag(content='testing', name="img") == (
        '<img content="testing" />')

    attrs = {'name': 'img', 'title': 'Sunset Boulevard',
             'src': 'sunset.jpg', 'cls': 'framed'}
    assert tag(**attrs) == (
        '<img class="framed" src="sunset.jpg" '
        'title="Sunset Boulevard" />')


def clip(text: str, max_len: int = 80) -> str:
    """Return text clipped at the last space before or after max_len"""
    end = None
    if len(text) > max_len:
        space_before = text.rfind(' ', 0, max_len)
        if space_before >= 0:
            end = space_before
        else:
            space_after = text.rfind(' ', max_len)
            if space_after >= 0:
                end = space_after
    if end is None:  # no spaces were found
        end = len(text)
    return text[:end].rstrip()


def test_signature_retrieval():
    import inspect
    from inspect import signature, _ParameterKind as PK
    sig = signature(clip)
    sig_details = [(p.kind, name, p.default) for name, p in sig.parameters.items()]
    assert sig_details == [(PK.POSITIONAL_OR_KEYWORD, 'text', inspect._empty),
                           (PK.POSITIONAL_OR_KEYWORD, 'max_len', 80)]


def test_annotation_retrieval():
    assert clip.__annotations__ == {'text': str, 'max_len': int, 'return': str}


def test_retrieving_annotation_from_signature():
    import inspect
    from inspect import signature
    sig = signature(clip)
    annotations = [(p.name, p.annotation, p.default) for p in sig.parameters.values()]
    assert annotations == [('text', str, inspect._empty), ('max_len', int, 80)]


def test_signature_binding():
    import inspect
    sig = inspect.signature(tag)
    my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
              'src': 'sunset.jpg', 'cls': 'framed'}
    bound_args = sig.bind(**my_tag)
    assert bound_args.arguments == {'name': 'img', 'cls': 'framed',
                                    'attrs': {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}}


def test_arithmetic_operators():
    """p. 156"""
    from functools import reduce
    from operator import mul

    def ugly_fact(n: int) -> int:
        return reduce(lambda a, b: a * b, range(1, n + 1))

    def fact(n: int) -> int:
        return reduce(mul, range(1, n + 1))

    assert ugly_fact(42) == fact(42) == factorial(42)


def test_selection_operators():
    """p. 157 - 158"""

    # select items from tuples
    from operator import itemgetter

    metro_data = [
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386)),
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
    ]

    assert sorted(metro_data, key=itemgetter(1)) == [
        ('Sao Paulo', 'BR', 19.649, (-23.547778, -46.635833)),
        ('Delhi NCR', 'IN', 21.935, (28.613889, 77.208889)),
        ('Tokyo', 'JP', 36.933, (35.689722, 139.691667)),
        ('Mexico City', 'MX', 20.142, (19.433333, -99.133333)),
        ('New York-Newark', 'US', 20.104, (40.808611, -74.020386))
    ]

    assert [itemgetter(1, 0)(city) for city in metro_data] == [
        ('JP', 'Tokyo'),
        ('IN', 'Delhi NCR'),
        ('MX', 'Mexico City'),
        ('US', 'New York-Newark'),
        ('BR', 'Sao Paulo')
    ]

    # select attributes from objects
    from operator import attrgetter
    from typing import NamedTuple

    LatLong = NamedTuple('LatLong', [('lat', float), ('long', float)])
    Metropolis = NamedTuple('Metropolis', [('name', str), ('cc', str), ('pop', float), ('coord', LatLong)])

    metro_areas = [Metropolis(name, cc, pop, LatLong(lat, long))
                   for name, cc, pop, (lat, long) in metro_data]
    assert metro_areas[0].coord.lat == 35.689722

    cities_by_lat = [attrgetter('name', 'coord.lat')(city) for city in
                     sorted(metro_areas, key=attrgetter('coord.lat'))]

    assert cities_by_lat == [
        ('Sao Paulo', -23.547778),
        ('Mexico City', 19.433333),
        ('Delhi NCR', 28.613889),
        ('Tokyo', 35.689722),
        ('New York-Newark', 40.808611)
    ]


def test_display_all_operators():
    import operator
    """p. 158"""
    ops = [name for name in dir(operator) if not name.startswith('_')]
    assert ops == ['abs', 'add', 'and_', 'attrgetter', 'concat', 'contains',
                   'countOf', 'delitem', 'eq', 'floordiv', 'ge', 'getitem', 'gt',
                   'iadd', 'iand', 'iconcat', 'ifloordiv', 'ilshift', 'imatmul', 'imod', 'imul',
                   'index', 'indexOf', 'inv', 'invert', 'ior', 'ipow', 'irshift',
                   'is_', 'is_not', 'isub', 'itemgetter', 'itruediv', 'ixor', 'le',
                   'length_hint', 'lshift', 'lt', 'matmul', 'methodcaller', 'mod', 'mul', 'ne',
                   'neg', 'not_', 'or_', 'pos', 'pow', 'rshift', 'setitem', 'sub',
                   'truediv', 'truth', 'xor']


def test_methodcaller_operator():
    """p. 159"""
    from operator import methodcaller
    hyphenate = methodcaller('replace', ' ', '-')
    assert hyphenate('The time has come') == 'The-time-has-come'


def test_trivial_partial_example():
    """p. 159-160"""
    from operator import mul
    from functools import partial

    triple = partial(mul, 3)
    assert triple(7) == 21
    assert list(map(triple, range(1, 10))) == [3, 6, 9, 12, 15, 18, 21, 24, 27]


def test_partial_for_unicode_normalization():
    """p. 160"""
    import unicodedata, functools

    nfc = functools.partial(unicodedata.normalize, 'NFC')
    s1 = 'café'
    s2 = 'cafe\u0301'
    assert s1 != s2
    assert nfc(s1) == nfc(s2)


def test_partial_application_of_tag():
    """p. 160"""
    from functools import partial
    pic = partial(tag, 'img', cls='pic-frame')

    assert pic.func == tag
    assert pic.args == ('img', )
    assert pic.keywords == {'cls': 'pic-frame'}
    assert pic(src='wumpus.jpg') == '<img class="pic-frame" src="wumpus.jpg" />'
