from Petrifier import *
from generic_petri_net import *

def get_petrified_places_arcs_tras(pfier, verbose=False):
    places = []
    for pname, content in pfier.place_to_content.items():
        place = Place(pname, content)
        places.append(place)

    arcs=[]
    for pname in pfier.place_names:
        x1, x2 = pname.split("2")
        arc = Arc((x1, pname), capacity=1)
        arcs.append(arc)
        arc = Arc((pname, x2), capacity=1)
        arcs.append(arc)

    tras = []
    for tra_name in pfier.bnet_nds:
        in_arcs = []
        out_arcs = []
        for pname in pfier.place_names:
            x1, x2 = pname.split("2")
            if x2 == tra_name:
                out_arc = Arc((x1, pname), capacity=1)
                out_arcs.append(out_arc)
            if x1 == tra_name:
                in_arc = Arc((pname, x2), capacity=1)
                in_arcs.append(in_arc)
        tra = Transition(tra_name, in_arcs, out_arcs)
        tras.append(tra)
    if verbose:
        PetriNet.describe_PAT(places, arcs, tras)
    return places, arcs, tras

if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        pfier = Petrifier(bnet_pa_to_children, verbose=False)
        places, tras, arcs = get_petrified_places_arcs_tras(pfier,
                                                            verbose=False)
        pnet = PetriNet(places, tras, arcs)
        pnet.describe_current_markings()
        pnet.fire_transition(tras[1])
        pnet.describe_current_markings()

    main()

