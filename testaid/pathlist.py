class PathList(object):

    def __init__(self,
                 pathstring,
                 molecule_scenario_directory):
        self._molecule_scenario_directory = molecule_scenario_directory
        self._pathlist = self._pathstring_to_pathlist_(pathstring)

    def get(self):
        return self._pathlist

    def _get_molecule_scenario_directory_(self):
        return self._molecule_scenario_directory

    def _pathstring_to_pathlist_(self, pathstring):
        '''Returns list of yaml files with extra vars'''
        pathlist = list()
        base_dir = self._get_molecule_scenario_directory_()
        for item in str(pathstring).split(':'):
            path = base_dir / item
            path = path.resolve()
            if path.is_file():
                pathlist.append(path)
            if path.is_dir():
                filelist = path.glob('**/*.yml')
                for file in filelist:
                    pathlist.append(file.resolve())

        return sorted(pathlist)
