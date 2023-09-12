# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models,  api

class DetailFML(models.Model):
    _inherit = 'ams_fml.log'
    _description = 'Flight Maintenance Log'


    # Fixed Wing
    engine1_fw_torque   = fields.Float('Torque/Thrust/EPR')
    engine1_rpm         = fields.Float('RPM (NL/N1/NG)', track_visibility="onchange")
    engine1_rpm_nh 		= fields.Float('RPM (NH/N2)', track_visibility="onchange")
    engine1_np 			= fields.Float('NP', track_visibility="onchange")
    engine1_itt         = fields.Float('ITT/TGT/T5/EGT', track_visibility="onchange")
    engine1_fuelflow    = fields.Float('Fuel Flow', track_visibility="onchange")
    engine1_fueltemp    = fields.Selection([('green','Green'), ('yellow','Yellow'), ('red','Red')], 'Fuel Temperature', default="green", track_visibility="onchange")
    engine1_oiltemp     = fields.Float('Oil Temperature', track_visibility="onchange")
    engine1_oilpess     = fields.Float('Oil Pressure', track_visibility="onchange")
    engine1_oillvl      = fields.Float('Oil Level', track_visibility="onchange")
    engine1_vibra       = fields.Float('Vibration', track_visibility="onchange")
    engine1_c1          = fields.Float('C1/GW', track_visibility="onchange")
    engine1_itt_fw         = fields.Float('T5/TOT/ITT', track_visibility="onchange")
    engine1_oil_press_fw   = fields.Float('Oil Press')
    engine1_oil_temp_fw    = fields.Float('Oil Temp')

    # Rotary Wing
    engine1_itt_rw         = fields.Float('T4/TOT/ITT', track_visibility="onchange")
    engine1_start_itt      = fields.Float('T4/TOT/ITT')
    engine1_start_rpm      = fields.Float('N1/Ng')
    engine1_takeof_itt     = fields.Float('T4/TOT/ITT')
    engine1_takeof_rpm     = fields.Float('N1/Ng')
    engine1_xmsn_oil       = fields.Float('Xmsn Oil P/T')
    engine1_torque_percent = fields.Float('Torque (%)')
    engine1_ntl            = fields.Float('N2/Ntl')
    engine1_nr             = fields.Float('Nr')
    engine1_oil_press_rw   = fields.Float('Oil Press')
    engine1_oil_temp_rw    = fields.Float('Oil Temp')
    engine1_oat            = fields.Float('OAT')
    engine1_airspeed       = fields.Float('Airspeed')
    engine1_altitude       = fields.Float('Altitude')

    # Fixed Wing
    engine2_fw_torque   = fields.Float('Torque/Thrust/EPR')
    engine2_rpm         = fields.Float('RPM (NL/N1/NG)', track_visibility="onchange")
    engine2_rpm_nh      = fields.Float('RPM (NH/N2)', track_visibility="onchange")
    engine2_np          = fields.Float('NP', track_visibility="onchange")
    engine2_itt         = fields.Float('ITT/TGT/T5/EGT', track_visibility="onchange")
    engine2_fuelflow    = fields.Float('Fuel Flow', track_visibility="onchange")
    engine2_fueltemp    = fields.Selection([('green','Green'), ('yellow','Yellow'), ('red','Red')], 'Fuel Temperature', default="green", track_visibility="onchange")
    engine2_oiltemp     = fields.Float('Oil Temperature', track_visibility="onchange")
    engine2_oilpess     = fields.Float('Oil Pressure', track_visibility="onchange")
    engine2_oillvl      = fields.Float('Oil Level', track_visibility="onchange")
    engine2_vibra       = fields.Float('Vibration', track_visibility="onchange")
    engine2_c1          = fields.Float('C1/GW', track_visibility="onchange")
    engine2_itt_fw         = fields.Float('T5/TOT/ITT', track_visibility="onchange")
    engine2_oil_press_fw   = fields.Float('Oil Press')
    engine2_oil_temp_fw    = fields.Float('Oil Temp')

    # Rotary Wing
    engine2_itt_rw         = fields.Float('T4/TOT/ITT', track_visibility="onchange")
    engine2_start_itt      = fields.Float('T4/TOT/ITT')
    engine2_start_rpm      = fields.Float('N1/Ng')
    engine2_takeof_itt     = fields.Float('T4/TOT/ITT')
    engine2_takeof_rpm     = fields.Float('N1/Ng')
    engine2_xmsn_oil       = fields.Float('Xmsn Oil P/T')
    engine2_torque_percent = fields.Float('Torque (%)')
    engine2_ntl            = fields.Float('N2/Ntl')
    engine2_nr             = fields.Float('Nr')
    engine2_oil_press_rw   = fields.Float('Oil Press')
    engine2_oil_temp_rw    = fields.Float('Oil Temp')
    engine2_oat            = fields.Float('OAT')
    engine2_airspeed       = fields.Float('Airspeed')
    engine2_altitude       = fields.Float('Altitude')

    # Fixed Wing
    engine3_fw_torque   = fields.Float('Torque/Thrust/EPR')
    engine3_rpm         = fields.Float('RPM (NL/N1/NG)', track_visibility="onchange")
    engine3_rpm_nh      = fields.Float('RPM (NH/N2)', track_visibility="onchange")
    engine3_np          = fields.Float('NP', track_visibility="onchange")
    engine3_itt         = fields.Float('ITT/TGT/T5/EGT', track_visibility="onchange")
    engine3_fuelflow    = fields.Float('Fuel Flow', track_visibility="onchange")
    engine3_fueltemp    = fields.Selection([('green','Green'), ('yellow','Yellow'), ('red','Red')], 'Fuel Temperature', default="green", track_visibility="onchange")
    engine3_oiltemp     = fields.Float('Oil Temperature', track_visibility="onchange")
    engine3_oilpess     = fields.Float('Oil Pressure', track_visibility="onchange")
    engine3_oillvl      = fields.Float('Oil Level', track_visibility="onchange")
    engine3_vibra       = fields.Float('Vibration', track_visibility="onchange")
    engine3_c1          = fields.Float('C1/GW', track_visibility="onchange")
    engine3_itt_fw         = fields.Float('T5/TOT/ITT', track_visibility="onchange")
    engine3_oil_press_fw   = fields.Float('Oil Press')
    engine3_oil_temp_fw    = fields.Float('Oil Temp')


    # Rotary Wing
    engine3_itt_rw         = fields.Float('T4/TOT/ITT', track_visibility="onchange")
    engine3_start_itt      = fields.Float('T4/TOT/ITT')
    engine3_start_rpm      = fields.Float('N1/Ng')
    engine3_takeof_itt     = fields.Float('T4/TOT/ITT')
    engine3_takeof_rpm     = fields.Float('N1/Ng')
    engine3_xmsn_oil       = fields.Float('Xmsn Oil P/T')
    engine3_torque_percent = fields.Float('Torque (%)')
    engine3_ntl            = fields.Float('N2/Ntl')
    engine3_nr             = fields.Float('Nr')
    engine3_oil_press_rw   = fields.Float('Oil Press')
    engine3_oil_temp_rw    = fields.Float('Oil Temp')
    engine3_oat            = fields.Float('OAT')
    engine3_airspeed       = fields.Float('Airspeed')
    engine3_altitude       = fields.Float('Altitude')

    # Fixed Wing
    engine4_fw_torque   = fields.Float('Torque/Thrust/EPR')
    engine4_rpm         = fields.Float('RPM (NL/N1/NG)', track_visibility="onchange")
    engine4_rpm_nh      = fields.Float('RPM (NH/N2)', track_visibility="onchange")
    engine4_np          = fields.Float('NP', track_visibility="onchange")
    engine4_itt         = fields.Float('ITT/TGT/T5/EGT', track_visibility="onchange")
    engine4_fuelflow    = fields.Float('Fuel Flow', track_visibility="onchange")
    engine4_fueltemp    = fields.Selection([('green','Green'), ('yellow','Yellow'), ('red','Red')], 'Fuel Temperature', default="green", track_visibility="onchange")
    engine4_oiltemp     = fields.Float('Oil Temperature', track_visibility="onchange")
    engine4_oilpess     = fields.Float('Oil Pressure', track_visibility="onchange")
    engine4_oillvl      = fields.Float('Oil Level', track_visibility="onchange")
    engine4_vibra       = fields.Float('Vibration', track_visibility="onchange")
    engine4_c1          = fields.Float('C1/GW', track_visibility="onchange")
    engine4_itt_fw         = fields.Float('T5/TOT/ITT', track_visibility="onchange")
    engine4_oil_press_fw   = fields.Float('Oil Press')
    engine4_oil_temp_fw    = fields.Float('Oil Temp')

    # Rotary Wing
    engine4_itt_rw         = fields.Float('T4/TOT/ITT', track_visibility="onchange")
    engine4_start_itt      = fields.Float('T4/TOT/ITT')
    engine4_start_rpm      = fields.Float('N1/Ng')
    engine4_takeof_itt     = fields.Float('T4/TOT/ITT')
    engine4_takeof_rpm     = fields.Float('N1/Ng')
    engine4_xmsn_oil       = fields.Float('Xmsn Oil P/T')
    engine4_torque_percent = fields.Float('Torque (%)')
    engine4_ntl            = fields.Float('N2/Ntl')
    engine4_nr             = fields.Float('Nr')
    engine4_oil_press_rw   = fields.Float('Oil Press')
    engine4_oil_temp_rw    = fields.Float('Oil Temp')
    engine4_oat            = fields.Float('OAT')
    engine4_airspeed       = fields.Float('Airspeed')
    engine4_altitude       = fields.Float('Altitude')

    fuel_uplift			= fields.Float('Uplift (Liter / Galon)', track_visibility="onchange")
    fuel_total			= fields.Float('Total (Liter / Kg)', track_visibility="onchange")
    fuel_cons			= fields.Float('Cons (Liter / Kg)', track_visibility="onchange")
    fuel_rem			= fields.Float('Rem (Liter / Kg)', track_visibility="onchange")

    oil_uplift         = fields.Float('Uplift (Liter / Tin)', track_visibility="onchange")
    oil_total          = fields.Float('Total (Liter / Tin)', track_visibility="onchange")
    oil_cons           = fields.Float('Cons (Liter / Tin)', track_visibility="onchange")
    oil_rem            = fields.Float('Rem (Liter / Tin)', track_visibility="onchange")

    oil1_add			= fields.Float('Engine 1', track_visibility="onchange")
    oil2_add			= fields.Float('Engine 2', track_visibility="onchange")
    oil3_add			= fields.Float('Engine 3', track_visibility="onchange")
    oil4_add			= fields.Float('Engine 4', track_visibility="onchange")


    """ASURRANCE CHECK"""

    engine1_torque            = fields.Float('Torque', track_visibility="onchange")
    engine2_torque            = fields.Float('Torque', track_visibility="onchange")
    engine3_torque            = fields.Float('Torque', track_visibility="onchange")
    engine4_torque            = fields.Float('Torque', track_visibility="onchange")


    engine1_pan            = fields.Float('PA/N1', track_visibility="onchange")
    engine2_pan            = fields.Float('PA/N1', track_visibility="onchange")
    engine3_pan            = fields.Float('PA/N1', track_visibility="onchange")
    engine4_pan            = fields.Float('PA/N1', track_visibility="onchange")

    engine1_oat            = fields.Float('OAT', track_visibility="onchange")
    engine2_oat            = fields.Float('OAT', track_visibility="onchange")
    engine3_oat            = fields.Float('OAT', track_visibility="onchange")
    engine4_oat            = fields.Float('OAT', track_visibility="onchange")

    engine1_act            = fields.Float('ACT/ITT', track_visibility="onchange")
    engine2_act            = fields.Float('ACT/ITT', track_visibility="onchange")
    engine3_act            = fields.Float('ACT/ITT', track_visibility="onchange")
    engine4_act            = fields.Float('ACT/ITT', track_visibility="onchange")

    engine1_calb            = fields.Float('CALB.', track_visibility="onchange")
    engine2_calb            = fields.Float('CALB.', track_visibility="onchange")
    engine3_calb            = fields.Float('CALB.', track_visibility="onchange")
    engine4_calb            = fields.Float('CALB.', track_visibility="onchange")

    engine1_margin            = fields.Float('Margin', track_visibility="onchange")
    engine2_margin            = fields.Float('Margin', track_visibility="onchange")
    engine3_margin            = fields.Float('Margin', track_visibility="onchange")
    engine4_margin            = fields.Float('Margin', track_visibility="onchange")

    engine1_hp      = fields.Float('HP', track_visibility="onchange")
    engine2_hp      = fields.Float('HP', track_visibility="onchange")
    engine3_hp      = fields.Float('HP', track_visibility="onchange")
    engine4_hp      = fields.Float('HP', track_visibility="onchange")

    engine1_pwr_mrg = fields.Float('Pwr Mrg', track_visibility="onchange")
    engine2_pwr_mrg = fields.Float('Pwr Mrg', track_visibility="onchange")
    engine3_pwr_mrg = fields.Float('Pwr Mrg', track_visibility="onchange")
    engine4_pwr_mrg = fields.Float('Pwr Mrg', track_visibility="onchange")

