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

    def fire_transition(self, tra):
        if not self.is_enabled(tra):
            print(f"Transition {tra.name} is not enabled!")
            return
        else:
            print(f"Fired transition {tra.name}.")

        for in_arc in tra.in_arcs:
            nd1 = in_arc.name_pair[0].split("2")[0]
            nd2 = tra.name
            unblocked_out_arcs = []
            for out_arc in tra.out_arcs:
                nd3 = out_arc.name_pair[1].split("2")[1]
                if not self.petrifier.nd2_is_blocked(nd1, nd2, nd3):
                    unblocked_out_arcs.append(out_arc)
            if unblocked_out_arcs:
                lucky_out_arc = random.choice(unblocked_out_arcs)
            else:
                lucky_out_arc = None
            if lucky_out_arc:
                in_place = self.get_place_from_name(
                    in_arc.name_pair[0])
                out_place = self.get_place_from_name(
                    lucky_out_arc.name_pair[1])
                in_place.content -=1
                out_place.content += 1
        # self.describe_current_markings()


    def write_dot_file(self,
                       fname,
                       num_grays=10,
                       inv_arcs=None):
        assert False

    def read_dot_file(fname, verbose=False):
        pass


if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        petrifier = BNetPetrifier(bnet_pa_to_children, verbose=False)
        PAT = petrifier.get_PAT(verbose=False)
        pnet = PetriNet(*PAT)
        pnet.describe_current_markings()
        pnet.fire_transition(tras[1])
        pnet.describe_current_markings()


    main()
