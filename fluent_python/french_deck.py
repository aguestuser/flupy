"""French Deck module"""
import collections
from typing import NamedTuple, List, Dict, Iterable, Iterator, cast

Card = NamedTuple('Card', [('rank', str), ('suit', str)])


class FrenchDeck:
    ranks: List[str] = [str(n) for n in range(2, 11)] + list('JQKA')
    suits: List[str] = 'spades diamonds clubs hearts'.split()
    suit_values: Dict[str, int] = dict(spades=3, hearts=2, diamonds=1, clubs=0)

    def __init__(self) -> None:
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self) -> int:
        return len(self._cards)

    # we don't have to implement this if we cast in line 33
    # def __iter__(self) -> Iterator[Card]:
    #     for card in self._cards:
    #         yield card
    
    def __getitem__(self, position) -> Card:
        return self._cards[position]

    # __getitem__ allows indexing and slicing:
    # >>> deck[0]
    # Card(rank='2', suit='spades')
    # >>> deck[-1]
    # Card(rank='A', suit='hearts')
    
    # >>> deck[:3]
    # [Card(rank='2', suit='spades'), Card(rank='3', suit='spades'),
    # Card(rank='4', suit='spades')]

    # and:
    # >>> for card in deck: # doctest: +ELLIPSIS
    # ...
    # print(card)
    # Card(rank='2', suit='spades')
    # Card(rank='3', suit='spades')
    # Card(rank='4', suit=

    def sorting(self, card: Card) -> int:
        rank_value = FrenchDeck.ranks.index(card.rank)
        return rank_value * len(self.suit_values) + self.suit_values[card.suit]

    def sorted(self) -> List[Card]:
        return sorted(cast(Iterable[Card], self), key=self.sorting)
