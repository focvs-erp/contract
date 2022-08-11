import collections
from odoo import fields, api, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class ContratoConsorcio(models.Model):
    _name = 'contract.contrato_consorcio'
    _description = 'Contrato Consórcio'

    name = fields.Char(
        string="Code", #Código
        default="COD", 
        copy=False, 
        index=True, 
        readonly=True)
    cd_descricao = fields.Text(string="Description") #Descrição
    cd_ativo = fields.Boolean(default=False, string="Active") #Ativo

    contratos = fields.One2many('contract.contrato_consorcio_linha', 'contrato_id', string='Contracts') #Contratos

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
                raise ValidationError(_('It is not possible to repeat a supplier in the same consortium contract')) #Não é possível repetir um fornecedor no mesmo contrato de consórcio

        if sum([item.cd_participacao for item in contratos]) > 100:
            raise ValidationError(_(
                'The sum of the "%" shares of the companies must be less than 100')) #A soma das participações "%" das empresas devem ser menor que 100
