from odoo import fields, api, models
from odoo.exceptions import ValidationError


class ContratoConsorcioLinha(models.Model):
    _name = 'contract.contrato_consorcio_linha'
    _description = 'Contrato Consórcio Linha'

    name = fields.Char(
            string="Código", 
            default="COD", 
            copy=False, 
            index=True, 
            readonly=True)
    cd_fornecedores = fields.Many2one('res.partner', string="Fornecedores")
    cd_contato = fields.Many2one('res.partner', string="Contato") 
    cd_email = fields.Char(related='cd_contato.email', string="Email") 
    cd_telefone = fields.Char(related='cd_contato.phone', string="Telefone")
    cd_participacao = fields.Float(string="Participação %")
    cd_ativo = fields.Boolean(default=False, string="Ativo")

    contrato_id = fields.Many2one('contract.contrato_consorcio', string="Contrato")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code(
            'contract.contrato_consorcio_linha')

        return super().create(vals)

    @api.constrains('cd_participacao')
    def verificar_porcentagem(self):
        if self.cd_participacao < 0 or self.cd_participacao > 100:
            raise ValidationError("Campo participação deve ser maior que 0 e menor que 100!")
  
    @api.onchange('cd_fornecedores')
    def _onchange_cd_fornecedore(self):
        for record in self:
            if record.cd_fornecedores.id:
                return {'domain': {'cd_contato': [('parent_id', '=', record.cd_fornecedores.id)]}}
            else:
                return {'domain': {'cd_contato': []}}
