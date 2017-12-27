"""
Example usage of LAMMPs log parser.
"""

from matplotlib import pyplot
from parse_lammps_log.parse_log import LammpsLog

log_data = LammpsLog(log_file="example_files/log.lammps").thermo_data

pyplot.plot(log_data["step"], log_data["etotal"])
pyplot.xlabel("step")
pyplot.ylabel("total energy")
pyplot.tight_layout()
pyplot.show()
