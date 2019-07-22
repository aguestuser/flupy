"""chapter 2, section 1 list comprehensions"""

colors = ['black', 'white']
sizes = ['S', 'M', 'L']
tshirts = [(c, s) for c in colors for s in sizes]
