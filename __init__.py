#!/usr/bin/env python3
# vim: set encoding=utf-8 tabstop=4 softtabstop=4 shiftwidth=4 expandtab
#########################################################################
# Copyright 2013 KNX-User-Forum e.V.            http://knx-user-forum.de/
#########################################################################
#  This file is part of SmartHome.py.    http://mknx.github.io/smarthome/
#
#  SmartHome.py is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  SmartHome.py is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with SmartHome.py. If not, see <http://www.gnu.org/licenses/>.
#########################################################################

import logging
from pyModbusTCP.client import ModbusClient
from pyModbusTCP import utils

logger = logging.getLogger('')


class DimplexWP():

    def __init__(self, smarthome, wp_ip, wp_port=502):
        self._sh = smarthome
        try:
            self._conn = ModbusClient(host = wp_ip, port = wp_port)
            self._conn.open()
        except ValueError:
            logger.info('Fehler mit Host oder Port Parameter')

        self._modbus_dpts = {}

        self._modbusDatapoints = {
            "outdoor_temp" : {"type" : "register", "address" : 1, "count" : 1, "conVal" : 10},
            "return_temp" : {"type" : "register", "address" : 2, "count" : 1, "conVal" : 10},
            "set-point_return_temp" : {"type" : "register", "address" : 53, "count" : 1, "conVal" : 10},
            "hot_water_temp" : {"type" : "register", "address" : 3, "count" : 1, "conVal" : 10},
            "flow_temp" : {"type" : "register", "address" : 5, "count" : 1, "conVal" : 10},
            "heat_source_inlet_temp" : {"type" : "register", "address" : 6, "count" : 1, "conVal" : 10},
            "heat_source_outlet_temp" : {"type" : "register", "address" : 7, "count" : 1, "conVal" : 10},
            "hysteresis" : {"type" : "register", "address" : 47, "count" : 1, "conVal" : 10},
            "heating_rod" : {"type" : "register", "address" : 75, "count" : 1, "conVal" : 1},
            "heat_heating" : {"type" : "register", "address" : 5096, "count" : 3, "conVal" : 1},
            "heat_hot_water" : {"type" : "register", "address" : 5099, "count" : 3, "conVal" : 1},
            "operating_mode" : {"type" : "register", "address" : 5015, "count" : 1, "conVal" : 1},
            "hot_water_hysteresis" : {"type" : "register", "address" : 5045, "count" : 1, "conVal" : 1},
            "hot_water_set-point_temp" : {"type" : "register", "address" : 5047, "count" : 1, "conVal" : 1},
            "status_messages" : {"type" : "register", "address" : 103, "count" : 1, "conVal" : 1},
            "heat_pump_lock" : {"type" : "register", "address" : 104, "count" : 1, "conVal" : 1},
            "alerts" : {"type" : "register", "address" : 105, "count" : 1, "conVal" : 1},
            "sensors" : {"type" : "register", "address" : 106, "count" : 1, "conVal" : 1},
            "outlet_compressor" : {"type" : "coil", "address" : 41, "count" : 1},
            "outlet_primary_pump" : {"type" : "coil", "address" : 43, "count" : 1},
            "outlet_heating_rod" : {"type" : "coil", "address" : 44, "count" : 1},
            "outlet_heating_pump_M13" : {"type" : "coil", "address" : 45, "count" : 1},
            "outlet_hot_water_pump" : {"type" : "coil", "address" : 46, "count" : 1},
            "outlet_add_circ_pump" : {"type" : "coil", "address" : 49, "count" : 1},
            "outlet_heating_pump_M15" : {"type" : "coil", "address" : 51, "count" : 1},
            "outlet_heating_pump_M14" : {"type" : "coil", "address" : 59, "count" : 1},
            "outlet_heating_pump_M20" : {"type" : "coil", "address" : 61, "count" : 1}
        }



    def run(self):
        self.alive = True
        self._sh.scheduler.add('DIMPLEXWP', self._update_values, prio=5, cycle=30)
        # if you want to create child threads, do not make them daemon = True!
        # They will not shutdown properly. (It's a python bug)

    def stop(self):
        self.alive = False
        self._conn.close()

    def parse_item(self, item):
        if 'wp_modbus_dpt' in item.conf:
            logger.debug("parse item: {0}".format(item))
            self._modbus_dpts[item] = self._modbusDatapoints[item.conf['wp_modbus_dpt']]

            return self.update_item
        return None

    def parse_logic(self, logic):
        if 'xxx' in logic.conf:
            # self.function(logic['name'])
            pass

    def update_item(self, item, caller=None, source=None, dest=None):
        if caller != 'plugin':
            logger.info("update item: {0}".format(item.id()))

    def _update_values(self):
        logger.debug("DIMPLEXWP: update")

        for item in self._modbus_dpts.keys():
            item_val = self._modbus_dpts[item]
            if item_val['type'] == 'register':
                #read register
                val = self._conn.read_holding_registers(item_val['address'], item_val['count'])
                if item_val['count'] == 1:
                    if item_val['conVal'] == 1:
                        val = val[0]
                    else:
                        val = utils.get_2comp(val[0])/item_val['conVal']
                elif  item_val['address'] == 5096 or item_val['address'] == 5099 : #Start Berechnung Wärmemenge Heizen
                    val = utils.get_2comp(val[0]) + utils.get_2comp(val[1])*10000 + utils.get_2comp(val[2])*100000000
            elif item_val['type'] == 'coil':
                #read coil
                val = self._conn.read_coils(item_val['address'], item_val['count'])[0]

            item(val, 'DIMPLEXWP')




if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    myplugin = Plugin('DIMPLEXWP')
    myplugin.run()
