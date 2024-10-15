class Place:
    """

    Attributes
    ----------
    content: int|float
    name: str

    """
    def __init__(self, name, content):
        """

        Parameters
        ----------
        name: str
        content: int|float
        """
        self.name = name
        self.content = content

    def __str__(self):
        """

        Returns
        -------
        str

        """
        return f"({self.name}, {self.content})"


class Arc:
    """
    Attributes
    ----------
    capacity: int
    inv: bool
    name_pair: tuple[str, str]

    """
    def __init__(self, name_pair, capacity, inv):
        """

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

        Returns
        -------
        str

        """
        return f"({self.name_pair}, {self.capacity}, {self.inv})"

    def __eq__(self, other):
        """

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

        Returns
        -------
        None

        """
        self.inv = not self.inv
        self.name_pair = (self.name_pair[1], self.name_pair[0])


class Transition:
    """
    Attributes
    ----------
    in_arcs: list[Arc]
    name: str
    out_arcs: list[Arc]

    """
    def __init__(self,
                 name,
                 in_arcs,
                 out_arcs):
        """

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
