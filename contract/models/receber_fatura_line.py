from typing import DefaultDict
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class ReceberFaturaLine(models.Model):
    _name = "receber.fatura.line"
    _description = "Receber Fatura Line"
    
    receber_fatura = fields.Many2one("receber.fatura", invisible=True)
    
    products_list = fields.Many2one("contract.line")
    demanda = fields.Float(related="products_list.quantity", string="Demanda")
    recebido = fields.Integer(string="Recebido")