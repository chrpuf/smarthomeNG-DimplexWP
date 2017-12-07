# smarthomeNG-DimplexWP
smarthomeNG Plugin for reading information from a Dimplex heat pump via Modbus TCP

## Requirements
First you need the [NWPM extension](http://www.dimplex.de/wiki/index.php/NWPM) properly installed and configured for your Dimplex heat pump. This extension also offers [Modbus TCP](http://www.dimplex.de/wiki/index.php/NWPM_Modbus_TCP) access to your heat pump.

Moreover you have to install [pyModbusTCP](https://github.com/sourceperl/pyModbusTCP) to use this plugin.

## Configuration

### plugin.conf
```
dimplexwp:
    class_name: DimplexWP
    class_path: plugins.dimplexwp
    wp_ip: 192.168.0.4
    wp_port: 502
```

#### Attributes
* `wp_ip` : IP address of the Dimplex heat pump respectivley the NWPM extension
* `wp_port` : Port number of the NWPM extension for Modbus TCP access (default: 502)

### item.conf

To assign information from the heat pump to an item, it has to be type of `num` and must implement one attribute called `wp_modbus_dpt`, which represents the kind of information you want to get from your heat pump. 

#### wp_modbus_dpt

Below you can find a list of possible values with which you can get the corresponding information from your heat pump:

* outdoor_temp                  (outdoor temperature)
* return_temp                   (return temperature)     
* set-point_return_temp         (set-point return temperature) 
* hot_water_temp                (hot water temperature)
* flow_temp                     (flow temperature)
* heat_source_inlet_temp        (heat source inlet temperature)
* heat_source_outlet_temp       (heat source outlet temperature)
* hysteresis                    (hysteresis of the return temperature)
* heating_rod                   (returns the time in hours which the heating rod was running)
* heat_heating                  (returns the all time produced quantity of heat for heating)
* heat_hot_water                (returns the all time produced quantity of heat for hot water)
* operating_mode                (represent the operation mode of the heat pump\*)
* hot_water_hysteresis          (hysteresis of the hot water)
* hot_water_set-point_temp      (set-point temperature of the hot water)
* status_messages               (represent the status of the heat pump\*)
* heat_pump_lock                (indicates if the heat pump is locked)
* alerts                        (represent the alerts of the heat pump\*)
* sensors                       ()
* outlet_compressor             (indicates if the compressor is running)
* outlet_primary_pump           (indicates if the primary pump is running)
* outlet_heating_rod            (indicates if the heating rod is running)
* outlet_heating_pump_M13       (indicates if the heating pump M13 is running)
* outlet_hot_water_pump         (indicates if the hot water pump is running)
* outlet_add_circ_pump          (indicates if the additional circulation pump is running)
* outlet_heating_pump_M15       (indicates if the heating pump M15 is running)
* outlet_heating_pump_M14       (indicates if the heating pump M14 is running)
* outlet_heating_pump_M20       (indicates if the heating pump M20 is running)

\*More information can be found in the [documentation](http://www.dimplex.de/wiki/index.php/NWPM_Modbus_TCP#Datenpunktliste) of the NWPM extension

### Example:
```
    Waermepumpe:
        Aussentemperatur:
            type: num
            wp_modbus_dpt: outdoor_temp

        Ruecklauftemperatur:
            type: num
            wp_modbus_dpt: return_temp

        Ruecklaufsolltemperatur:
            type: num
            wp_modbus_dpt: set-point_return_temp

        Warmwassertemperatur:
            type: num
            wp_modbus_dpt: hot_water_temp

        Vorlauftemperatur:
            type: num
            wp_modbus_dpt: flow_temp
```