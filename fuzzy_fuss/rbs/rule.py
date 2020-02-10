class Rule(object):
    def __init__(self, name, prop_atoms, prop_connectives, conclusion):
        la = len(prop_atoms)
        lc = len(prop_connectives)
        if not lc == la - 1:
            raise ValueError(f"Improper number of connectives for {la} atoms: expected {la - 1}, got {lc}")

        self.name = name
        self.prop_atoms = prop_atoms
        self.prop_connectives = prop_connectives
        self.conclusion = conclusion

    def __repr__(self):
        def connect(atom):
            return f"({atom[0]} = {atom[1]})"

        pc = self.prop_connectives
        pa = self.prop_atoms

        prop = connect(pa[0])

        for i in range(len(self.prop_connectives)):
            prop += f" {pc[i].upper()}"
            prop += f" {connect(pa[i+1])}"

        return f"{self.name}: {prop} => {connect(self.conclusion)}"
