import unittest

from o3webapp_be.back_end import app


class ModelListTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.headers = {'Accept': 'application/json'}
        self.json = {'ptype': 'tco3_zm'}
        self.expected_json = {
            'models': ['CCMI-1_ACCESS-refC2', 'CCMI-1_ACCESS-senC2fGHG', 'CCMI-1_ACCESS-senC2fODS',
                       'CCMI-1_CCCma-CMAM-refC2', 'CCMI-1_CCCma-CMAM-senC2CH4rcp85',
                       'CCMI-1_CCCma-CMAM-senC2fCH4', 'CCMI-1_CCCma-CMAM-senC2fGHG',
                       'CCMI-1_CCCma-CMAM-senC2fN2O', 'CCMI-1_CCCma-CMAM-senC2fODS',
                       'CCMI-1_CCCma-CMAM-senC2rcp26', 'CCMI-1_CCCma-CMAM-senC2rcp45',
                       'CCMI-1_CCCma-CMAM-senC2rcp85', 'CCMI-1_CHASER-MIROC-ESM-refC2',
                       'CCMI-1_CHASER-MIROC-ESM-senC2fCH4', 'CCMI-1_CHASER-MIROC-ESM-senC2fEmis',
                       'CCMI-1_CHASER-MIROC-ESM-senC2fGHG', 'CCMI-1_CHASER-MIROC-ESM-senC2fN2O',
                       'CCMI-1_CHASER-MIROC-ESM-senC2fODS', 'CCMI-1_CNRM-CERFACS-CNRM-CM5-3-refC2',
                       'CCMI-1_CNRM-CERFACS-MOCAGE-refC2', 'CCMI-1_ETH-PMOD-SOCOL3-refC2',
                       'CCMI-1_ETH-PMOD-SOCOL3-senC2CH4rcp85', 'CCMI-1_ETH-PMOD-SOCOL3-senC2fCH4',
                       'CCMI-1_ETH-PMOD-SOCOL3-senC2fEmis', 'CCMI-1_ETH-PMOD-SOCOL3-senC2fN2O',
                       'CCMI-1_ETH-PMOD-SOCOL3-senC2rcp26', 'CCMI-1_ETH-PMOD-SOCOL3-senC2rcp45',
                       'CCMI-1_ETH-PMOD-SOCOL3-senC2rcp85', 'CCMI-1_GSFC-GEOSCCM-refC2',
                       'CCMI-1_IPSL-refC2', 'CCMI-1_IPSL-senC2fGHG', 'CCMI-1_IPSL-senC2fODS',
                       'CCMI-1_IPSL-senC2fODS2000', 'CCMI-1_IPSL-senC2rcp26',
                       'CCMI-1_IPSL-senC2rcp45', 'CCMI-1_IPSL-senC2rcp85',
                       'CCMI-1_MESSy-EMAC-L47MA-refC2', 'CCMI-1_MESSy-EMAC-L90MA-refC2',
                       'CCMI-1_MESSy-EMAC-L90MA-senC2fGHG', 'CCMI-1_MOHC-HadGEM3-ES-refC2',
                       'CCMI-1_MRI-ESM1r1-refC2', 'CCMI-1_NIES-CCSRNIES-MIROC3.2-refC2',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2SlrTrnd',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2fCH4',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2fGHG',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2fN2O',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2fODS',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2fODS2000',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2rcp26',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2rcp45',
                       'CCMI-1_NIES-CCSRNIES-MIROC3.2-senC2rcp85', 'CCMI-1_NIWA-UKCA-refC2',
                       'CCMI-1_NIWA-UKCA-senC2fCH4', 'CCMI-1_NIWA-UKCA-senC2fGHG',
                       'CCMI-1_NIWA-UKCA-senC2fN2O', 'CCMI-1_NIWA-UKCA-senC2fODS',
                       'CCMI-1_U-CAMBRIDGE-UMUKCA-UCAM-refC2', 'CCMI-1_U-LAQUILA-CCM-refC2',
                       'CCMI-1_U-LAQUILA-CCM-senC2GeoMIPG4', 'CCMI-1_U-LAQUILA-CCM-senC2SlrTrnd',
                       'CCMI-1_U-LAQUILA-CCM-senC2fCH4', 'CCMI-1_U-LAQUILA-CCM-senC2fEmis',
                       'CCMI-1_U-LAQUILA-CCM-senC2fGHG', 'CCMI-1_U-LAQUILA-CCM-senC2fN2O',
                       'CCMI-1_U-LAQUILA-CCM-senC2fODS', 'CCMI-1_U-LAQUILA-CCM-senC2rcp26',
                       'CCMI-1_U-LAQUILA-CCM-senC2rcp45', 'CCMI-1_U-LAQUILA-CCM-senC2rcp85',
                       'CCMI-1_U-LEEDS-UMSLIMCAT-refC2', 'CCMI-1_U-LEEDS-UMSLIMCAT-senC2fGHG',
                       'CCMI-1_U-LEEDS-UMSLIMCAT-senC2fODS',
                       'CCMI-1_U-LEEDS-UMSLIMCAT-senC2fODS2000',
                       'CCMI-1_U-LEEDS-UMSLIMCAT-senC2rcp45', 'CCMI-1_U-LEEDS-UMSLIMCAT-senC2rcp85',
                       'ESACCI_DLR-merged-SAT-ozone', 'SBUV_GSFC_merged-SAT-ozone'],
            'vars': [{'name': 'model', 'type': 'array'}, {'name': 'begin', 'type': 'integer'},
                     {'name': 'end', 'type': 'integer'}, {'name': 'month', 'type': 'array'},
                     {'name': 'lat_min', 'type': 'integer'}, {'name': 'lat_max', 'type': 'integer'}]}
        app.config.update(
            TESTING=True
        )

    def test_modellist_tco3zm(self):
        resp = self.client.post('/model_list/tco3_zm', headers=self.headers, json=self.json)

        self.assertEqual(self.expected_json, resp.json)

    def test_tmv_status_code(self):
        resp = self.client.post('/model_list/tco3zm', headers=self.headers, json=self.json)

        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
