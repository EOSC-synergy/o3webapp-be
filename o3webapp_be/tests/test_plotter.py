import unittest
import json
from flask import request
from o3webapp_be.back_end import app
from o3webapp_be import controller,plotData,plotter
from o3webapp_be.controller import PlotController, RemoteController, Tco3ZmController


class TestPlotter(unittest.TestCase):
    def setUp(self):
         obj = {"pType": "tco3_zm",
                "models": [{"model": "CCMI-1_ACCESS-refC2",
                            "style": {"color": "red", "highlighted": "1"}},
                           {"model": "CCMI-1_CCCma-CMAM-refC2",
                            "style": {"color": "green", "highlighted": "0"}},

                           {"model": "CCMI-1_CHASER-MIROC-ESM-refC2",
                            "style": {"color": "yellow", "highlighted": "0"}}],
                "begin": "1989",
                "end": "2100",
                "month": ["7", "9", "11"],
                "lat_min": "-10",
                "lat_max": "10",
                "output": "json"}
         jsonData = json.dumps(obj);
         testobj3 = PlotController(jsonData)
    def test_1(self):
        obj = {"pType": "tco3_zm",
               "models": [{"model": "CCMI-1_ACCESS-refC2",
                           "style": {"color": "red", "highlighted": "1"}},
                          {"model": "CCMI-1_CCCma-CMAM-refC2",
                           "style": {"color": "green", "highlighted": "0"}},

                          {"model": "CCMI-1_CHASER-MIROC-ESM-refC2",
                           "style": {"color": "yellow", "highlighted": "0"}}],
               "begin": "1989",
               "end": "2100",
               "month": ["7", "9", "11"],
               "lat_min": "-10",
               "lat_max": "10",
               "output": "json"}
        jsonData = json.dumps(obj);
        with open('test_data.json', 'w') as json_file:
            json_file.write(jsonData)
        testobj3 = Tco3ZmController(obj)
        layout = testobj3.handle_process()

        self.assertEqual(str(type(layout)), "<class 'flask.wrappers.Response'>")

if __name__ == '__main__':
            unittest.main()
