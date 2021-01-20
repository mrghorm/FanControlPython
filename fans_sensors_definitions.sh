#!/bin/bash

echo "Fan control program"

cpu0_core0_prefix="/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp2"
cpu0_core1_prefix="/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp3"
cpu0_core2_prefix="/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp4"
cpu0_core3_prefix="/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp10"
cpu0_core4_prefix="/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp11"
cpu0_core5_prefix="/sys/devices/platform/coretemp.0/hwmon/hwmon0/temp12"

cpu1_core0_prefix="/sys/devices/platform/coretemp.1/hwmon/hwmon0/temp2"
cpu1_core1_prefix="/sys/devices/platform/coretemp.1/hwmon/hwmon0/temp3"
cpu1_core2_prefix="/sys/devices/platform/coretemp.1/hwmon/hwmon0/temp4"
cpu1_core3_prefix="/sys/devices/platform/coretemp.1/hwmon/hwmon0/temp10"
cpu1_core4_prefix="/sys/devices/platform/coretemp.1/hwmon/hwmon0/temp11"
cpu1_core5_prefix="/sys/devices/platform/coretemp.1/hwmon/hwmon0/temp12"

smc_core_a_diode_prefix="/sys/devices/platform/applesmc.768/temp8"
smc_core_b_diode_prefix="/sys/devices/platform/applesmc.768/temp3"

northbridge_heatsink_prefix="/sys/devices/platform/applesmc.768/temp54"
northbridge_diode_prefix="/sys/devices/platform/applesmc.768/temp53"

powersupply1_alt_prefix="/sys/devices/platform/applesmc.768/temp72"
powersupply2_alt_prefix="/sys/devices/platform/applesmc.768/temp73"

pcie_ambient_prefix="/sys/devices/platform/applesmc.768/temp57"

fan_readrpm_PCI="/sys/devices/platform/applesmc.768/fan1_input"
fan_setrpm_PCI="/sys/devices/platform/applesmc.768/fan1_output"
fan_setmanual_PCI="/sys/devices/platform/applesmc.768/fan1_manual"

fan_readrpm_PS="/sys/devices/platform/applesmc.768/fan2_input"
fan_setrpm_PS="/sys/devices/platform/applesmc.768/fan2_output"
fan_setmanual_PS="/sys/devices/platform/applesmc.768/fan2_manual"

fan_readrpm_EXHAUST="/sys/devices/platform/applesmc.768/fan3_input"
fan_setrpm_EXHAUST="/sys/devices/platform/applesmc.768/fan3_output"
fan_setmanual_EXHAUST="/sys/devices/platform/applesmc.768/fan3_manual"

fan_readrpm_INTAKE="/sys/devices/platform/applesmc.768/fan4_input"
fan_setrpm_INTAKE="/sys/devices/platform/applesmc.768/fan4_output"
fan_setmanual_INTAKE="/sys/devices/platform/applesmc.768/fan4_manual"

fan_readrpm_BOOSTA="/sys/devices/platform/applesmc.768/fan5_input"
fan_setrpm_BOOSTA="/sys/devices/platform/applesmc.768/fan5_output"
fan_setmanual_BOOSTA="/sys/devices/platform/applesmc.768/fan5_manual"

fan_readrpm_BOOSTB="/sys/devices/platform/applesmc.768/fan6_input"
fan_setrpm_BOOSTB="/sys/devices/platform/applesmc.768/fan6_output"
fan_setmanual_BOOSTB="/sys/devices/platform/applesmc.768/fan6_manual"

echo $fan_readrpm_BOOSTB
