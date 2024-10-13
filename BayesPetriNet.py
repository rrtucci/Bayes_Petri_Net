from Petrifier import *
from PetriNet import *

class BayesPetriNet(PetriNet):

if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        pfier = Petrifier(bnet_pa_to_children, verbose=False)
        PAT = pfier.get_petrified_PAT(verbose=False)
        pnet = PetriNet(*PAT)
        pnet.describe_current_markings()
        pnet.fire_transition(tras[1])
        pnet.describe_current_markings()

    main()

