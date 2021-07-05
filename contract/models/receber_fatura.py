from odoo import _, api, fields, models
from odoo.exceptions import ValidationError, UserError
from datetime import datetime

class ReceberFatura(models.TransientModel):
    _name = "contract.receber_fatura"
    _description = "Receber Fatura"

    name = fields.Char(readonly=True)
    contract_id = fields.Many2one("contract.contract", invisible=True)

    # AX4B - CPTM - RATEIO FORNECEDOR 
    ativar_consorcio_fatura = fields.Boolean( string="Ativar consorcio")
    porcentagem = fields.Float(string="Porcentagem")
     # AX4B - CPTM - RATEIO FORNECEDOR 

    partner_id = fields.Many2one("res.partner", string="Receber De")
    scheduled_date = fields.Date(string="Data Agendada", default=datetime.today())
    origin = fields.Char(related="contract_id.name", string="Documento de Origem")

    receber_fatura_line = fields.One2many("contract.receber_fatura_line","receber_fatura",string="Receber Fatura")

    def btn_validar_concluido(self):
        raise UserError (self.ativar_consorcio_fatura)
        for products_line in self.receber_fatura_line:
            for concluido in products_line:
                if concluido.demanda < concluido.concluido:
                    raise UserError('O valor do campo Concluído não pode ser maior do que o campo Demanda')
                self._cr.execute(''' update contract_line set cd_recebido=%(concluido)s where id=%(contract_line_id)s ;''',
                                {
                                    'contract_line_id': concluido.products_list.id,
                                    'concluido': concluido.concluido

                                })

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}


    @api.model
    def create(self, vals):
        obj = super(ReceberFatura, self).create(vals)
        sequence = self.env['ir.sequence'].get('receber_fatura_sequence')
        obj.write({'name': sequence})
