class Petrifier:
    def __init__(self,
                 bnet_pa_to_children,
                 ar_to_multiplicity=None):
        self.bnet_arrows = []
        self.petri_nds = []
        self.ar_to_multiplicity = ar_to_multiplicity
        for pa, children in bnet_pa_to_children.items():
            self.bnet_arrows += [(pa, ch) for ch in children]
        for (pa, ch) in self.bnet_arrows:
            self.petri_nds.append(pa + "2" + ch)
            self.petri_nds.append(ch + "2" + pa)

        if ar_to_multiplicity is None:
            self.ar_to_multiplicity = \
                {ar:1 for ar in self.petri_nds}
        else:
            assert set(self.petri_nds) == set(ar_to_multiplicity.keys())
        print(self.bnet_arrows)
        print(self.petri_nds)

    def write_petrified_bnet_file(self, out_fname):
        with open(out_fname, "w") as f:
            str0 = "digraph G {\n"
            for ar in self.bnet_arrows:
                str0 += ar[0] + "->" + ar[1] + ";\n"
                upstream_nd = ar[1] + "2" + ar[0]
                downstream_nd = ar[0] + "2" + ar[1]
                str0 += ar[0] + "->" + downstream_nd
                str0 += "[style=dotted];\n"
                str0 += downstream_nd + "->" + ar[1]
                str0 += "[style=dotted];\n"

                str0 += ar[1] + "->" + upstream_nd
                str0 += "[style=dotted];\n"
                str0 += upstream_nd + "->" + ar[0]
                str0 += "[style=dotted];\n"

                str0 += ar[0] + "[shape=none];\n"
                str0 += ar[1] + "[shape=none];\n"

                str0 += downstream_nd + f"[label=" \
                        f"{self.ar_to_multiplicity[downstream_nd]}];\n"
                str0 += upstream_nd + f"[label=" \
                        f"{self.ar_to_multiplicity[upstream_nd]}];\n"
                str1 = "[shape=circle, style=dotted, style=filled, " \
                       "fontcolor=red, fillcolor=skyblue];"
                str0 += downstream_nd + str1 + "\n"
                str0 += upstream_nd + str1 + "\n"
            str0 += "}"
            f.write(str0)

if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        ar_multiplicity = None
        out_fname = "petri_bayes.txt"
        pfier = Petrifier(bnet_pa_to_children, ar_multiplicity)


        pfier.write_petrified_bnet_file(out_fname)

    main()




