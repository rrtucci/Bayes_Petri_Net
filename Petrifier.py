

class Petrifier:
    def __init__(self,
                 bnet_pa_to_children,
                 num_grays=10,
                 place_to_content=None,
                 verbose=False):
        self.bnet_pa_to_children = bnet_pa_to_children
        self.num_grays = num_grays
        assert (self.num_grays >= 2)
        self.place_to_content = place_to_content
        self.verbose = verbose
        
        self.bnet_arrows = []
        self.place_names = []

        for pa, children in bnet_pa_to_children.items():
            self.bnet_arrows += [(pa, ch) for ch in children]
        for (pa, ch) in self.bnet_arrows:
            self.place_names.append(pa + "2" + ch)
            self.place_names.append(ch + "2" + pa)
        if verbose:
            print("bnet_arrows=", self.bnet_arrows)
            print("place_names=", self.place_names)

        if place_to_content is None:
            self.place_to_content = \
                {place:1 for place in self.place_names}
        else:
            for place in range(len(self.place_names)):
                if place not in place_to_content:
                    place_to_content[place]=1
        if verbose:
            print("place_to_content=", self.place_to_content)
        max_content = max(self.place_to_content.values())
        if max_content > self.num_grays:
            self.num_grays = max_content

        self.bnet_nds = []
        for pa, children in self.bnet_pa_to_children.items():
            if pa not in self.bnet_nds:
                self.bnet_nds.append(pa)
            for ch in children:
                if ch not in self.bnet_nds:
                    self.bnet_nds.append(ch)
        if verbose:
            print("bnet_nds=", self.bnet_nds)


    def get_gray_tone(self, i):

        if i < 0 or i >= self.num_grays:
            raise ValueError("i should be in the range [0, num_grays]")
        tone_value = int((self.num_grays-i-1)*255/ (self.num_grays-1))
        hex_value = f"{tone_value:02x}"  # Convert to 2-digit hex
        return f"#{hex_value}{hex_value}{hex_value}"  # Return the gray color

    def write_petrified_bnet_file(self, out_fname, red_upstream=True):
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

                if not red_upstream:
                    str0 += ar[1] + "->" + upstream_nd
                    str0 += "[style=dotted];\n"
                    str0 += upstream_nd + "->" + ar[0]
                    str0 += "[style=dotted];\n"
                else:
                    str0 += ar[0] + "->" + upstream_nd
                    str0 += "[style=dotted, color=red];\n"
                    str0 += upstream_nd + "->" + ar[1]
                    str0 += "[style=dotted, color=red];\n"

                str0 += ar[0] + "[shape=none];\n"
                str0 += ar[1] + "[shape=none];\n"

                u_content= self.place_to_content[upstream_nd]
                d_content = self.place_to_content[downstream_nd]
                str1 = "[shape=circle, style=filled, fontcolor=red, "
                str0 += downstream_nd + str1 + \
                        f'fillcolor="{self.get_gray_tone(d_content)}", ' +\
                        f"label={d_content}];\n"
                str0 += upstream_nd + str1 + \
                        f'fillcolor="{self.get_gray_tone(u_content)}", ' + \
                        f"label={u_content}];\n"
            str0 += "}"
            f.write(str0)

if __name__ == "__main__":
    def main():
        bnet_pa_to_children = {"a": ["b", "c"],
                               "b": ["c", "d"],
                               "c": "d"}
        out_fname = "petri_bayes.txt"
        pfier = Petrifier(bnet_pa_to_children, verbose=True)
        print("gray_tones=",
            [pfier.get_gray_tone(i) for i in range(pfier.num_grays)])

        pfier.write_petrified_bnet_file(out_fname)

    main()




