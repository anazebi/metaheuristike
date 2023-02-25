from copy import deepcopy
from Predmet import Item
from functools import reduce

properties_number = 0

class Knapsack(object):

    def __init__(self, all_items, *restrictions, **kwargs):
        
        self.value = 0
        self.items_out = all_items              # predmeti van ruksaka
        self.start_value = 0
        self.items_in = []                      # predmeti u ruksaku
        self.iterations = 0                     # broj iteracija
        self.steps = []                         # koraci do sada

        # postavljanje svih ogranicenja na pojedine dimenzije ruksaka
        for indeks, restriction in enumerate(restrictions):
            setattr(self, 'property{}'.format(indeks + 1), int(restriction))

        # broj dimenzija ruksaka
        properties_number = len(restrictions)

        for key in kwargs.keys():
            setattr(self, key, kwargs[key])

    def can_add(self, item):                    # funkcija koja vraca true ako dani predmet mozemo dodati u ruksak, false inace 
        
        if item in self.items_in:
            return False                        # predmet ne smije vec biti u ruksaku

        # predmet mozemo dodati ako nijedna njegova tezina ne prelazi preostali kapacitet pripadne dimenzije ruksaka
        for i in range(properties_number):
            if getattr(self, 'property{}'.format(i + 1)) < getattr(item, 'property{}'.format(i + 1)):
                return False
        
        return True

    def add_item(self, item):                   # vraca True ako je predmet uspjesno dodan u ruksak, False inace

        if self.can_add(item):
            self.value += item.value

            for i in range (properties_number):
                setattr(self, 'property{}'.format(i + 1), int(getattr(self, 'property{}'.format(i + 1))) - int(getattr(item, 'property{}'.format(i + 1))))
                # smanjujemo preostali kapacitet svake dimenzije ruksaka za pripadne vrijednosti tezina predmeta kojeg u njega dodajemo
            self.items_in.append(item)
            self.items_out.remove(item)
            return True
        
        return False

    def remove_item(self, item):                # vraca True ako je predmet uspjesno izbacen, False inace

        if item in self.items_in:
            for i in range(properties_number):
                setattr(self, 'property{}'.format(i + 1), int(getattr(self,'property{}'.format(i + 1))) + int(getattr(item, 'property{}'.format(i + 1)))) 
                # uvecavamo preostali kapacitet svake dimenzije ruksaka za pripadne vrijednosti tezina predmeta kojeg iz njega izbacujemo

            self.value = self.value - item.value
            self.items_out.append(item)         # dodajemo predmet u listu predmeta izvan ruksaka
            self.items_in.remove(item)          # izbacujemo predmet iz liste predmeta sadrzanih u ruksaku
            return True

        return False

    def __contains__(self, item):
        return any(map(lambda x: x == item, self.items_in))    ## any vraca True ako je bilo koja od vrijednosti True, map vraca listu vrijednosti dobivenih kad lambda funkciju primijenimo na listu predmeta u ruksaku 

    def sort(self, items):                      # vraca listu predmeta sortiranu po omjeru vrijednosti i ukupne tezine
        return sorted(items, key = Item.ratio, reverse = True)

    def switch_possible(self, item1, item2):    # vraca True ako predmet item1 iz ruksaka mogu zamijeniti predmetom item2 koji nije u ruksaku

        if item1 not in self.items_in or item2 not in self.items_out:
            return False

        for i in range (properties_number):
            if(int(getattr(self, 'property{}'.format(i + 1))) + int(getattr(item1, 'property{}'.format(i + 1))) < int(getattr(item2, 'property{}'.format(i + 1)))):
                return False
        
            return True

    def switch(self, item1, item2):                   # vraca True ako je zamjena uspjesno obavljena, false inace 
        
        if self.switch_possible(item1, item2):
            self.add_item(item2)
            self.remove_item(item1)
            return True

        return False

    def evaluate_switch(self, item1, item2):        # vraca vrijednost ruksaka nakon izbacivanja predmeta item1 te dodavanja predmeta item2

        if(self.switch_possible(item1, item2)):
            return self.value - item1.value + item2.value
        
        return False

    def execute_step(self, step, silent = False):
        
        for item in step.add_items:
            if not item in self.items_out:
                return False
            self.add_item(item)

        for item in step.remove_items:
            if not item in self.items_in:
                return False
            self.remove_item(item)

        if not silent:
            self.iterations += 1
            self.steps.append(step)



# klasa koja predstavlja korak prijelaza iz jedne konfiguracije u drugu
class Step(object):

    def __init__(self, add_items = [], remove_items = []):      # konstruktor koji kreira korak s listom predmeta za dodavanje u ruksak te s listom predmeta za uklanjanje iz ruksaka
        
        self.add_items = add_items
        self.remove_items = remove_items

    def evaluate_step(self):                                   # funkcija vraca promjenu vrijednosti ruksaka nakon izvrsenog koraka, procjenjuje 'snagu' koraka
        
        increase_value = decrease_value = 0

        if not len(self.add_items) == 0:
            increase_value = reduce(lambda x, y : x + y, [item.value for item in self.add_items])  # reduce primjenjuje lambda funkciju na elemente liste

        if not len(self.remove_items) == 0:
            decrease_value = reduce(lambda x, y : x + y, [item.value for item in self.remove_items])

        return increase_value - decrease_value

    def __eq__(self, another_step):                            # omogucujemo usporedbu koraka
        
        if not isinstance(another_step, Step):
            return False

        return self.remove_items == another_step.remove_items and self.add_items == another_step.add_items

    def reverse_step(self):                                    # radi suprotni korak
        return Step(add_items = self.remove_items, remove_items = self.add_items)