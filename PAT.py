class Place:
    """
    This class defines a place node of a Petri net.

    Attributes
    ----------
    content: int|float
        a.k.a. the number of tokens or markings. Note that we will allow
        fractional tokens.
    name: str

    """
    def __init__(self, name, content):
        """
        Constructor

        Parameters
        ----------
        name: str
        content: int|float
        """
        self.name = name
        self.content = content

    def __str__(self):
        """
        Magic method that returns a string describing the place node.

        Returns
        -------
        str

        """
        return f"({self.name}, {self.content})"


class Arc:
    """
    This class defines an arc of a Petri net.


    Attributes
    ----------
    capacity: int
        This is the maximum amount of juice that can flow through the arrow
        in one step (step= firing of one transition)
    inv: bool
        If inv=False and name_pair=('a', 'b'), then the arrow is drawn by
        graphviz pointing from node 'a' to node 'b' and with a standard
        arrowhead. If inv=True and name_pair=('b', 'a'), then the arrow is
        drawn by graphviz pointing from node 'b' to node 'a' and with an
        inverted arrowhead. Both cases are defined to be physically
        identical but are drawn differently by graphviz. We normally ask
        graphviz to draw feedback arrows that point from the present to the
        past in the inverted style. Usng the inverted style for feedback
        arrows yields more pleasing drawings because graphviz by default
        orders the nodes in chronological (i.e. topological order with time
        pointing from top to bottom.
    name_pair: tuple[str, str]
        we will refer to this string pair as an "arrow" pointing from the
        first string to the second. The arrow may point from a place node to
        a transition node or vice versa.

    """
    def __init__(self, name_pair, capacity, inv):
        """
        Constructor

        Parameters
        ----------
        name_pair: tuple[str, str]
        capacity: int
        inv: bool
        """
        self.name_pair = name_pair
        self.capacity = capacity
        self.inv = inv
        if inv:
            self.reverse()

    def __str__(self):
        """
        Magic method that returns a string describing an arc.

        Returns
        -------
        str

        """
        return f"({self.name_pair}, {self.capacity}, {self.inv})"

    def __eq__(self, other):
        """
        Magic method that returns True iff two arcs (self and other) are
        equal in the sense they have equal attributes name_pair, capacity,
        inv. This method is used in bool statements like `arc in arcs`

        Parameters
        ----------
        other: Arc

        Returns
        -------
        bool

        """
        return self.name_pair == other.name_pair and \
            self.capacity == other.capacity and \
            self.inv == other.inv

    def reverse(self):
        """
        This method "reverses" an arc by replacing inv by its negation and
        name_pair by its reverse. Both the new and the old arcs are defined
        to be physically the same but drawn in a different style,
        with different arrowheads.

        Returns
        -------
        None

        """
        self.inv = not self.inv
        self.name_pair = (self.name_pair[1], self.name_pair[0])


class Transition:
    """
    This class defines a transition of a Petri net.


    Attributes
    ----------
    in_arcs: list[Arc]
        list of arcs entering self
    name: str
    out_arcs: list[Arc]
        list of arcs exiting self


    """
    def __init__(self,
                 name,
                 in_arcs,
                 out_arcs):
        """
        Constructor

        Parameters
        ----------
        name: str
        in_arcs: list[Arc]
        out_arcs: list[Arc]
        """
        self.name = name
        self.in_arcs = in_arcs
        self.out_arcs = out_arcs

    def describe_self(self):
        """
        This method prints a description of all the attributes of self.

        Returns
        -------
        None

        """
        print(f"\nname={self.name}")
        print("in_arcs:")
        for arc in self.in_arcs:
            print(arc)
        print("out_arcs:")
        for arc in self.out_arcs:
            print(arc)


def describe_PAT(places, arcs, tras):
    """
    This global method describes a PAT (i.e., places, arcs and transitions).
    Petri nets are defined by a PAT. Note that we will often abbreviate the
    longish word "transition" by a simple "tra".

    Parameters
    ----------
    places: list[Place]
    arcs: list[Arc]
    tras: list[Transition]

    Returns
    -------
    None

    """
    print("\nplaces:")
    for p in places:
        print(p)
    print("\narcs:")
    for a in arcs:
        print(a)
    print("\ntransitions:")
    for tra in tras:
        tra.describe_self()
