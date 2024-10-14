from utils import get_gray_tone, complete_dict, reverse_pair
from utils import get_pa_to_descendants
from PAT import *

class BNetPetrifier:
    def __init__(self,
                 bnet_pa_to_children,
                 cond_bnet_nds=None,
                 buffer_nd_to_content=None,
                 petri_arrow_to_capacity=None,
                 num_grays=10,
                 verbose=False):
        self.bnet_pa_to_children = bnet_pa_to_children
        self.cond_bnet_nds = cond_bnet_nds
        self.buffer_nd_to_content = buffer_nd_to_content
        self.petri_arrow_to_capacity = petri_arrow_to_capacity
        self.num_grays = num_grays
        assert (self.num_grays >= 2)
        self.verbose = verbose

        self.bnet_nds = []
        self.bnet_arrows = []
        self.buffer_nds = []
        self.petri_arrows = []
        self.inv_petri_arrows = []

        for pa, children in self.bnet_pa_to_children.items():
            if pa not in self.bnet_nds:
                self.bnet_nds.append(pa)
            for ch in children:
                if ch not in self.bnet_nds:
                    self.bnet_nds.append(ch)
        if verbose:
            print("bnet_nds=", self.bnet_nds)
            print("cond_bnet_nds=", self.cond_bnet_nds)

        self.pa_to_descendants = get_pa_to_descendants(
            self.bnet_pa_to_children)
        if verbose:
            print("bnet_pa_to_children=", self.pa_to_descendants)
            
        for pa, children in bnet_pa_to_children.items():
            self.bnet_arrows += [(pa, ch) for ch in children]
        if verbose:
            print("bnet_arrows=", self.bnet_arrows)

        for (pa, ch) in self.bnet_arrows:
            self.buffer_nds.append(pa + "2" + ch)
            self.buffer_nds.append(ch + "2" + pa)
        if verbose:
            print("buffer_nds=", self.buffer_nds)

        for buffer_nd in self.buffer_nds:
            x1, x2 = buffer_nd.split("2")
            ars = [(x1, buffer_nd), (buffer_nd, x2)]
            for ar in ars:
                self.petri_arrows.append(ar)
                if (x1, x2) not in self.bnet_arrows:
                    self.inv_petri_arrows.append(ar)
        if verbose:
            print("petri_arrows=", self.petri_arrows)
            print("inv_petri_arrows=", self.inv_petri_arrows)

        self.buffer_nd_to_content = complete_dict(
            self.buffer_nd_to_content,
            self.buffer_nds,
            1)
        if verbose:
            print("buffer_nd_to_content=", 
                  self.buffer_nd_to_content)
        max_content = max(self.buffer_nd_to_content.values())
        if max_content > self.num_grays:
            self.num_grays = max_content

        self.petri_arrow_to_capacity = complete_dict(
            self.petri_arrow_to_capacity,
            self.petri_arrows,
            1
        )
        if verbose:
            print("petri_arrow_to_capacity=", 
                  self.petri_arrow_to_capacity)

    def get_PAT(self, verbose=False):
        places = []
        for buffer_nd, content in self.buffer_nd_to_content.items():
            place = Place(buffer_nd, content)
            places.append(place)

        def get_arc(petri_arrow):
            inv = petri_arrow in self.inv_petri_arrows
            return Arc(petri_arrow if not inv else reverse_pair(petri_arrow),
                       self.petri_arrow_to_capacity[petri_arrow],
                       inv)
        arcs = []
        for petri_arrow, cap in self.petri_arrow_to_capacity.items():
            arc = get_arc(petri_arrow)
            arcs.append(arc)

        tras = []
        for tra_name in self.bnet_nds:
            in_arcs = []
            out_arcs = []
            for petri_arrow in self.petri_arrows:
                if petri_arrow[0] == tra_name:
                    out_arc = get_arc(petri_arrow)
                    out_arcs.append(out_arc)
                if petri_arrow[1] == tra_name:
                    in_arc = get_arc(petri_arrow)
                    in_arcs.append(in_arc)
            tra = Transition(tra_name, in_arcs, out_arcs)
            tras.append(tra)
        if verbose:
            describe_PAT(places, arcs, tras)
        return places , arcs, tras

    def nd2_is_collider(self, nd1, nd2, nd3):
        if (nd1, nd2) in self.bnet_nds and \
                (nd3, nd2) in self.bnet_nds:
            return True
        else:
            return False

    def nd2_is_blocked(self, nd1, nd2, nd3):
        blocked = True
        if self.nd2_is_collider(nd1, nd2, nd3):
            if nd2 in self.cond_bnet_nds:
                blocked = False
            for des in self.pa_to_descendants[nd2]:
                if des in self.cond_bnet_nds:
                    blocked = False
        else: # not collider
            if nd2 not in self.cond_bnet_nds:
                blocked = False
        return blocked



    def write_dot_file_of_BPN(self, out_fname, red_upstream=True):
        def get_cap_inv_strings(petri_arrow):
            cap_str = f", label=" \
                      f"{self.petri_arrow_to_capacity[petri_arrow]}"
            inv_str = ", arrowhead=inv" if \
                petri_arrow in self.inv_petri_arrows else ""
            return cap_str, inv_str
        with open(out_fname, "w") as f:
            str0 = "digraph G {\n"
            for ar in self.bnet_arrows:
                str0 += ar[0] + "->" + ar[1] + ";\n"
            for petri_arrow in self.petri_arrows:
                if petri_arrow not in self.inv_petri_arrows:
                    str0 += f"{petri_arrow[0]}->{petri_arrow[1]}"
                else:
                    str0 += f"{petri_arrow[1]}->{petri_arrow[0]}"
                cap_str, inv_str = get_cap_inv_strings(petri_arrow)
                str0 += f"[style=dotted{inv_str}{cap_str}];\n"

            for buffer_nd in self.buffer_nds:
                str0 += f"{buffer_nd}["
                str0 += "shape=circle, style=filled, fontcolor=red, "
                content = self.buffer_nd_to_content[buffer_nd]
                tone = get_gray_tone(self.num_grays, content)
                str0 += f'fillcolor="{tone}", label={content}];\n'
            for name in self.bnet_nds:
                if name in self.cond_bnet_nds:
                    color_str = \
                        "[shape=circle, style=filled, color=yellow];\n"
                else:
                    color_str = "[shape=none];\n"
                str0 += name + color_str
            str0 += "}"
            f.write(str0)

if __name__ == "__main__":
    def main1():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        out_fname = "dot_atlas/BPN_wet_grass.txt"
        petrifier = BNetPetrifier(bnet_pa_to_children, verbose=True)
        pat = petrifier.get_PAT(verbose=True)
        petrifier.write_dot_file_of_BPN(out_fname)

    main1()




