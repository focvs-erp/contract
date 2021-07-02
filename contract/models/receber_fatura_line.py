from typing import DefaultDict
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from datetime import datetime

class ReceberFaturaLine(models.TransientModel):
    _name = "contract.receber_fatura_line"
    _description = "Receber Fatura Line"

    receber_fatura = fields.Many2one("contract.receber_fatura", invisible=True)

    products_list = fields.Many2one("contract.line")
    demanda = fields.Float(related="products_list.quantity", string="Demanda")
    concluido = fields.Float(string="Concluído")
    unidade = fields.Many2one(related="products_list.uom_id")
