# -------------------------------------------------------------------------
# Name:        Sealed_water module
# Purpose:     runoff calculation for open water and sealed areas

# Author:      PB
#
# Created:     12/12/2016
# Copyright:   (c) PB 2016
# -------------------------------------------------------------------------

from management_modules.data_handling import *


class sealed_water(object):
    """
    Sealed and open water runoff

    calculated runoff from impermeable surface (sealed) and into water bodies
    """

    def __init__(self, sealed_water_variable):
        self.var = sealed_water_variable

# --------------------------------------------------------------------------
# --------------------------------------------------------------------------

 

    def dynamic(self,coverType, No):
        """
        Dynamic part of the sealed_water module
        runoff calculation for open water and sealed areas

        :param coverType: Land cover type: forest, grassland  ...
        :param No: number of land cover type: forest = 0, grassland = 1 ...

        """

        if coverType == "water":
            self.var.openWaterEvap[No] = np.minimum(self.var.EWRef, self.var.availWaterInfiltration[No])
            self.var.directRunoff[No] = self.var.availWaterInfiltration[No] - self.var.openWaterEvap[No]

            # open water evaporation is directly substracted from the river, lakes, reservoir
            #self.var.directRunoff[No] = self.var.availWaterInfiltration[No].copy()
            #self.var.openWaterEvap[No] = globals.inZero.copy()

        if coverType == "sealed":
            self.var.directRunoff[No] = self.var.availWaterInfiltration[No].copy()

        self.var.waterdemand_module.dynamic_waterdemand(coverType, No)


        if option['calcWaterBalance'] and (No>3):
            self.var.waterbalance_module.waterBalanceCheck(
                [self.var.availWaterInfiltration[No] ],  # In
                [self.var.directRunoff[No],  \
                 self.var.actTransTotal[No], self.var.actBareSoilEvap[No], self.var.openWaterEvap[No]],  # Out
                [globals.inZero],  # prev storage
                [globals.inZero],
                "NoSoil", False)

