from PetriNet import *
from BNetPetrifier import *


class BayesPetriNet(PetriNet):

    def __init__(self,
                 bnet_pa_to_children,
                 bnet_nd_to_cond_flag=None,
                 buffer_nd_to_content=None,
                 petri_arrow_to_capacity=None,
                 num_grays=10,
                 verbose=False):
        petrifier = BNetPetrifier(
            bnet_pa_to_children,
            bnet_nd_to_cond_flag,
            buffer_nd_to_content,
            petri_arrow_to_capacity,
            num_grays,
            verbose)
        super().__init__(*petrifier.get_PAT())

    def is_blocked(self, tra):
        pass

    def fire_transition(self, tra):
        pass

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
