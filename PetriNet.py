# https://github.com/vvasilescu-uni/OOP-Homework-2
from utils import get_label_value, get_gray_tone, draw_dot_file
from PAT import *


class PetriNet:
    """

    Attributes
    ----------
    arcs: list[Arc]
    places: list[Place]
    step_num: int
    tras: list[Transition]
    """
    global step_num
    step_num = 0

    def __init__(self,
                 places,
                 arcs,
                 tras):
        """

        Parameters
        ----------
        places: list[Place]
        arcs: list[Arc]
        tras: list[Transition]
        """
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
        """

        Parameters
        ----------
        name: str

        Returns
        -------
        Place

        """
        for p in self.places:
            if p.name == name:
                return p
        assert False, f"no place named {name}"

    def get_arc_from_name_pair(self, name_pair):
        """

        Parameters
        ----------
        name_pair: tuple(str, str)

        Returns
        -------
        Arc

        """
        for arc in self.arcs:
            if arc.name_pair == name_pair:
                return arc
        assert False, f"no arc named {name_pair}"

    def get_arcs_from_name_pairs(self, name_pairs):
        """

        Parameters
        ----------
        name_pairs: list[tuple[str, str]]

        Returns
        -------
        list[Arc]

        """
        arcs = []
        for pair in name_pairs:
            arc = self.get_arc_from_name_pair(pair)
            arcs.append(arc)
        return arcs

    def get_tra_from_name(self, name):
        """

        Parameters
        ----------
        name: str

        Returns
        -------
        Transition

        """
        for tra in self.tras:
            if tra.name == name:
                return tra
        assert False, f"no transition named {name}"

    def get_firing_tras_from_names(self, names):
        """

        Parameters
        ----------
        names: list[str]

        Returns
        -------
        list[Transition]

        """
        return [self.get_tra_from_name(name) for name in names]

    def is_enabled(self, tra):
        """

        Parameters
        ----------
        tra: Transition

        Returns
        -------
        bool

        """
        for arc in tra.in_arcs:
            in_place = self.get_place_from_name(arc.name_pair[0])
            if arc.capacity > in_place.content:
                return False
        return True

    def describe_current_markings(self):
        """

        Returns
        -------
        None

        """
        print("current markings:",
              [(p.name, f"{p.content:.2f}") for p in self.places])

    def fire_transition(self, tra):
        """

        Parameters
        ----------
        tra; Transition

        Returns
        -------
        None

        """
        if not self.is_enabled(tra):
            print(f"Transition {tra.name} is not enabled!")
            return
        else:
            print(f"Fired transition {tra.name}.")
        # print("==========", tra.name)
        # self.describe_current_markings()
        for arc in tra.in_arcs:
            # print("====in arc=", arc)
            in_place = self.get_place_from_name(arc.name_pair[0])
            in_place.content -= arc.capacity

        for arc in tra.out_arcs:
            # print("====out arc=", arc)
            out_place = self.get_place_from_name(arc.name_pair[1])
            out_place.content += arc.capacity
        # self.describe_current_markings()

    def fire_transition_list(self, firing_tras):
        """

        Parameters
        ----------
        firing_tras: list[Transition]

        Returns
        -------
        None

        """
        for tra in firing_tras:
            self.fire_transition(tra)
        self.describe_current_markings()

    def inner_step(self,
                   firing_tras,
                   inv_arcs=None):
        """

        Parameters
        ----------
        firing_tras: list[Transition]
        inv_arcs: list[Arc]

        Returns
        -------
        None

        """
        global step_num
        print("step_num=", step_num)
        assert firing_tras is not None
        if step_num > len(firing_tras):
            return
        if step_num != 0:
            tra = firing_tras[step_num - 1]
            self.fire_transition(tra)
        self.describe_current_markings()
        self.draw(jupyter=True, inv_arcs=inv_arcs)
        step_num += 1

    def write_dot_file(self,
                       fname,
                       inv_arcs=None,
                       omit_unit_caps=False,
                       place_shape="circle",
                       num_grays=10):
        """

        Parameters
        ----------
        fname: str
        inv_arcs: list[Arc]
        omit_unit_caps: bool
        place_shape: str
        num_grays: int

        Returns
        -------
        None

        """
        with open(fname, "w") as f:
            str0 = "digraph G {\n"
            for arc in self.arcs:
                ar0, ar1 = arc.name_pair
                # allow for possibility of decimal arrow capacities
                cap = round(arc.capacity)
                inv = arc.inv
                inv_str = ""
                # if inv_arcs:
                # print("nmmjkkkkkkkkk",
                # [str(x) for x in inv_arcs], arc)
                # print(arc in inv_arcs)
                if inv_arcs and (arc in inv_arcs):
                    # print("nmmjk-===============",arc.name_pair)
                    ar0, ar1 = ar1, ar0
                    inv = not inv
                    inv_str = ", arrowhead=inv"
                cap_str = f"label={cap}"
                if omit_unit_caps and cap == 1:
                    cap_str = ""
                str0 += f"{ar0}->{ar1}[{cap_str}{inv_str}];\n"
            max_content = max([p.content for p in self.places])
            num_grays = max(max_content, num_grays)
            for p in self.places:
                place_str = f"[shape={place_shape}," + \
                            "style=filled," + \
                            "fontcolor=red,"
                tone = get_gray_tone(p.content, num_grays)
                str0 += p.name + place_str + \
                        f'fillcolor="{tone}", ' + \
                        f"label={p.content}];\n"
            for tra in self.tras:
                str0 += tra.name + "[shape=none];\n"
            str0 += "}"
            f.write(str0)

    @staticmethod
    def read_dot_file(fname, verbose=False):
        """

        Parameters
        ----------
        fname: str
        verbose: bool

        Returns
        -------
        PetriNet

        """
        places = []
        arcs = []
        tras = []
        tra_names = []
        with open(fname, "r") as f:
            for line in f:
                line.strip()
                if line:
                    if "->" in line:
                        assert "[" in line and "]" in line, \
                            "[] must be in same line"
                        capacity = get_label_value(line)
                        inv = ("arrowhead=inv" in line)
                        nd1, x = line.split("->")
                        nd2 = x.split("[")[0]
                        arc = Arc((nd1.strip(),
                                   nd2.strip()),
                                  capacity,
                                  inv)
                        arcs.append(arc)
                    elif "fontcolor=red" in line:
                        assert "[" in line and "]" in line, \
                            "[] must be in same line"
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
                if arc.name_pair[0] in pnames and \
                        arc.name_pair[1] == tra_name:
                    in_arcs.append(arc)
                elif arc.name_pair[1] in pnames and \
                        arc.name_pair[0] == tra_name:
                    out_arcs.append(arc)
            tra = Transition(tra_name, in_arcs, out_arcs)
            tras.append(tra)
        pat = (places, arcs, tras)
        if verbose:
            describe_PAT(*pat)
        return PetriNet(*pat)

    def draw(self, jupyter,
             inv_arcs=None,
             omit_unit_caps=False,
             place_shape="circle",
             num_grays=10):
        """

        Parameters
        ----------
        jupyter: bool
        inv_arcs: list[Arc]
        omit_unit_caps: bool
        place_shape: str
        num_grays: int

        Returns
        -------
        None

        """
        fname = "tempo.txt"
        self.write_dot_file(fname,
                            inv_arcs=inv_arcs,
                            omit_unit_caps=omit_unit_caps,
                            place_shape=place_shape,
                            num_grays=num_grays)
        draw_dot_file(fname, jupyter=jupyter)


if __name__ == "__main__":
    def main1():
        fname1 = "dot_atlas/PN_fork(1).txt"
        places = [Place("p1", 5), Place("p2", 1), Place("p3", 1)]
        arc1 = Arc(("p1", "x1"), 1, False)
        arc2 = Arc(("x1", "p2"), 1, False)
        arc3 = Arc(("x1", "p3"), 1, False)
        arcs = [arc1, arc2, arc3]
        in_arcs = [arc1]
        out_arcs = [arc2, arc3]
        tra = Transition("x1", in_arcs, out_arcs)
        tras = [tra]
        pnet = PetriNet(places, arcs, tras)
        pnet.write_dot_file(fname1)

        pnet.describe_current_markings()
        pnet.fire_transition(tra)
        pnet.describe_current_markings()


    def main2():
        fname1 = "dot_atlas/PN_fork(1).txt"
        print("\nread test:")
        pnet = PetriNet.read_dot_file(fname1, verbose=True)
        pnet.draw(jupyter=False)


    main1()
    main2()
