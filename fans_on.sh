#!/bin/bash

[ -f fans_sensors_definitions.sh ] && . fans_sensors_definitions.sh

echo 1 > $fan_setmanual_PCI
echo 1200 > $fan_setrpm_PCI

echo 1 > $fan_setmanual_PS
echo 1000 > $fan_setrpm_PS

echo 1 > $fan_setmanual_EXHAUST
echo 1500 > $fan_setrpm_EXHAUST

echo 1 > $fan_setmanual_INTAKE
echo 1500 > $fan_setrpm_INTAKE

echo 1 > $fan_setmanual_BOOSTA
echo 2500 > $fan_setrpm_BOOSTA

echo 1 > $fan_setmanual_BOOSTB
echo 2500 > $fan_setrpm_BOOSTB

