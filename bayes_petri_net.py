from Petrifier import *
from generic_petri_net import *

def get_places_tras_arcs(pfier, verbose=False):
    places = []
    for name, content in pfier.place_to_content.items():
        place = Place(name, content)
        places.append(place)

    arcs=[]
    for name in pfier.place_names:
        x1, x2 = name.split("2")
        arc = Arc((x1, name), capacity=1)
        arcs.append(arc)
        arc = Arc((name, x2), capacity=1)
        arcs.append(arc)

    tras = []
    for tra_name in pfier.bnet_nds:
        in_arcs = []
        out_arcs = []
        for name in pfier.place_names:
            x1, x2 = name.split("2")
            if x2 == tra_name:
                in_arc = Arc((x1, name), capacity=1)
                in_arcs.append(in_arc)
            if x1 == tra_name:
                out_arc = Arc((name, x2), capacity=1)
                out_arcs.append(out_arc)
        tra = Transition(tra_name, in_arcs, out_arcs)
        tras.append(tra)
    if verbose:
        print("\nplaces:")
        for p in places:
            print(p)
        print("\narcs:")
        for a in arcs:
            print(a)
        print("\ntransitions:")
        for tra in tras:
            tra.describe_self()
    return places, tras, arcs

if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        pfier = Petrifier(bnet_pa_to_children)
        places, tras, arcs = get_places_tras_arcs(pfier, verbose=True)
        pnet = Petri_Net(places, tras, arcs)

    main()

