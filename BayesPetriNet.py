from PetriNet import *
from BNetPetrifier import *


class BayesPetriNet(PetriNet):
    """
    This class defines a Bayes Petri Net.

    Note that even though this is a subclass of PetriNet, the parameters of 
    its __init__ constructor are not the same as those of the __init__ of 
    PetriNet. Instead, they are the same as those of the __init__ of 
    BNetPetrifier. The __init__ of this class uses its input parameters to 
    immediately create self.petrifier.


    Attributes
    ----------
    petrifier: BNetPetrifier
    """

    def __init__(self,
                 bnet_pa_to_children,
                 cond_bnet_nds=None,
                 buffer_nd_to_content=None,
                 petri_arrow_to_capacity=None,
                 verbose=False):
        """
        Constructor. See input parameter of the __init__ of BnetPetrifier
        which are the same as those for this __init__.

        Parameters
        ----------
        bnet_pa_to_children: dict[str, list[str]]
        cond_bnet_nds: list[str]
        buffer_nd_to_content: dict[str, int|float]
        petri_arrow_to_capacity: dict[tuple[str,str], int]
        verbose: bool
        """
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

    def refresh_petrifier_markings(self):
        """
        This method refreshes the markings of self.petrifier. It is used
        whenever the markings (i.e., self.place.content) of the self.places
        have changed but its equivalents in self.petrifier haven't been
        changed yet.

        Returns
        -------
        None

        """
        for place in self.places:
            self.petrifier.buffer_nd_to_content[place.name] = \
                place.content

    def get_reachable_out_arcs(self, tra, in_arc):
        """
        This method returns a list of the reachable outgoing arcs for a
        given transition `tra` and an in arc `in_arc`. An outgoing arc is
        reachable if it is not blocked, judging by Pearl's rules for
        d-separation.

        Parameters
        ----------
        tra: Transition
        in_arc: Arc

        Returns
        -------
        list[Arc]

        """
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
        """
        This method performs a single "step"; i.e., it fires a single
        transition node `tra`.

        Parameters
        ----------
        tra: Transition

        Returns
        -------
        None

        """
        check_fully_enabled = False
        if check_fully_enabled and not self.is_enabled(tra):
            print(f"Transition {tra.name} is not fully enabled!")
            return
        else:
            print(f"Fired transition {tra.name}.")

        for in_arc in tra.in_arcs:
            if not self.is_enabled(tra, in_arc):
                pass
            else:
                reachable_out_arcs =\
                    self.get_reachable_out_arcs(tra, in_arc)
                num_reachables = len(reachable_out_arcs)
                in_place = self.get_place_from_name(
                    in_arc.name_pair[0])
                if reachable_out_arcs and self.is_enabled(tra, in_arc):
                    for arc in reachable_out_arcs:
                        out_place = self.get_place_from_name(
                            arc.name_pair[1])
                        out_place.content += \
                            in_arc.capacity / num_reachables
                    in_place.content -= in_arc.capacity
        self.refresh_petrifier_markings()
        # self.describe_current_markings()

    def write_dot_file(self,
                       fname,
                       inv_arcs=None,
                       omit_unit_caps=False,
                       place_shape="circle",
                       num_grays=10):
        """
        This method just calls self.petrifier.write_dot_file(). It overrides
        the method of the same name in the parent class PetriNet.

        If you input something other than None for the parameter `inv_arcs`,
        it won't be used as the inv arcs of a Bayes Petri Net are determined
        by the program, not inputed by the user as they are in PetriNet.

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
        self.petrifier.write_dot_file(
            fname=fname,
            omit_unit_caps=omit_unit_caps,
            place_shape=place_shape,
            num_grays=num_grays)

    @staticmethod
    def read_dot_file(fname, verbose=False):
        """
        This method just calls self.petrifier.read_dot_file().  It overrides
        the method of the same name in the parent class PetriNet,
        but instead of returning a PetriNet object, it returns a
        BayesPetriNet object.

        Parameters
        ----------
        fname: str
        verbose: bool

        Returns
        -------
        BayesPetriNet

        """
        BNetPetrifier.read_dot_file(fname=fname, verbose=verbose)

    def draw(self, jupyter,
             inv_arcs=None,
             omit_unit_caps=False,
             place_shape="circle",
             num_grays=10):
        """
        This method just calls self.petrifier.draw(). It overrides the
        method of the same name in the parent class PetriNet.

        If you input something other than None for the parameter `inv_arcs`,
        it won't be used at all because the inv arcs of a Bayes Petri Net
        are determined by the program, not inputed by the user as they are
        in a PetriNet.

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
        self.petrifier.draw(
            jupyter=jupyter,
            omit_unit_caps=omit_unit_caps,
            place_shape=place_shape,
            num_grays=num_grays)

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
