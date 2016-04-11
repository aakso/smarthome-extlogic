import logging
import datetime

logger = logging.getLogger('')

from plugins.extlogic import ExtLogicBase

class AutumnLogic(ExtLogicBase):

    def fetch_current_values(self):
        self.cur_out_temp = self.sh.outside.outdoortemperature()
        self.cur_boiler_temp = self.sh.eahp.boiler_temp_ow()

    def scenario1(self):
        ref = 'Scenario 1'
        triggered = (
            (
                (self.cur_out_temp <= 20 and self.cur_out_temp > 1) or
                (self.cur_out_temp <= -30)
            )
            and self.cur_boiler_temp > 45
        )
        if triggered: self.set(self.pump_power, False, ref=ref)

    def scenario2(self):
        ref = 'Scenario 2'
        triggered = (
            (
                (self.cur_out_temp <= 20 and self.cur_out_temp > 1) or
                (self.cur_out_temp <= -30)
            )
            and self.cur_boiler_temp <= 45
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 20.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 1, ref=ref)

    def scenario3(self):
        ref = 'Scenario 3'
        triggered = (
            (self.cur_out_temp <= 1 and self.cur_out_temp > 0)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 21.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 1, ref=ref)

    def scenario4(self):
        ref = 'Scenario 4'
        triggered = (
            (self.cur_out_temp <= 0 and self.cur_out_temp > -2)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 21.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 2, ref=ref)

    def scenario5(self):
        ref = 'Scenario 5'
        triggered = (
            (self.cur_out_temp <= -2 and self.cur_out_temp > -5)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 21.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 3, ref=ref)

    def scenario6(self):
        ref = 'Scenario 6'
        triggered = (
            (self.cur_out_temp <= -5 and self.cur_out_temp > -10)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 22.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 2, ref=ref)

    def scenario7(self):
        ref = 'Scenario 7'
        triggered = (
            (self.cur_out_temp <= -10 and self.cur_out_temp > -15)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 22.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 3, ref=ref)

    def scenario8(self):
        ref = 'Scenario 8'
        triggered = (
            (self.cur_out_temp <= -15 and self.cur_out_temp > -30)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 23.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 3, ref=ref)

    def reduce(self):
        ref = 'Reduce-'
        triggered1 = (
            self.sh.eahp.boiler_temp_ow.db('min', '30i') >= 51 and
            self.get(self.pump_power) == True
        )
        triggered2 = (
            self.sh.first.livingroom.fireplacetemp.db('min','1h') >= 35 and
            self.get(self.pump_power) == True
        )
        triggered3 = (
            self.sh.eahp.air_out_cooledtemp.db('max','4h','4h') >= 10 and
            self.get(self.pump_power) == True
        )
        triggered4 = (
            self.sh.eahp.air_out_cooledtemp.db('max','4h') >= 10 and
            self.get(self.pump_power) == True
        )

        if triggered1:
            self.relative_set(self.set_temp, -1, ref=ref)
        if triggered2:
            self.relative_set(self.set_temp, -1, ref=ref)
        if triggered3:
            self.relative_set(self.set_temp, -1, ref=ref)
        if triggered4:
            self.relative_set(self.set_temp, -1, ref=ref)

    def increase(self):
        ref = 'Increase+'
        triggered1 = (
            self.sh.eahp.boiler_temp_ow.db('min', '30i') < 51 and
            self.get(self.pump_power) == True
        )
        triggered2 = (
            self.sh.eahp.air_out_cooledtemp.db('max','8h') < 10 and
            self.get(self.pump_power) == True
        )
        if triggered1:
            self.relative_set(self.set_temp, +1, ref=ref)
        if triggered2:
            self.relative_set(self.set_temp, +1, ref=ref)

    def night(self):
        ref = 'Night {}'
        dt = datetime.datetime.now()
        triggered1 = (
            dt.hour > 1 and dt.hour <= 6 and
            self.get(self.pump_power) == True
        )
        if triggered1:
            self.relative_set(self.set_temp, -2, ref=ref.format(dt.hour))

    def logic(self):
        self.pump_power = self.sh.second.ilp.pump_power
        self.set_temp = self.sh.second.ilp.set_temp
        self.mode = self.sh.second.ilp.mode
        self.quiet = self.sh.second.ilp.quiet
        self.fan_speed = self.sh.second.ilp.fan_speed

        self.fetch_current_values()

        self.scenario1()
        self.scenario2()
        self.scenario3()
        self.scenario4()
        self.scenario5()
        self.scenario6()
        self.scenario7()
        self.scenario8()

        self.reduce()
        self.increase()
        self.night()

