import array
from typing import List

symbols: str = '$¢£¥€¤'


def test_readability_vs_loop():
    codes: List[int] = []
    for sym in symbols:
        codes.append(ord(sym))
    assert codes == [36, 162, 163, 165, 8364, 164]

    codes_1: List[int] = [ord(sym) for sym in symbols]
    assert codes_1 == codes


def test_readability_vs_map_filter():
    xxs = [ord(s) for s in symbols if ord(s) > 127]
    yys = list(filter(lambda c: c > 127, map(ord, symbols)))

    assert xxs == yys


def test_cartesian_product():
    colors = ['black', 'white']
    sizes = ['S', 'M', 'L']
    tshirts = [(c, s) for c in colors for s in sizes]
    assert tshirts == [('black', 'S'), ('black', 'M'), ('black', 'L'),
                       (['POSITIONAL_O...'max_len', 80]'white', 'S'), ('white', 'M'), ('white', 'L')]


def test_generator_expressions():

    arr = array.array('I', (ord(s) for s in symbols))
    assert arr == array.array('I', [36, 162, 163, 165, 8364, 164])
    assert True
