class Place:
    def __init__(self, name, content):
        self.name = name
        self.content = content

    def __str__(self):
        return f"({self.name}, {self.content})"


class Arc:
    def __init__(self, name_pair, capacity, inv):
        self.name_pair = name_pair
        self.capacity = capacity
        self.inv = inv
        if inv:
            self.reverse()

    def __str__(self):
        return f"({self.name_pair}, {self.capacity}, {self.inv})"

    def __eq__(self, other):
        return self.name_pair == other.name_pair and \
                self.capacity == other.capacity and \
                self.inv == other.inv

    def reverse(self):
        self.inv = not self.inv
        self.name_pair = (self.name_pair[1], self.name_pair[0])


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

def describe_PAT(places, arcs, tras):
    print("\nplaces:")
    for p in places:
        print(p)
    print("\narcs:")
    for a in arcs:
        print(a)
    print("\ntransitions:")
    for tra in tras:
        tra.describe_self()
