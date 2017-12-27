# Python 3.x

"""
Copied and adapted some code from Pymatgen, which has a MIT License. See:
https://github.com/materialsproject/pymatgen/blob/master/pymatgen/io/lammps/output.py

Class for parsing a LAMMPs log file.

Alta Fang, 2017
"""

import re
import os
from io import open

import numpy as np

class LammpsLog:
    """
    Parser for LAMMPS log file.
    """

    def __init__(self, log_file="log.lammps"):
        """
        Args:
            log_file (string): path to the log file
        """
        self.log_file = os.path.abspath(log_file)
        self.timestep = -1
        self._parse_log()

    def _parse_log(self):
        """
        Parse the log file for run and thermodynamic data.
        Automatically detects thermo_style and parses accordingly.
        Sets the thermodynamic data as a dictionary with field names taken from the 
        custom thermo_style command if using thermo_style custom, or the column headings 
        if using thermo_style multi or one.
        
        The thermo_data dictionary contains numpy arrays (not lists as in pymatgen).
        """

        thermo_data = []
        fixes = []
        d_build = None
        thermo_pattern = None
        thermo_multi_keys = None
        with open(self.log_file, 'r') as logfile:
            for line in logfile:
                # Exclude comments
                comment_re = re.search(r"^\s*#+.*", line)
                if comment_re:
                    continue
                # timestep, the unit depedns on the 'units' command
                time = re.search(r'timestep\s+([0-9]+)', line)
                if time and not d_build:
                    self.timestep = float(time.group(1))
                # total number md steps
                steps = re.search(r'run\s+([0-9]+)', line)
                if steps and not d_build:
                    self.nmdsteps = int(steps.group(1))
                # simulation info
                fix = re.search(r'fix.+', line)
                if fix and not d_build:
                    fixes.append(fix.group())
                # dangerous builds
                danger = re.search(r'Dangerous builds\s+([0-9]+)', line)
                if danger and not d_build:
                    d_build = int(danger.group(1)) #XXX BUGFIX ALTA steps --> danger
                # logging interval
                thermo = re.search(r'thermo\s+([0-9]+)', line)
                if thermo and not d_build:
                    self.interval = float(thermo.group(1))
                # thermodynamic data, set by the thermo_style command
                fmt = re.search(r'thermo_style.+', line) 
                if fmt and not d_build:
                    thermo_type = fmt.group().split()[1]
                    # Set up parsing of the appropriate style
                    if thermo_type == "custom":
                        fields = fmt.group().split()[2:]
                        thermo_pattern_string = r"\s*([0-9eE\.+-]+)" + "".join(
                            [r"\s+([0-9eE\.+-]+)" for _ in range(len(fields) - 1)])
                        thermo_pattern = re.compile(thermo_pattern_string)
                    elif thermo_type == "multi": 
                        thermo_multi_keys = "Step CPU TotEng KinEng Temp PotEng E_bond \
                                E_angle E_dihed E_impro E_vdwl E_coul E_long Press \
                                Volume".split()
                        # Create dictionary of empty lists
                        thermo_data.append({key:[] for key in thermo_multi_keys})
                    else: # thermo_style one
                        fields = "Step Temp E_pair E_mol TotEng Press Volume".split() 
                        thermo_pattern_string = r"\s*([0-9eE\.+-]+)" + "".join( \
                            [r"\s+([0-9eE\.+-]+)" for _ in range(len(fields) - 2)]) \
                            + r"\s*([0-9eE\.+-]*)" # Last field, Volume, may not be there
                        thermo_pattern = re.compile(thermo_pattern_string)
                # Parse thermo_style custom or one
                if thermo_pattern:
                    if thermo_pattern.search(line):
                        m = thermo_pattern.search(line)
                        thermo_data.append(tuple([float(x) for x in m.groups() if x]))
                # Parse thermo_style multi
                elif thermo_multi_keys: 
                    step_re = re.search(r'Step\s+([0-9eE]+).+', line)
                    if step_re:
                        step = int(step_re.group(1))
                        thermo_data[-1]['Step'].append(step)
                    remaining_re = re.findall(r'\s*([a-zA-Z_]+)\s+=\s+([0-9eE\.+-]+)\s*', 
                                              line)
                    # Append to the appropriate lists in the dictionary
                    if remaining_re:
                        for tup in remaining_re:
                            if tup[0] in thermo_data[-1].keys():
                                thermo_data[-1][tup[0]].append(float(tup[1]))

        if thermo_data:
            if isinstance(thermo_data[0], tuple): # thermo_style custom or one
                # Concatenate to ensure that thermo_data is the right length
                try:
                    thermo_data = thermo_data[:int(self.nmdsteps/self.interval+1)]
                except AttributeError: # Catch if nmdsteps or interval are not attributes
                    pass
                # Exclude Volume if it's not there
                if len(fields) != len(thermo_data[0]): 
                    fields = fields[:-1]
                self.thermo_data = {fields[i]: np.array([thermo_data[j][i] 
                                    for j in range(len(thermo_data))])
                                    for i in range(len(fields))}
            else: # thermo_style multi
                self.thermo_data = {k:np.array(v) for (k, v) in thermo_data[0].items()
                                    if v} # Exclude Volume if it's empty

        self.fixes = fixes
        self.dangerous_builds = d_build

    def as_dict(self):
        d = {}
        for attrib in [a for a in dir(self)
                       if not a.startswith('__') and not callable(getattr(self, a))]:
            d[attrib] = getattr(self, attrib)
        d["@module"] = self.__class__.__module__
        d["@class"] = self.__class__.__name__
        return d