class WinterLogic(ExtLogicBase):

    def fetch_current_values(self):
        self.cur_out_temp = self.sh.outside.outdoortemperature()
        self.cur_boiler_temp = self.sh.eahp.boiler_temp_ow()

    def scenario1(self):
        ref = 'Scenario 1'
        triggered = (
            (
                (self.cur_out_temp <= 20 and self.cur_out_temp > -3) or
                (self.cur_out_temp <= -30)
            )
            and self.cur_boiler_temp > 45
        )
        if triggered: self.set(self.pump_power, False, ref=ref)

    def scenario2(self):
        ref = 'Scenario 2'
        triggered = (
            (
                (self.cur_out_temp <= 20 and self.cur_out_temp > -3) or
                (self.cur_out_temp <= -30)
            )
            and self.cur_boiler_temp <= 40
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 23.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 3, ref=ref)

    def scenario3(self):
        ref = 'Scenario 3'
        triggered = (
            (self.cur_out_temp <= -3 and self.cur_out_temp > -8)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 17.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 1, ref=ref)

    def scenario4(self):
        ref = 'Scenario 4'
        triggered = (
            (self.cur_out_temp <= -8 and self.cur_out_temp > -15)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 18.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 1, ref=ref)

    def scenario5(self):
        ref = 'Scenario 5'
        triggered = (
            (self.cur_out_temp <= -15 and self.cur_out_temp > -30)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 19.0, ref=ref)
            self.set(self.mode, 1, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 1, ref=ref)

    def reduce(self):
        ref = 'Reduce-'
        triggered1 = (
            self.sh.eahp.boiler_temp_ow.db('min', '30i') >= 51 and 
            self.get(self.pump_power) == True
        )
        triggered2 = (
            self.sh.first.livingroom.fireplacetemp.db('min','1h') >= 35 and
            self.get(self.pump_power) == True
        )
        triggered3 = (
            self.sh.eahp.air_out_cooledtemp.db('max','4h','4h') >= 10 and
            self.get(self.pump_power) == True
        )
        triggered4 = (
            self.sh.eahp.air_out_cooledtemp.db('max','4h') >= 10 and
            self.get(self.pump_power) == True
        )

        if triggered1:
            if self.get(self.set_temp) > 16:
                self.relative_set(self.set_temp, -1, ref=ref)
        if triggered2: 
            if self.get(self.set_temp) > 16:
                self.relative_set(self.set_temp, -1, ref=ref)
        if triggered3:
            if self.get(self.set_temp) > 16:
                self.relative_set(self.set_temp, -1, ref=ref)
        if triggered4:
            if self.get(self.set_temp) > 16:
                self.relative_set(self.set_temp, -1, ref=ref)

    def increase(self):
        ref = 'Increase+'
        triggered1 = (
            self.sh.eahp.boiler_temp_ow.db('min', '30i') < 51 and 
            self.sh.eahp.boiler_temp_ow.db('max', '30i') >= 55 and 
            self.get(self.pump_power) == True and self.get(self.set_temp) < 23
        )
        triggered2 = (
            self.sh.eahp.air_out_cooledtemp.db('max','8h') < 10 and
            self.get(self.pump_power) == True and self.get(self.set_temp) < 23
        )
        if triggered1:
            if self.get(self.set_temp) < 25:
                self.relative_set(self.set_temp, +1, ref=ref)
        if triggered2:
            if self.get(self.set_temp) < 25:
                self.relative_set(self.set_temp, +1, ref=ref)

    def night(self):
        ref = 'Night {}'
        dt = datetime.datetime.now()
        triggered1 = (
            (dt.hour >= 20 or (dt.hour >= 0 and dt.hour <= 6)) and
            self.get(self.pump_power) == True
        )
        if triggered1:
            self.set(self.pump_power, False, ref=ref.format(dt.hour))

    def logic(self):
        self.pump_power = self.sh.second.ilp.pump_power
        self.set_temp = self.sh.second.ilp.set_temp
        self.mode = self.sh.second.ilp.mode
        self.quiet = self.sh.second.ilp.quiet
        self.fan_speed = self.sh.second.ilp.fan_speed

        self.fetch_current_values()

        self.scenario1()
        self.scenario2()
        self.scenario3()
        self.scenario4()
        self.scenario5()

        self.reduce()
        self.increase()
        self.night()

class SummerLogic(ExtLogicBase):

    def fetch_current_values(self):
        self.cur_out_temp = self.sh.outside.outdoortemperature()
        self.cur_boiler_temp = self.sh.eahp.boiler_temp_ow()
        self.cur_tundratemp = self.sh.first.hallway.tundratemp()

    def scenario1(self):
        ref = 'Scenario 1'
        triggered = (
                (self.cur_tundratemp < 22.5 and self.cur_out_temp < 11)
        )
        if triggered: 
            self.set(self.pump_power, False, ref=ref)

    def scenario2(self):
        ref = 'Scenario 2'
        triggered = (
                 (self.cur_tundratemp >= 22.5 and self.cur_tundratemp < 23 and self.cur_out_temp >= 11)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 21.0, ref=ref)
            self.set(self.mode, 3, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 1, ref=ref)

    def scenario3(self):
        ref = 'Scenario 3'
        triggered = (
                (self.cur_tundratemp >= 23 and self.cur_out_temp >= 11)
        )
        if triggered:
            self.set(self.pump_power, True, ref=ref)
            self.set(self.set_temp, 21.0, ref=ref)
            self.set(self.mode, 3, ref=ref)
            self.set(self.quiet, False, ref=ref)
            self.set(self.fan_speed, 3, ref=ref)

    def logic(self):
        try:
            self.pump_power = self.sh.second.ilp.pump_power
            self.set_temp = self.sh.second.ilp.set_temp
            self.mode = self.sh.second.ilp.mode
            self.quiet = self.sh.second.ilp.quiet
            self.fan_speed = self.sh.second.ilp.fan_speed
            self.fetch_current_values()
        except AttributeError:
            return

        self.scenario1()
        self.scenario2()
        self.scenario3()
