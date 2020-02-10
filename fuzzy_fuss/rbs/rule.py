class Atom(tuple):
    def __init__(self, vals):
        if len(vals) != 2:
            raise ValueError(f"Expected a length 2 argument, got length {len(vals)}: {vals}")

    def __repr__(self):
        return f"({self[0]} = {self[1]})"


class Rule(object):
    def __init__(self, name, prop_atoms, prop_connectives, conclusion):
        la = len(prop_atoms)
        lc = len(prop_connectives)
        if not lc == la - 1:
            raise ValueError(f"Improper number of connectives for {la} atoms: expected {la - 1}, got {lc}")

        self.name = name
        self.prop_atoms = tuple(Atom(a) for a in prop_atoms)
        self.prop_connectives = prop_connectives
        self.conclusion = conclusion

    def __repr__(self):
        pc = self.prop_connectives
        pa = self.prop_atoms

        prop = str(pa[0])

        for i in range(len(self.prop_connectives)):
            prop += f" {pc[i].upper()}"
            prop += f" {str(pa[i+1])}"

        return f"{self.name}: {prop} => {str(self.conclusion)}"
