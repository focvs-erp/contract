import collections
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

    @api.constrains('contratos')
    def _check_exist_product_in_line(self):
        contratos = self.contratos.search([('contrato_id', '=', self.id)])
        data = [item.cd_fornecedores.id for item in contratos]

        duplicates = [item for item, count in collections.Counter(
            data).items() if count > 1]

        for n in duplicates:
            cts = contratos.filtered(
                lambda item: item.cd_fornecedores.id == n)

            if len(cts) > 0:
                raise ValidationError('Somente um fornecedor')

        if sum([item.cd_participacao for item in contratos]) > 100:
            raise ValidationError(
                'A soma das participações "%" das empresas devem ser menor que 100')