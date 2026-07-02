import datetime as dt
import json
import os

from django.conf import settings
from PIL import Image

from .fpdf import PDF

JSON_PATH = settings.JSON_IPEM_DATA_PATH
COAT_ARMS_IMAGE_PATH = settings.COAT_ARMS_IMAGE_PATH
AGREEMENT_IMAGE_PATH = settings.AGREEMNET_IMAGE_PATH
IN_CHARGE_SIGNATURE = settings.IN_CHARGE_IMAGE_PATH

uf_choices = {
    'AC': 'Acre',
    'AL': 'Alagoas',
    'AP': 'Amapá',
    'AM': 'Amazonas',
    'BA': 'Bahia',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'ES': 'Espirito Santo',
    'GO': 'Goiás',
    'MA': 'Maranhão',
    'MS': 'Mato Grosso do Sul',
    'MT': 'Mato Grosso',
    'MG': 'Minas Gerais',
    'PA': 'Pará',
    'PB': 'Paraíba',
    'PR': 'Paraná',
    'PE': 'Pernambuco',
    'PI': 'Piauí',
    'RJ': 'Rio de Janeiro',
    'RN': 'Rio Grande do Norte',
    'RS': 'Rio Grande do Sul',
    'RO': 'Rondônia',
    'RR': 'Roraima',
    'SC': 'Santa Catarina',
    'SP': 'São Paulo',
    'SE': 'Sergipe',
    'TO': 'Tocantins'
}

