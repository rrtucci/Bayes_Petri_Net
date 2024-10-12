# https://github.com/vvasilescu-uni/OOP-Homework-2
from utils import get_label_value, get_gray_tone, draw_dot_file

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
        if capacity < 0:
            self.reverse()

    def __str__(self):
        return f"({self.name_pair}, {self.capacity})"

    def reverse(self):
        self.capacity = -self.capacity
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


class PetriNet:
    global step_num
    step_num=0
    def __init__(self,
                 places,
                 arcs,
                 tras):
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
        assert False, f"no place named {name}"

    def get_arc_from_name_pair(self, name_pair):
        for arc in self.arcs:
            if arc.name_pair == name_pair:
                return arc
        assert False, f"no arc named {name_pair}"

    def get_tra_from_name(self, name):
        for tra in self.tras:
            if tra.name == name:
                return tra
        assert False, f"no transition named {name}"

    def get_firing_tras_from_names(self, names):
        return [self.get_tra_from_name(name) for name in names]

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

    def inner_step(self,
                   firing_tras=None,
                   jupyter=True,
                   red_arc_list=None):
        global step_num
        print("step_num=", step_num)
        assert firing_tras is not None
        if step_num > len(firing_tras):
            return
        if step_num != 0:
            tra = firing_tras[step_num - 1]
            self.fire_transition(tra)
        self.describe_current_markings()
        self.draw(jupyter, red_arc_list)
        step_num += 1

    def write_dot_file(self,
                       fname,
                       num_grays=10,
                       red_arc_list=None):
        with open(fname, "w") as f:
            str0 = "digraph G {\n"
            for arc in self.arcs:
                ar0, ar1 = arc.name_pair
                cap = arc.capacity
                str1 = ""
                if red_arc_list and arc in red_arc_list:
                    ar0, ar1 = ar1, ar0
                    cap = -cap
                    str1 = ", color=red"
                str0 += f"{ar0}->{ar1}[label={cap}{str1}];\n"
            max_content = max([p.content for p in self.places])
            num_grays = max(max_content, num_grays)
            for p in self.places:
                str1 = "[shape=circle, style=filled, fontcolor=red, "
                tone = get_gray_tone(num_grays, p.content)
                str0 += p.name + str1 + \
                        f'fillcolor="{tone}", ' + \
                        f"label={p.content}];\n"
            for tra in self.tras:
                str0 += tra.name + "[shape=none];\n"
            str0 += "}"
            f.write(str0)

    @staticmethod
    def read_dot_file(fname):
        places = []
        arcs = []
        tras = []
        tra_names = []
        with open(fname, "r") as f:
            for line in f:
                line.strip()
                if line:
                    if "digraph" in line:
                        pass
                    elif "->" in line:
                        capacity = get_label_value(line)
                        nd1, x = line.split("->")
                        nd2 = x.split("[")[0]
                        arc = Arc((nd1.strip(), nd2.strip()), capacity)
                        arcs.append(arc)
                    elif "shape=circle" in line:
                        pname = line.split("[")[0].strip()
                        content = get_label_value(line)
                        p = Place(pname, content)
                        places.append(p)
                    elif "shape=none" in line:
                        name = line.split("[")[0].strip()
                        tra_names.append(name)
        pnames = [p.name for p in places]
        for tra_name in tra_names:
            out_arcs = []
            in_arcs = []
            for arc in arcs:
                if arc.name_pair[0] in pnames:
                    in_arcs.append(arc)
                elif arc.name_pair[1] in pnames:
                    out_arcs.append(arc)
            tra = Transition(tra_name, in_arcs, out_arcs)
            tras.append(tra)
        return places, arcs, tras

    def draw(self, jupyter, red_arc_list=None):
        fname = "tempo.txt"
        self.write_dot_file(fname, red_arc_list=red_arc_list)
        draw_dot_file(fname, jupyter=jupyter)


    @staticmethod
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


if __name__ == "__main__":
    def main1():
        places = [Place("p1", 5), Place("p2", 1), Place("p3", 1)]
        arc1 = Arc(("p1", "x1"), 1)
        arc2 = Arc(("x1", "p2"), 1)
        arc3 = Arc(("x1", "p3"), 1)
        arcs = [arc1, arc2, arc3]
        in_arcs = [arc1]
        out_arcs = [arc2, arc3]
        tra = Transition("x1", in_arcs, out_arcs)
        tras = [tra]
        pnet = PetriNet(places, arcs, tras)
        pnet.write_dot_file("dot_atlas/PN_fork.txt")

        pnet.describe_current_markings()
        pnet.fire_transition(tra)
        pnet.describe_current_markings()


    def main2(fname):
        print("\nread test:")
        places, arcs, tras = PetriNet.read_dot_file(fname)
        PetriNet.describe_PAT(places, arcs, tras)
        pnet = PetriNet(places, arcs, tras)
        pnet.draw(jupyter=False)


    # main1()
    # main2("dot_atlas/PN_fork.txt")
    main2("dot_atlas/PN_loop.txt")
