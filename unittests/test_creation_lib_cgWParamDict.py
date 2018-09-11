#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
import unittest2 as unittest
import xmlrunner

# unittest_utils will handle putting the appropriate directories on the python
# path for us.
from glideinwms.unittests.unittest_utils import runTest

from glideinwms.creation.lib.cgWParamDict import glideinDicts
from glideinwms.creation.lib.cgWParamDict import glideinMainDicts
from glideinwms.creation.lib.cgWParamDict import glideinEntryDicts
from glideinwms.creation.lib.cgWParamDict import UnconfiguredScheddError
from glideinwms.creation.lib.cgWParamDict import add_file_unparsed 
from glideinwms.creation.lib.cgWParamDict import add_attr_unparsed 
from glideinwms.creation.lib.cgWParamDict import add_attr_unparsed_real 
from glideinwms.creation.lib.cgWParamDict import iter_to_dict 
from glideinwms.creation.lib.cgWParamDict import populate_factory_descript 
from glideinwms.creation.lib.cgWParamDict import populate_job_descript 
from glideinwms.creation.lib.cgWParamDict import populate_frontend_descript 
from glideinwms.creation.lib.cgWParamDict import populate_gridmap 
from glideinwms.creation.lib.cgWParamDict import validate_condor_tarball_attrs 
from glideinwms.creation.lib.cgWParamDict import old_get_valid_condor_tarballs 
from glideinwms.creation.lib.cgWParamDict import get_valid_condor_tarballs 
from glideinwms.creation.lib.cgWParamDict import itertools_product 
from glideinwms.creation.lib.cgWParamDict import calc_monitoring_collectors_string 
from glideinwms.creation.lib.cgWParamDict import calc_primary_monitoring_collectors 
from glideinwms.creation.lib.factoryXmlConfig import parse

XML = 'fixtures/factory/glideinWMS.xml'
XML_ENTRY = 'fixtures/factory/config.d/Dev_Sites.xml'
XML_ENTRY2 = 'fixtures/factory/config.d/Dev_Sites2.xml'



class TestGlideinMainDicts(unittest.TestCase):
    def setUp(self):
        self.conf = parse(XML)
        self.gmd = glideinMainDicts(self.conf, 'fixtures/factory/work-dir')
    
    def test__init__(self):
        self.assertTrue(isinstance(self.gmd, glideinMainDicts))

    @unittest.skip('need to mock condor_tarball existence')
    def test_populate(self):
        self.gmd.populate()

class TestGlideinEntryDicts(unittest.TestCase):
    def setUp(self):
        self.conf = parse(XML)
        self.ged = glideinEntryDicts(self.conf, '','','/var/lib/gwms-factory/work-dir')
    
    def test__init__(self):
        self.assertTrue(isinstance(self.ged, glideinEntryDicts))

    @unittest.skip('cant seem to find entry config stanza')
    def test_populate(self):
        self.ged.populate(parse(XML), "fermicloud380.fnal.gov")

class TestGlideinDicts(unittest.TestCase):
    def setUp(self):
        self.conf = parse(XML)
        self.ged = glideinDicts(self.conf)
    
    def test__init__(self):
        self.assertTrue(isinstance(self.ged, glideinDicts))

    @unittest.skip('have to mock out condor tarball stuff')
    def test_populate(self):
        self.ged.populate()

class TestAddFileUnparsed(unittest.TestCase):
    @unittest.skip('for now')
    def test_add_file_unparsed(self):
        self.assertEqual(expected, add_file_unparsed(user_file, dicts, is_factory))
        # assert False TODO: implement your test here

class TestAddAttrUnparsed(unittest.TestCase):
    @unittest.skip('for now')
    def test_add_attr_unparsed(self):
        self.assertEqual(expected, add_attr_unparsed(attr, dicts, description))
        # assert False TODO: implement your test here

class TestAddAttrUnparsedReal(unittest.TestCase):
    @unittest.skip('for now')
    def test_add_attr_unparsed_real(self):
        self.assertEqual(expected, add_attr_unparsed_real(attr, dicts))
        # assert False TODO: implement your test here

class TestIterToDict(unittest.TestCase):
    @unittest.skip('for now')
    def test_iter_to_dict(self):
        self.assertEqual(expected, iter_to_dict(dictObject))
        # assert False TODO: implement your test here

class TestPopulateFactoryDescript(unittest.TestCase):
    def test_populate_factory_descript(self):
        work_dir = 'fixtures/factory/work-dir'
        conf = parse(XML)
        ged = glideinMainDicts(conf, work_dir)
        populate_factory_descript(ged.work_dir, ged.dicts['glidein'], ged.active_sub_list, ged.disabled_sub_list, ged.conf)

class TestPopulateJobDescript(unittest.TestCase):
    @unittest.skip('hmmm')
    def test_populate_job_descript(self):
        work_dir = 'fixtures/factory/work-dir'
        conf = parse(XML)
        ged = glideinEntryDicts(conf,'','', work_dir)
        #entry = parse(XML_ENTRY)
        entry = conf
        schedd = "fermicloud173.fnal.gov"
        ged.dicts['job_descript'] = {}
        populate_job_descript(ged.work_dir, ged.dicts['job_descript'], ged.sub_name, entry, schedd)
        #self.assertEqual(expected, populate_job_descript(work_dir, job_descript_dict, sub_name, entry, schedd))
        # assert False TODO: implement your test here

class TestPopulateFrontendDescript(unittest.TestCase):
    def test_populate_frontend_descript(self):
        conf = parse(XML)
        ged = glideinMainDicts(conf, 'fixtures/factory/work-dir') 
        frontend_dict = ged.dicts['frontend_descript']
        populate_frontend_descript(frontend_dict, conf)

class TestPopulateGridmap(unittest.TestCase):
    def test_populate_gridmap(self):
        gridmap_dict = {}
        conf = parse(XML)
        populate_gridmap(conf, gridmap_dict)

class TestValidateCondorTarballAttrs(unittest.TestCase):
    @unittest.skip('for now')
    def test_validate_condor_tarball_attrs(self):
        self.assertEqual(expected, validate_condor_tarball_attrs(conf))
        # assert False TODO: implement your test here

class TestOldGetValidCondorTarballs(unittest.TestCase):
    @unittest.skip('for now')
    def test_old_get_valid_condor_tarballs(self):
        self.assertEqual(expected, old_get_valid_condor_tarballs(params))
        # assert False TODO: implement your test here

class TestGetValidCondorTarballs(unittest.TestCase):
    @unittest.skip('for now')
    def test_get_valid_condor_tarballs(self):
        self.assertEqual(expected, get_valid_condor_tarballs(condor_tarballs))
        # assert False TODO: implement your test here

class TestItertoolsProduct(unittest.TestCase):
    @unittest.skip('for now')
    def test_itertools_product(self):
        self.assertEqual(expected, itertools_product(*args, **kwds))
        # assert False TODO: implement your test here

class TestCalcMonitoringCollectorsString(unittest.TestCase):
    @unittest.skip('for now')
    def test_calc_monitoring_collectors_string(self):
        self.assertEqual(expected, calc_monitoring_collectors_string(collectors))
        # assert False TODO: implement your test here

class TestCalcPrimaryMonitoringCollectors(unittest.TestCase):
    @unittest.skip('for now')
    def test_calc_primary_monitoring_collectors(self):
        self.assertEqual(expected, calc_primary_monitoring_collectors(collectors))
        # assert False TODO: implement your test here

if __name__ == '__main__':
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='unittests-reports'))
