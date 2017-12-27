# Python 2.7 or Python 3.x

"""
Unittest of parse_lammps_log.parse_log

Adapted from/inspired by pymatgen:
https://github.com/materialsproject/pymatgen/blob/master/pymatgen/io/lammps/tests/test_output.py

Alta Fang, 2017
"""

import os
import unittest
import numpy as np

from parse_lammps_log.parse_log import LammpsLog

test_dir = os.path.join(os.path.dirname(__file__))

class TestParseLog(unittest.TestCase):
    
    def test_log_custom(self):
        """
        Test parsing a LAMMPs log file with thermo_style custom.
        """
        # Create LammpsLog object from log text file
        log_file_custom = os.path.join(test_dir, "test_files", "log.lammps_custom")
        self.log_custom = LammpsLog(log_file=log_file_custom)
        
        # Check fields
        expected_fields = "step time pe ke etotal temp press c_msd[4]".split()
        self.assertEqual(sorted(expected_fields), 
                         sorted(self.log_custom.thermo_data.keys()))
        
        # Code for making the expected data (dict values sorted by dict keys)
        #np.savetxt(os.path.join(test_dir, "log_custom_data.txt"), 
        #           np.stack([v[1] for v 
        #                     in sorted(self.log_custom.thermo_data.items())])[0])  
        
        # Check data
        expected_data = np.loadtxt(os.path.join(test_dir, "test_files", 
                                                "log_custom_data.txt"))
        np.testing.assert_allclose(expected_data, np.stack([v[1] for v 
                                   in sorted(self.log_custom.thermo_data.items())])[0])    
                                      
    def test_log_multi(self):
        """
        Test parsing a LAMMPs log file with thermo_style multi.
        """
        # Create LammpsLog object from log text file
        log_file_multi = os.path.join(test_dir, "test_files", "log.lammps_multi")
        self.log_multi = LammpsLog(log_file=log_file_multi)
        
        # Check fields
        expected_fields = "Step CPU TotEng KinEng Temp PotEng E_bond E_angle \
                           E_dihed E_impro E_vdwl E_coul E_long Press \
                           Volume".split()
        self.assertEqual(sorted(expected_fields), 
                         sorted(self.log_multi.thermo_data.keys()))                   
        
        # Code for making the expected data (dict values sorted by dict keys)
        #np.savetxt(os.path.join(test_dir, "log_multi_data.txt"), 
        #           np.stack([v[1] for v 
        #                     in sorted(self.log_multi.thermo_data.items())])[0])  
        
        # Check data
        expected_data = np.loadtxt(os.path.join(test_dir, "test_files", 
                                                "log_multi_data.txt"))
        np.testing.assert_allclose(expected_data, np.stack([v[1] for v 
                                   in sorted(self.log_multi.thermo_data.items())])[0])  
                                    
    def test_log_one(self):
        """
        Test parsing a LAMMPs log file with thermo_style one.
        """
        # Create LammpsLog object from log text file
        log_file_one = os.path.join(test_dir, "test_files", "log.lammps_one")
        self.log_one = LammpsLog(log_file=log_file_one)  
        
        # Code for making the expected data (dict values sorted by dict keys)
        #np.savetxt(os.path.join(test_dir, "log_one_data.txt"), 
        #           np.stack([v[1] for v 
        #                     in sorted(self.log_one.thermo_data.items())])[0])  
        
        # Check data
        expected_data = np.loadtxt(os.path.join(test_dir, "test_files", 
                                                "log_one_data.txt"))
        np.testing.assert_allclose(expected_data, np.stack([v[1] for v 
                                   in sorted(self.log_one.thermo_data.items())])[0])  
        
if __name__ == '__main__':
    unittest.main()