class Dispatch(PDF):
  """
  Class to generate the dispatch PDF.

  Required argument
  - list_erros: list with error texts to be displayed
  Optional arguments: 'args' dictionary
  - args['data_despacho']: if not informed, uses the current date
  - args['width_perc_assin']: percentage width of the signature image in relation to the page 
  width. If not informed, uses 90%
  - args['nome_responsavel']: name of the person responsible for the dispatch. If not informed,
    uses ''
  - args['cargo_responsavel']: position of the person responsible for the dispatch. If not 
  informed, uses ''  """
  def __init__(self, list_erros, **args):
    # Header height
    self.cabec_h = None

    # Page margins
    self.l_margin = 20
    self.r_margin = 20
    self.t_margin = 10
    self.b_margin = 10
    self.t_margin_cabec = 10 # t_margin is set to 10 in the parent class's __init__(). This
                             # attribute is set because the first time header()
                             # is called in super().__init__(), t_margin is 10, even though
                          # it is set differently above
    # Data do despacho
    self.dispatch_date = args.get(
      'dispatch_date',
      dt.date.today().strftime('%d/%m/%Y')
    )

    # Percentual da imagem da assinatura na página. Se não for informado usa 80%
    self.perc_w_signature = args.get('width_perc_assin', 80)

    # Nome do responsável pelo despacho
    self.responsable_name = args.get('responsable_name', '')

    # Cargo do responsável pelo despacho
    self.responsable_position = args.get('responsable_position', '')

    # Tentando carregar url da imagem do brasão do Estado
    self.url_coat_of_arms = None
    if os.path.exists(settings.MEDIA_ROOT / 'brasao.png'):
      self.url_coat_of_arms = f'{settings.MEDIA_ROOT}/brasao.png'

    # Carregando arquivo json com dados do cabeçalho do despacho...
    # Existe arquivo
    try:
      with open(JSON_PATH, 'r') as f:
        ipem_data = json.load(f)
      self.txt_state = uf_choices[ipem_data.get('uf_ipem', '')].upper()
      self.txt_secretary = ipem_data.get('sec_ipem', '').upper()
      self.txt_ipem = ipem_data.get('rs_ipem', '').upper()
    # Não existe arquivo
    except Exception:
      self.txt_state = 'FALTA DEFINIR O NOME DO ESTADO'
      self.txt_secretary = 'FALTA DEFINIR O NOME DA SECRETARIA'
      self.txt_ipem = 'FALTA DEFINIR O NOME DO IPEM'

    # Tentando carregar a imagem de marca d'água do despacho
    if os.path.exists(AGREEMENT_IMAGE_PATH):
      self.watermark = str(AGREEMENT_IMAGE_PATH)

    else:
      self.watermark = None

    # O método 'header()' é chamado no __init__() da classe pai. Por isso os
    # itens acima foram definidos antes da chamada de super().__init__(), pois
    # precisam estar definidos antes da chamada de 'header()'
    super().__init__()

    # Tentando carregar a url da imagem de assinatura (se houver)
    if os.path.exists(IN_CHARGE_SIGNATURE):
      self.url_signature = IN_CHARGE_SIGNATURE
    else:
      self.url_signature = None

    # Lista com erros
    self.list_erros = list_erros

    # Norma
    self.norma = 'NIT-SIMEP-015'

    # Parte inicial do texto despacho
    self.txt_start = f'De acordo com a {self.norma} '

    # Parte final do texto do despacho (após os textos com erros)
    self.txt_end = 'Como não dispomos nem de recursos nem de local adequado para apreensão de produtos pré-medidos'
    self.txt_end += ', recomendamos que a infração seja avaliada pela COJUR com base no Art. 9º, § 1º, incisos I'
    self.txt_end += ' a V da Lei 9933 de 20/12/1999.\n\n\nAtenciosamente\n\nA seu dispor'

    # Título 'DESPACHO'
    self.set_xy(20,70)
    self.set_font('helvetica', 'B', 14)
    self.multi_cell(0, 5, 'DESPACHO', align='C')

    # Seção 'DATA'
    self.set_xy(20,self.get_y() + 15)
    self.set_font('helvetica', 'B', 12)
    self.cell(16, 5,'DATA: ')
    self.set_font('helvetica', '', 12)
    self.cell(0, 5, self.dispatch_date)

    # Seção 'DE: Divisão de Pré-Medidos'
    self.set_y(self.get_y() + 5)
    self.set_font('helvetica', 'B', 12)
    self.cell(0, 5,'DE: ')
    self.set_font('helvetica', '', 12)
    self.set_x(30)
    self.cell(0, 5, 'Divisão de Pré-Medidos')

    # Seção 'PARA: COJUR'
    self.set_y(self.get_y() + 5)
    self.set_font('helvetica', 'B', 12)
    self.cell(0, 6,'PARA: ')
    self.set_font('helvetica', '', 12)
    self.set_x(35.5)
    self.cell(0, 6, 'COJUR')

    # Seção ASSUNTO: Valores de erro individual acima ...
    self.set_y(self.get_y() + 5)
    self.set_font('helvetica', 'B', 12)
    self.cell(0, 6,'ASSUNTO: ')
    self.set_font('helvetica', '', 12)
    self.set_x(44)
    self.cell(0, 6, f'Valores de erro individual acima do estabelecido pela {self.norma}')
    self.set_x(20)

  # Cria o cabeçalho e define marca dágua (se existir imagem no Drive)
  def header(self):
    self.set_xy(self.l_margin, self.t_margin_cabec)
    if self.url_coat_of_arms is not None:
      self.renderImage(self.url_coat_of_arms, prop_w=10)

    self.set_font('Times', 'B', 12)
    txt_cabec = f'GOVERNO DO ESTADO DE {self.txt_state}\n'
    txt_cabec += f'{self.txt_secretary}\n'
    txt_cabec += f'{self.txt_ipem}\n'
    txt_cabec += 'ÓRGÃO EXECUTOR DO INMETRO'
    self.multi_cell(0, 5, txt_cabec, align='C')

    # Definindo a altura do cabeçalho
    self.cabec_h = self.get_y()

    # Renderizando a marca d'água, se houver imagem salva
    if self.watermark is not None:
      # A marca d'água deve ocupar 2/3 da altura da página, a seção central
      # Altura da imagem de marca d'água
      marca_h = self.h / 3

      # Posição vertical onde a marca d'água deve ser renderizada
      marca_pos_y = marca_h

      # Obtendo a relação entre largura e altura da imagem de marca d'água
      marca = Image.open(self.watermark)
      w, h = marca.size
      w_h = w / h

      # Definindo a largura da imagem com base em w_h
      marca_w = marca_h * w_h

      # Posição horizontal onde a marca d'água deve ser renderizada
      if marca_w < self.w:
        marca_pos_x = (self.w - marca_w) / 2
      else:
        marca_pos_x = 0

      # Aplicando opacidade à marca d'água
      marca = marca.convert('RGBA')
      r,g,b,a = marca.split()
      a = a.point(lambda p: int(p * 0.1))
      marca = Image.merge('RGBA', (r,g,b,a))

      # Renderizando a imagem de marca d'água
      self.image(marca, w=marca_w, h=marca_h, y=marca_pos_y, x=marca_pos_x)
      marca.close()

    self.set_xy(self.l_margin, self.cabec_h + 10)

  def makeDispatchPDF(self, pathfile=None, perc_w_signature=100):
    """
    makeDispatchPDF(): Gera o PDF do despacho.
    Se houver erros passíveis de apreensão, gera o PDF com o texto final do
    despacho. Se não houver erros retorna False
    """
    # Signature image width in percentual about page
    self.perc_w_signature = perc_w_signature

    # Quantidade de erros em 'self.list_erros'
    n = len(self.list_erros)

    # Lista com erros
    erros = self.list_erros

    # Iniciando o texto final do despacho
    txt = f'{self.txt_start}'

    # Não há nenhum texto com erros. Finaliza e retorna False
    if n == 0:
      return False

    # Casos em que é gerado PDF do despacho
    # Há apenas um texto com erros
    elif n == 1:
      txt += f' {erros[0]} {self.txt_end}'
    # Há mais de um texto com erros
    else:
      txt += ':\n\n'
      for erro in erros:
        txt += f'- {erro[0].upper() + erro[1:]}\n\n'
      txt += self.txt_end
    # Inserindo o texto com os erros no despacho
    self.set_xy(20, self.get_y() + 15)
    self.multi_cell(0, 6, txt)

    # Se foi informado nome e cargo do responsável, exibe esses valores para
    # assinatura, mesmo que exista imagem de assinatura no Google Drive
    nome_cargo_definidos = (self.responsable_name != '') and (self.responsable_position != '')

    # Foram informados nome e cargo do responsável pelo despacho. Imprime esses
    # valores mesmo que haja imagem de assinatura disponível no Google Drive
    if nome_cargo_definidos:
      self.cell(0, 6, '____________________________________________________', align='C', new_y='NEXT', new_x='LEFT')
      self.multi_cell(0, 6, f'{self.responsable_name}\n{self.responsable_position}', align='C')

    # Nome e cargo do responsável pelo despacho não foram definidos, mas imagem
    # assinatura foi. Imprime a imagem da assinatura
    elif not nome_cargo_definidos and self.url_signature is not None:
      self.renderImage(
        self.url_signature,
        prop_w=self.perc_w_signature,
        y_adic_new_page=self.cabec_h,
      )

    # Não foram definidos nem nome/cargo do responsável nem imagem de assinatura
    # Imprimir 'Nome Responsável' e 'Cargo Responsável'
    elif not nome_cargo_definidos and self.url_signature is None:
      self.cell(0, 6, '____________________________________________________', align='C', new_y='NEXT', new_x='LEFT')
      self.multi_cell(0, 6, 'Nome Responsável\nCargo Responsável', align='C')


    code_file = 1 # Código do usuário (PK)
    filename = f'{code_file:05d}_dispatch.pdf'

    # Trying to erase previous file
    try:
      os.remove(settings.BASE_DIR / f'media/dispatch_pdfs/{filename}')
    except Exception:
      pass

    fullpath = filename if pathfile is None else f'{pathfile}/{filename}'
    self.output(fullpath)
    return filename