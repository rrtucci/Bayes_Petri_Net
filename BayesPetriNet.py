from PetriNet import *
from BNetPetrifier import *
import random


class BayesPetriNet(PetriNet):

    def __init__(self,
                 bnet_pa_to_children,
                 cond_bnet_nds=None,
                 buffer_nd_to_content=None,
                 petri_arrow_to_capacity=None,
                 num_grays=10,
                 verbose=False):
        # petri_arrow_to_capacity = None
        # this will cause all capacities to be set to 1
        # by BNetPetrifier

        self.petrifier = BNetPetrifier(
            bnet_pa_to_children,
            cond_bnet_nds,
            buffer_nd_to_content,
            petri_arrow_to_capacity,
            num_grays,
            verbose)
        super().__init__(*self.petrifier.get_PAT())

    def get_reacheable_out_arcs(self, tra, in_arc):
        assert in_arc in tra.in_arcs
        nd1 = in_arc.name_pair[0].split("2")[0]
        nd2 = tra.name
        reachable_out_arcs = []
        for out_arc in tra.out_arcs:
            nd3 = out_arc.name_pair[1].split("2")[1]
            if not self.petrifier.nd2_is_blocked(nd1, nd2, nd3):
                reachable_out_arcs.append(out_arc)
        return reachable_out_arcs

    def fire_transition(self, tra):
        if not self.is_enabled(tra):
            print(f"Transition {tra.name} is not enabled!")
            return
        else:
            print(f"Fired transition {tra.name}.")

        for in_arc in tra.in_arcs:
            reachable_out_arcs = self.get_reacheable_out_arcs(tra, in_arc)
            num_reachables = len(reachable_out_arcs)
            in_place = self.get_place_from_name(
                in_arc.name_pair[0])
            if reachable_out_arcs:
                for arc in reachable_out_arcs:
                    out_place = self.get_place_from_name(
                        arc.name_pair[1])
                    out_place.content += in_arc.capacity / num_reachables
                in_place.content -= in_arc.capacity
        # self.describe_current_markings()

    def write_dot_file(self,
                       fname,
                       num_grays=10,
                       inv_arcs=None,
                       omit_unit_caps=False,
                       place_shape="circle"):
        assert False, \
            "Use instead the method BNetPetrifier.write_dot_file()"

    @staticmethod
    def read_dot_file(fname, verbose=False):
        assert False, \
            "Use instead the method BNetPetrifier.read_dot_file()"

if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        petrifier = BNetPetrifier(bnet_pa_to_children, verbose=False)
        PAT = petrifier.get_PAT(verbose=False)
        pnet = PetriNet(*PAT)
        tra = pnet.get_tra_from_name("a")
        pnet.describe_current_markings()
        pnet.fire_transition(tra)
        pnet.describe_current_markings()


    main()
