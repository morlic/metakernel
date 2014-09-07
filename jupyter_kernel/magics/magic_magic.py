# Copyright (c) Calico Development Team.
# Distributed under the terms of the Modified BSD License.
# http://calicoproject.org/

from jupyter_kernel import Magic


class MagicMagic(Magic):

    def line_magic(self):
        """%magic - show installed magics"""
        line_magics = []
        cell_magics = []

        for (name, magic) in self.kernel.line_magics.items():
            line_magics.append(magic.get_help('line', name))
        for (name, magic) in self.kernel.cell_magics.items():
            cell_magics.append(magic.get_help('cell', name))

        self.kernel.Print("Line magics:")
        self.kernel.Print("    " + ("\n    ".join(sorted(line_magics))))
        self.kernel.Print("")
        self.kernel.Print("Cell magics:")
        self.kernel.Print("    " + ("\n    ".join(sorted(cell_magics))))
        self.kernel.Print("")
        self.kernel.Print("Shell shortcut:")
        self.kernel.Print("    ! COMMAND ... - execute command in shell")
        self.kernel.Print("")
        self.kernel.Print(
            "Any cell magic can be made persistent for rest of session by using %%% prefix.")
        self.kernel.Print("")
        self.kernel.Print("Help on items:")
        for string in self.kernel.line_magics['help'].help_strings():
            self.kernel.Print("    " + string)
        self.kernel.Print("")

    def get_magic(self, info):

        if not info['magic']:
            return None

        minfo = info['magic']
        name = minfo['name']
        if minfo['type'] == 'sticky':
            sname = '%%' + name
            if sname in self.kernel.sticky_magics:
                del self.kernel.sticky_magics[sname]
                self.kernel.Print("%s removed from session magics.\n" % sname)
                # dummy magic to eat this line and continue:
                return Magic(self.kernel)
            else:
                self.kernel.sticky_magics[sname] = minfo['args']
                self.kernel.Print("%s added to session magics.\n" % name)

        cell_magics = self.kernel.cell_magics
        line_magics = self.kernel.line_magics
        if minfo['type'] in ['cell', 'sticky'] and name in cell_magics.keys():
            magic = cell_magics[name]
        elif minfo['type'] == 'line' and name in line_magics.keys():
            magic = line_magics[name]

        else:
            # FIXME: Raise an error
            return None
        return magic.call_magic(minfo['type'], minfo['name'],
                                minfo['code'], minfo['args'])


def register_magics(kernel):
    kernel.register_magics(MagicMagic)
