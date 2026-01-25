set_property PACKAGE_PIN AJ13 [get_ports {PPS[0]}]
set_property IOSTANDARD LVCMOS18 [get_ports {PPS[0]}]

set_property PACKAGE_PIN AR11 [get_ports led_tx_active]
set_property IOSTANDARD LVCMOS18 [get_ports led_tx_active]

set_property BITSTREAM.CONFIG.UNUSEDPIN PULLUP [current_design]
set_property BITSTREAM.CONFIG.OVERTEMPSHUTDOWN ENABLE [current_design]
set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]

set_max_delay -datapath_only -from [get_clocks -of_objects [get_pins rfsoc_radio_i/clk_wiz_0/inst/mmcme4_adv_inst/CLKOUT0]] -to [get_clocks -of_objects [get_pins rfsoc_radio_i/clk_wiz_0/inst/mmcme4_adv_inst/CLKOUT0]] 6.000
set_input_delay -clock [get_clocks -of_objects [get_pins rfsoc_radio_i/clk_wiz_0/inst/mmcme4_adv_inst/CLKOUT0]] -min -add_delay 0.200 [get_ports {PPS[0]}]
set_input_delay -clock [get_clocks -of_objects [get_pins rfsoc_radio_i/clk_wiz_0/inst/mmcme4_adv_inst/CLKOUT0]] -max -add_delay 0.300 [get_ports {PPS[0]}]
