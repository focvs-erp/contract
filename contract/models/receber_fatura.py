from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class ReceberFatura(models.Model):
    _name = "contract.receber_fatura"
    _description = "Receber Fatura"
    
    contract_id = fields.Many2one("contract.contract", invisible=True)
    
    partner_id = fields.Many2one("res.partner", string="Receber De")
    scheduled_date = fields.Date(string="Data Agendada", default=datetime.today())
    origin = fields.Char(related="contract_id.name", string="Documento de Origem")

    receber_fatura_line = fields.One2many("contract.receber_fatura_line","receber_fatura",string="Receber Fatura")
    state = fields.Selection([('rascunho', 'Rascunho'), ('confirmado', 'Confirmado')], default ="rascunho")
    
    def btn_validar_concluido(self):
        raise UserError("btn")
