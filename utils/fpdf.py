import fpdf
from PIL import Image


class PDF(fpdf):
  def __init__(self):
    super().__init__()
    self.add_page()
    self.set_font('Helvetica', '', 10)
    self.set_margins(20, 20, 20)
    self.set_xy(20,20)

  # Retorna o limite vertical para quebra de página
  def get_max_y(self):
    return self.h - 2 * self.t_margin

  # Retorna o limite horizontal para ultrapassar margem direita
  def get_max_x(self):
    return self.w - 2 * self.l_margin

  # Renderiza uma imagem no PDF e coloca o cursor abaixo dela
  def renderImage(self, filename, prop_w=None, align=None, y_adic_new_page=None):
    """ image(filename, dim, dim_vl): Define uma imagem no PDF e coloca o cursor abaixo dela.
        O tamanho da imagem deve ser definido em relação à largura da página. O parâmetro
        'prop_w' é um valor entre 0 e 100 que corresponde ao percentual da largura da página
        que a imagem deve ocupar. Sua altura é automaticamente definida com base na proporção
        entre altura e largura da própria imagem

    Args:
      - filename (obrigatório): Nome do arquivo da imagem
      - prop_w (opcional): valor entre 0 e 100 que corresponde ao percentual da largura da
                         página que a imagem deve ocupar. Sua altura é automaticamente
                         definida com base na proporção entre altura e largura da própria
                         imagem. Se não for informado, usa 100% da largura da página
      - align (opcional): alinhamento da imagem que pode ser 'C', 'L' ou 'R'. Se não for
                          informado alinha ao centro
      - y_adic_new_page (opcional): incremento para a posição vertical, caso a imagem
                                    ultrapasse a margem inferior da página e seja
                                    renderizada na próxima página
    """

    y = self.get_y()

    # Para obter as dimensõres reais da imagem em pixels
    img = Image.open(filename)

    # Capturando as dimensões da imagem
    W_img, H_img = img.size

    # Razão entre largura e altura
    W_H = W_img/H_img

    # Largura da página descontando as margens
    W_pg = self.w - self.l_margin - self.r_margin

    # Altura da página descontando as margens
    # H_pg = self.get_max_y() - self.t_margin

    # Dimensões da imagem em milímetros
    if prop_w is None:
      prop_w = 100
    W_img = W_pg * prop_w / 100
    H_img = W_img / W_H

    # Se a base da imagem ultrapassar a margem inferior, quebra a página
    # Posição y da base da imagem na página
    Y = y + H_img
    # Coordenada y que é o limite para ultrapassar a margem inferior
    Y_lim = self.h - self.b_margin
    if Y > Y_lim:
      self.add_page()
      y = self.t_margin if y_adic_new_page is None else y_adic_new_page + self.t_margin


    # Posicionando o cursor de acordo com o parâmetro 'align'
    match align:
      case 'L':
        x_img = self.l_margin
      case 'R':
        x_img = self.w - self.r_margin - W_img
      case 'C':
        x_img = self.l_margin + (self.w - self.l_margin - self.r_margin - W_img) / 2
      case _:
        x_img = self.l_margin + (self.w - self.l_margin - self.r_margin - W_img) / 2
        self.set_x(x_img)

    # Renderizando a imagem de acordo com a largura
    self.image(filename, w=W_img, y=y, x=x_img)

    # Posicionando o cursor abaixo da imagem
    self.set_y(y + H_img)


  # Renderiza uma tabela a partir de uma DataFrame Pandas
  def renderTableFromPandas(self, df, options):
    """ renderTableFromPandas(df, options): Renderiza uma tabela a partir de uma DataFrame Pandas.

    Args:
      df: DataFrame Pandas com os dados da tabela
      options: Dicionário com os parâmetros da tabela

        As seguintes chaves devem ser informadas no dicionário options:

        'h' (obrigatório): altura mínima de cada linha
        'cols' (obrigatório): lista com os nomes das colunas utilizadas de 'df'
        'tbl_w_per' (optional): largura da tabela em percentual da largura da página
        'labels' (optinal): lista com os rótulos da tabela. Se não for informado usa 'cols'
        'cols_w' (optional): lista com as larguras das colunas em % da largura da tabela. Usa 100% se não for informado
        'align' (opcional): alinhamento da tabela. Pode ser 'L', 'C' ou 'R'. Se for omitido, alinha ao centro

    """

    warning = 'Os parâmetros obrigatórios não foram definidos no dicionário "options":'
    warning += ' cols (lista com rótulos das colunas), tbl_w_perc (largura da tabela'
    warning += ' em % da página)'

    try:

      # Definindo a altura mínima das linhas da tabela
      h = options.get('h', None)
      if h is None:
        raise KeyError('A altura mínima das linhas da tabela é obrigatória')

      # Definindo lista com as colunas que serão usadas do DataFrame 'df'
      cols = options.get('cols', None)
      if cols is None:
        raise KeyError('A lista com as colunas usadas do DataFrame é obrigatória')

      # Definindo lista com os rótulos da tabela. Se for nula, usa a lista 'cols'
      labels = options.get('labels', cols)

      # Definindo a largura da tabela
      w_tab = options.get('tbl_w_per', None)

      # Se a largura percentual da tabela for nula, usa 100% da largura da página
      # subtraída das margens laterais
      if w_tab is None:
        w_tab = self.w - self.l_margin - self.r_margin
      else:
        w_tab = (w_tab / 100) * (self.w - self.l_margin - self.r_margin)

      # Definindo a lista com %largura das colunas. Se não for definida,
      # distribui por igual
      cols_w = options.get('cols_w', None)
      if cols_w is None:
        w = w_tab / len(cols)
        cols_w = []
        for item in cols:
          cols_w.append(w)
      elif sum(cols_w) != 100:
        raise ValueError('O somatório das larguras das colunas não é igual a 100%')
      else:
        for i in range(len(cols_w)):
          cols_w[i] = (cols_w[i] / 100) * w_tab
    except Exception:
      warning = 'Um ou mais parâmetros obrigatórios não foram definidos no dicio'
      warning += 'nário "options"'
      raise KeyError(warning)

    # Extraindo os valores do dataframe para uma lista. Cada elemento é uma
    # lista com os valores de cada linha
    df = df.loc[:, cols]
    lista = df.values.tolist()

    # Definindo o alinhamento da tabela
    x = self.get_x()
    y = self.get_y()

    # Renderizando o cabeçalho da tabela
    opts = {}
    opts['cols_w'] = cols_w
    opts['h'] = h
    self.set_xy(x, y) #self.l_margin, self.t_margin)
    result = self.renderRowTable(labels, opts, cabec=True)

    # Haverá quebra de página, o cabeçalho não foi renderizado. Adicionando
    # nova página e renderizando o cabeçalho
    if result is False:
      self.add_page()
      self.set_xy(x, y) # self.l_margin, self.t_margin)
      self.renderRowTable(labels, opts, cabec=True)

    # Renderizando as linhas da tabela
    for row in lista:
      self.set_x(x) # self.l_margin)
      result = self.renderRowTable(row, opts)
      if result is False:
        self.add_page()
        self.set_xy(x, y) # self.l_margin, self.t_margin)
        self.renderRowTable(labels, opts, cabec=True)
        self.set_x(x) # self.l_margin)
        self.renderRowTable(row, opts)


  def renderRowTable(self, row, options_dicion, cabec=False):
    """ renderRowTable(row, options_dicion, cabec): Renderiza uma linha da tabela.

        Args:
          row: lista com os valores da linha
          options_dicion: dicionário com os parâmetros da linha, os quais são:
            'cols_w' (obrigatório): lista com as larguras das colunas em % da largura da tabela. Usa 100% se não for informado
            'h' (obrigatório): altura mínima da linha
          cabec (optional): se True, a fonte deve estar em negrito e a cor de fundo cinza
                            pois é a linha é cabeçalho da tabela. Padrão é False
    """
    warning = 'Os parâmetros obrigatórios não foram definidos em options_dicion:'
    warning += ' cols_w (lista com larguras das colunas) e h (altura mínima da '
    warning += 'linha)'
    try:
      cols_w = options_dicion['cols_w']
      h = options_dicion['h']
    except Exception:
      raise KeyError(warning)

    # O parâmetro cabec é True. A fonte deve estar em negrito e a cor de fundo
    # cinza pois é a linha é cabeçalho da tabela
    if cabec:
      self.set_font(self.font_family, 'B', 10)
      self.set_fill_color(217, 217, 217)
      fill = True
    else:
      self.set_font(self.font_family, '', 10)
      fill = False

    x = self.get_x()
    x_0 = x
    h_efet = 0
    x = self.get_x()
    x_0 = x
    y_0 = self.get_y()

    # Define a opacidade do texto para 0% (transparente)
    with self.local_context(fill_opacity=0):
      # Determinando a altura da linha
      for i in range(len(row)):
        self.multi_cell(cols_w[i], h, str(row[i]), border=0)
        y = self.get_y()
        h_now = y - y_0
        if h_now > h_efet:
          h_efet = h_now
        x += cols_w[i]
        self.set_xy(x, y_0)

      # Determinando se haverá quebra de página. Se houver retorna False
      y_max = self.get_max_y()
      if (y_0 + h_efet) > y_max:
        return False

    self.set_x(x_0)
    x = x_0

    # Define a opacidade do texto para 100%
    with self.local_context(fill_opacity=1):
      # Imprimindo apenas o conteúdo sem as bordas
      for i in range(len(row)):
        self.multi_cell(cols_w[i], h, str(row[i]), border=0, fill=fill)
        x += cols_w[i]
        self.set_xy(x, y_0)

      self.set_x(x_0)
      x = x_0

      # Imprimindo apenas o as bordas
      for i in range(len(row)):
        self.multi_cell(cols_w[i], h_efet, '', border=1)
        x += cols_w[i]
        self.set_xy(x, y_0)

      # Posicionando o cursor uma linha abaixo
      self.set_y(y_0 + h_efet)