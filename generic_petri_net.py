# https://github.com/vvasilescu-uni/OOP-Homework-2

class Place:
    def __init__(self, name, content):
        self.name = name
        self.content = content
    def __str__(self):
        return f"({self.name}, {self.content})"

class Arc:
    def __init__(self, name_pair, capacity):
        self.name_pair = name_pair
        self.capacity = capacity
    def __str__(self):
        return f"({self.name_pair}, {self.capacity})"

class Transition:
    def __init__(self,
                name,
                in_arcs,
                out_arcs):
        self.name = name
        self.in_arcs = in_arcs
        self.out_arcs = out_arcs

    def describe_self(self):
        print(f"\nname={self.name}")
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
        tra_names = [t.name for t in tras]
        # print("nnmk", place_names, tra_names)
        for arc in arcs:
            a, b = arc.name_pair
            assert (a in place_names and b in tra_names) or \
                (b in place_names and a in tra_names), f"arc ({a}, {b})"

        for tra in tras:
            in_names = [arc.name_pair[0] for arc in tra.in_arcs]
            out_names = [arc.name_pair[1] for arc in tra.out_arcs]
            # print("vvbbgt", "-----------")
            # tra.describe_self()
            # print("in_names", in_names)
            # print("out_names", out_names)
            assert set(in_names).issubset(place_names), \
                f"{in_names} not in {place_names}"
            assert set(out_names).issubset(place_names), \
                f"{out_names} not in {place_names}"

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
            print(f"Fired transition {tra.name}.")

        for arc in tra.in_arcs:
            in_place = self.get_place_from_name(arc.name_pair[0])
            in_place.content -= arc.capacity

        for arc in tra.out_arcs:
            out_place = self.get_place_from_name(arc.name_pair[1])
            out_place.content += arc.capacity


    def describe_current_markings(self):
        print("current markings:", [(p.name, p.content) for p in self.places])


if __name__ == "__main__":
    def main():
        places=[Place("p1", 5), Place("p2", 1), Place("p3", 1)]
        arc1 = Arc(("p1","x1"), 1)
        arc2 = Arc(("x1", "p2"), 1)
        arc3 = Arc(("x1", "p3"), 1)
        arcs = [arc1, arc2, arc3]
        in_arcs = [arc1]
        out_arcs = [arc2, arc3]
        tra = Transition("x1", in_arcs, out_arcs)
        tras = [tra]
        pnet = Petri_Net(places, tras, arcs)
        pnet.describe_current_markings()
        pnet.fire_transition(tra)
        pnet.describe_current_markings()
    main()