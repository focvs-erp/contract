# # -*- coding: utf-8 -*-

# from odoo import models, fields, api
# from odoo.exceptions import UserError, ValidationError


# class ReajustePrecoItem(models.Model):
#     _name = 'contract.reajuste_preco_item'
#     _description = 'Item do Reajuste do Preço'

#     name = fields.Char()
#     descricao =fields.Char()
#     reajuste_preco = fields.Many2one("contract.reajuste_preco", invisible=True, string="Reajuste de Preço")


#     aplicado_em = fields.Selection([
#         ('1', 'Todos os Produtos'),
#         ('2', 'Produto')],
#         default='1', required=True
#         )

#     compute_price = fields.Selection([
#         ('fixed', 'Preço Fixo'),
#         ('percentage', 'Porcentagem'),
#         ('indice', 'Indice')],
#         index=True,
#         default='fixed',
#         required=True)

#     fixed_price = fields.Float(string="Preço fixo")
#     percent_price = fields.Float('Porcentagem')

#     currency_id = fields.Many2one('res.currency', 'Currency',readonly=True, store=True)
#     company_id = fields.Many2one('res.company', string='Empresa')
#     indice = fields.Many2one('res.currency', string='Baseado em')
#     product_id = fields.Many2one('product.product', 'Produto', ondelete='cascade', check_company=True)



#     data_inicio = fields.Date(string='Data Inicio',required="1")
#     data_final = fields.Date(string='Data Final',required="1")

#     @api.onchange('compute_price')
#     def _total(self):
#         if(self.compute_price == 'fixed'):
#             self.percent_price =0
#             self.indice = ""
#         else:
#             if(self.compute_price == 'percentage'):
#                 self.indice = ""
#                 self.fixed_price =0
#             else:
#                 self.percent_price =0
#                 self.fixed_price =0


#     def validar_produto_informado(self):
#         # Validar se o campo produto foi preenchido
#         if self.aplicado_em == '2' and not self.product_id:
#             raise UserError('Produto deve ser informado')

#     def validar_campos_obrigatorios(self):
#         self.validar_produto_informado()

# #     @api.model
# #     def create(self, vals):
# #         obj = super(ReajustePrecoItem, self).create(vals)
# #         obj.write({'descricao': self.name_produto})

# # #         if (aplicado_em==2):
# # #             obj.write({'name': self.name_produto})
# # #         else:
# # #             obj.write({'name': 'Todos os Produtos'})

# #         return obj

# #     def write(self, vals):

# #         if (self.aplicado_em==2):
# #             self.name  =  self.name_produto
# #         else:
# #             self.name  ="name': 'Todos os Produtos"

# #         res = super(ReajustePrecoItem, self).write(vals)
# #         return res
