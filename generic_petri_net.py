# https://github.com/vvasilescu-uni/OOP-Homework-2

class Place:
    def __init__(self, name, content):
        self.name = name
        self.content = content
    def __str__(self):
        return f"name={self.name}, content={self.content}"

class Arc:
    def __init__(self, name_pair, capacity):
        self.name_pair = name_pair
        self.capacity = capacity
    def __str__(self):
        return f"name={self.name_pair}, capacity={self.capacity}"

class Transition:
    def __init__(self,
                name,
                in_arcs,
                out_arcs):
        self.name = name
        self.in_arcs = in_arcs
        self.out_arcs = out_arcs

    def describe_self(self):
        print(f"name={self.name}")
        print("in_arcs:")
        for arc in self.in_arcs:
            print(arc)
        print("out_arcs:")
        for arc in self.out_arcs:
            print(arc)

class Petri_Net:
    def __init__(self,
                 places,
                 tras,
                 arcs):
        self.places = places
        self.tras = tras
        self.arcs = arcs
        place_names = [p.name for p in places]
        for arc in arcs:
            assert (arc.name_pair[0].issubset(place_names))
            assert (arc.name_pair[1].issubset(place_names))

        for tra in tras:
            in_names = [arc.pair[0] for arc in tra.in_arcs]
            out_names = [arc.pair[1] for arc in tra.out_arcs]
            assert (set(in_names).issubset(place_names))
            assert (set(out_names).issubset(place_names))

    def get_place_from_name(self, name):
        for p in self.places:
            if p.name == name:
                return p
        assert False

    def is_enabled(self, tra):
        for arc in tra.in_arcs:
            in_place = self.get_place_from_name(arc.name_pair[0])
            if arc.capacity > in_place.content:
                return False
        return True

    def fire_transition(self, tra):

        if not self.is_enabled(tra):
            print(f"Transition {tra.name} is not enabled!")
            return
        else:
            print(f"Fired transition {tra.name}.\n")

        tokens_in_transit = 0
        for arc in tra.in_arcs:
            in_place = self.get_place_from_name(arc.name_pair[0])
            in_place.content -= arc.capacity
            tokens_in_transit += arc.capacity

        for arc in tra.out_arcs:
            out_place = self.get_place_from_name(arc.name_pair[1])
            delta = min(tokens_in_transit, arc.capacity)
            out_place.content += delta
            tokens_in_transit -= delta


    def describe_current_markings(self):
        for place in self.places:
            print(place, "\n")
