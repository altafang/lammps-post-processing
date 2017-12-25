# Python 3.x

"""
Unittest of LAMMPs log parsing tools
"""

import os
import unittest
import numpy as np

from parse_lammps_log.parse_log import LammpsLog

test_dir = os.path.join(os.path.dirname(__file__))

class TestParseLog(unittest.TestCase):

    def setUp(self):
        log_file_custom = os.path.join(test_dir, "log.lammps_custom")
        self.log_custom = LammpsLog(log_file=log_file_custom)
        
        log_file_multi = os.path.join(test_dir, "log.lammps_multi")
        self.log_multi = LammpsLog(log_file=log_file_multi)
    
    def test_log_custom(self):
        """
        Test parsing a LAMMPs log file.
        
        Adapted from/inspired by pymatgen:
        https://github.com/materialsproject/pymatgen/blob/master/pymatgen/io/lammps/tests/test_output.py
        """
        
        # Check fields
        expected_fields = "step time pe ke etotal temp press c_msd[4]".split()
        self.assertEqual(sorted(expected_fields), 
                         sorted(self.log_custom.thermo_data.keys()))
        
        # Code for making the expected data
        #np.savetxt(os.path.join(test_dir, "log_custom_data.txt"), 
        #            np.dstack(tuple(self.log.thermo_data.values()))[0])  
        
        # Check data
        expected_data = np.loadtxt(os.path.join(test_dir, "log_custom_data.txt"))
        np.testing.assert_allclose(expected_data, np.dstack(
                                   tuple(self.log_custom.thermo_data.values()))[0])  
                                      
    def test_log_multi(self):
        # Code for making the expected data
        #np.savetxt(os.path.join(test_dir, "log_multi_data.txt"), 
        #           np.dstack(tuple(self.log_multi.thermo_data.values()))[0])
        
        # Check data
        expected_data = np.loadtxt(os.path.join(test_dir, "log_multi_data.txt"))
        np.testing.assert_allclose(expected_data, np.dstack(
                                   tuple(self.log_multi.thermo_data.values()))[0])  
        
if __name__ == '__main__':
    unittest.main()