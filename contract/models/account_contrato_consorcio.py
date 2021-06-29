from odoo import fields, api, models
from odoo.exceptions import ValidationError


class ContratoConsorcio(models.Model):
    _name = 'contract.contrato_consorcio'
    _description = 'Contrato Consórcio'

    name = fields.Char(
        string="Código", 
        default="COD", 
        copy=False, 
        index=True, 
        readonly=True)
    cd_descricao = fields.Text(string="Descrição")
    cd_ativo = fields.Boolean(default=False, string="Ativo")

    contratos = fields.One2many('contract.contrato_consorcio_linha', 'contrato_id', string='Contratos')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'contract.contrato_consorcio')

        return super().create(vals)
