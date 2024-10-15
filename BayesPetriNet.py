from PetriNet import *
from BNetPetrifier import *
import random


class BayesPetriNet(PetriNet):

    def __init__(self,
                 bnet_pa_to_children,
                 cond_bnet_nds=None,
                 buffer_nd_to_content=None,
                 petri_arrow_to_capacity=None,
                 verbose=False):
        # petri_arrow_to_capacity = None
        # this will cause all capacities to be set to 1
        # by BNetPetrifier

        self.petrifier = BNetPetrifier(
            bnet_pa_to_children,
            cond_bnet_nds,
            buffer_nd_to_content,
            petri_arrow_to_capacity,
            verbose)
        super().__init__(*self.petrifier.get_PAT())

    def get_reacheable_out_arcs(self, tra, in_arc):
        assert in_arc in tra.in_arcs
        nd1 = in_arc.name_pair[0].split("_")[0]
        nd2 = tra.name
        reachable_out_arcs = []
        for out_arc in tra.out_arcs:
            nd3 = out_arc.name_pair[1].split("_")[1]
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

    def inner_step(self,
                   firing_tras,
                   inv_arcs=None):
        global step_num
        print("step_num=", step_num)
        assert firing_tras is not None
        if step_num > len(firing_tras):
            return
        if step_num != 0:
            tra = firing_tras[step_num - 1]
            self.fire_transition(tra)
        self.describe_current_markings()
        self.petrifier.draw(jupyter=True)
        step_num += 1


    def write_dot_file(self,
                       fname,
                       inv_arcs=None,
                       omit_unit_caps=False,
                       place_shape="circle",
                       num_grays=10):
        assert False, \
            "Use instead the method BNetPetrifier.write_dot_file()"

    @staticmethod
    def read_dot_file(fname, verbose=False):
        assert False, \
            "Use instead the method BNetPetrifier.read_dot_file()"

    def draw(self, jupyter,
             inv_arcs=None,
             omit_unit_caps=False,
             place_shape="circle"):
        assert False, \
            "Use instead the method BNetPetrifier.draw()"


if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        bpnet = BayesPetriNet(bnet_pa_to_children, verbose=False)
        tra = bpnet.get_tra_from_name("b")
        bpnet.describe_current_markings()
        bpnet.fire_transition(tra)
        bpnet.describe_current_markings()

    main()
