import math

import pandas as pd
import pdfplumber as p


class Laudo():
    """
    classe Laudo(): Instancia um laudo genérico. Deve ser instanciada apenas
    para extração de dados com o método 'loadRawData()' e determinar o tipo
    de exame do laudo ('m': massa, 'v': volume: 'c': comprimento/largura/
    altura ou'u': unidade). Demais ações devem ser realizadas com suas
    classes filha: LaudoMassa, LaudoVolume, LaudoComp ou LaudoUnid.

    """

    def __init__(self):
        self.num_laudo = None
        self.tipo_exame = None
        self.nome_prod = None
        self.marca_prod = None
        self.qn_prod = None
        self.unid_prod = None
        self.unid_exame = None
        self.data_exame = None
        self.tc = None  # Termo de coleta
        self.n = None  # Tamanho da amostra
        self.c = None  # Critério de aceitação individual
        self.T = None  # Tolerância individual (erro tipo T1)
        self.T3 = None  # Erro tipo T3
        self.total_defeituosos = None  # Total de unidades com erro tipo T1
        self.total_T3 = None  # Total de unidades com erro tipo T3
        self.valor_min_indiv = None  # Qn - T
        self.valor_erro_T3 = None  # Qn - 3.T
        self.media_min = None
        self.perc_defeituosos = None
        self.list_raw_data = []
        # String para extrair informações do produto (nome, marca, Qn)
        self._string1 = None
        # String para extrair n, c e T
        self._string2 = None
        # String para extrair n.º defeituosas encontradas e média mínima
        self._string3 = None
        # Lista com linhas das string de medições
        self.lista_medicoes = []
        # DataFrame Pandas com as medições de 'lista_medicoes'
        self.df_medicoes = None

    # Carrega para a propriedade list_raw_data o conteúdo bruto do PDF do laudo
    def loadRawData(self, url_laudo):
        # Resetando dados de laudo anterior
        self.__init__()

        # Carregando todo o conteúdo do laudo
        pdf = p.open(url_laudo)

        # Extraindo as páginas para um iterável
        pgs = pdf.pages

        # Lista para receber todas as linhas das tabelas do PDF
        tbls = []

        # Varrendo todas as páginas para extrair as tabelas
        for pg in pgs:
            tbls += pg.extract_tables()

        # Varrendo as tabelas para extrair suas linhas para list_raw_data
        for tb in tbls:
            for row in tb:
                self.list_raw_data.append(row)

    # Retorna o tipo de exame e o atribui à 'tipo_exame'
    def getTipoExame(self):
        if self.tipo_exame is None:
            self._getString1()
            STRING = self._string1

            try:
                string = self._getValueBetweenStrings(
                   STRING,
                   'Conteúdo Nominal: ',
                   ' Massa Específica'
                )
                lst = string.split(' ')
                cod = lst[1][-1].lower()

                match cod:
                    case 'g':
                        self.tipo_exame = 'm'
                    case 'l':
                        self.tipo_exame = 'v'
                    case 'm':
                        self.tipo_exame = 'c'

            except Exception:
                self.tipo_exame = 'u'

            return self.tipo_exame

    def getTC(self):
        # data = self.list_raw_data

        string = self._getDataByString('Termo de Coleta')
        if len(string) > 0:
            lst_tmp = string.split('Matr. Metrol.:')
            tmp = lst_tmp[0]
            tmp = tmp.split(':')
            tmp = tmp[1].strip()

        self.tc = tmp

    # Método protegido que dada uma string chave 'str_key' varre list_raw_data
    # em busca da string que a contém
    def _getDataByString(self, str_key):
        for item in self.list_raw_data:
            for row in item:
                if row is not None and str_key in row:
                    return row
        return None

    # Método protegido utilizado para obter os dados do laudo (produto, marca, qn,  # noqa:E501
    # n, c, T, etc.). Extrai uma substring de uma string maior. Deve-se fornecer  # noqa:E501
    # um trecho antes e depois da substring (str_start e str_end) para extraí-la  # noqa:E501
    def _getValueBetweenStrings(self, string, str_start, str_end):
        i_0 = string.index(str_start) + len(str_start)
        i_1 = string.index(str_end)
        return string[i_0: i_1]

    # Carrega para a propriedade 'string1' a string da qual serão extraídos
    # dados do produto (nome, marca, Qn)
    def _getString1(self):
        if self._string1 is None:
            data = self._getDataByString('Produto: ')
            self._string1 = data

    # Carrega para a propriedade 'string2' a string da qual serão extraídos
    # n, c, e T
    def _getString2(self):
        if self._string2 is None:
            data = self._getDataByString('Faixa do Lote:')
            self._string2 = data

    # Carrega para a propriedade 'string3' a string da qual serão extraídos
    # n.º defeituosas encontradas e média mínima
    def _getString3(self):
        if self._string3 is None:
            data = self._getDataByString('Defeituosas Encontradas: ')
            self._string3 = data

    # Carrega para a propriedade 'lista_medicoes' uma lista com as medições do
    # exame como string. Deve ser sobrescrita por cada classe filha para as
    # devidas adapatações
    def _getListaMedicoes(self):
        data = self.list_raw_data
        linhas_com_medicoes = False

        for row in data:
            if row[0] is not None and 'Valor da menor unidade:' in row[0]:
                linhas_com_medicoes = False
            if row[0] is not None and 'Observação' in row[0]:
                linhas_com_medicoes = False
            if row[0] is not None and 'Observações' in row[0]:
                linhas_com_medicoes = False
            if row[0] is not None and 'Produto: ' in row[0]:
                linhas_com_medicoes = False
            if linhas_com_medicoes and len(row[0]) > 2:
                self.lista_medicoes.append(row[0])
            if row[0] is not None and 'Unidade nº ' in row[0]:
                linhas_com_medicoes = True

        return self.lista_medicoes

    # Transforma o conteúdo de lista_medicoes em dataframe Pandas
    def getMedicoesDataFrame(self):
        """
        Transforma o conteúdo de 'lista_medicoes' em um dataframe Pandas
        (df_medicoes). Retorna o dataframe
        """

        # Carregando 'lista_medicoes'
        if self.lista_medicoes == []:
            data = self._getListaMedicoes()
        else:
            data = self.lista_medicoes

        # Transformando 'lista_medicoes' em dataframe Pandas
        self.df_medicoes = pd.DataFrame(
           data,
           columns=['Cont_liq', 'Defeituosos']
        )
        return self.df_medicoes

    # Carrega dados do produto (nome_prod, marca_prod, qn_prod)
    def loadProdData(self):
        self._getString1()
        string = self._string1

        # nome_prod
        try:
            self.nome_prod = self._getValueBetweenStrings(
               string.upper(),
               'PRODUTO: ',
               ' CÓDIGO: '
            )
        except Exception:
            self.nome_prod = None

        # marca_prod
        try:
            self.marca_prod = self._getValueBetweenStrings(
               string.upper(),
               'MARCA: ',
               ' FATOR DE CORREÇÃO:'
            )
        except Exception:
            self.marca_prod = None

        # qn_prod, unid_prod
        try:
            str_qn = self._getValueBetweenStrings(
               string.upper(),
               'CONTEÚDO NOMINAL: ',
               ' MASSA ESPECÍFICA'
            ).lower()
            lst_qn = str_qn.split(' ')
            self.qn_prod = lst_qn[0]
            self.unid_prod = lst_qn[1]
        except Exception:
            self.qn_prod = None
            self.unid_prod = None

        # unid_exame
        try:
            self._getString3()
            string = self._string3
            str_un_ex = self._getValueBetweenStrings(
               string.upper(),
               'VALOR MÍN. INDIVIDUAL: ',
               '\nRESULTADO'
            )
            lst_un_ex = str_un_ex.split(' ')
            self.unid_exame = lst_un_ex[1].lower()
        except Exception:
            self.unid_exame = None

        # data_exame e num_laudo
        rows = self.list_raw_data
        for row in rows:
            # 'Data e Hora do Exame: 08/01/2025 11h00min'
            if row[1] is not None and 'Data e Hora do Exame:' in row[1]:
                lst_date = row[1].split(' ')
            self.data_exame = lst_date[5]
            if row[2] is not None and 'Data e Hora do Exame:' in row[2]:
                lst_date = row[2].split(' ')
                self.data_exame = lst_date[5]
            for item in row:
                if item is not None and 'NÚMERO DO LAUDO:' in item.upper():
                    lst_num = item.split(' ')
                    self.num_laudo = lst_num[3]

        # c
        try:
            self._getString2()
            string = self._string2

            str1 = 'DEFEITUOSAS ACEITÁVEIS (C): '
            str2 = '\nTOLERÂNCIA'
            self.c = self._getValueBetweenStrings(
               string.upper(),
               str1,
               str2
            ).lower()
        except Exception:
            self.c = None

        # n
        try:
            str1 = 'AMOSTRA: '
            str2 = ' UNIDADE(S)'
            self.n = int(self._getValueBetweenStrings(
               string.upper(),
               str1,
               str2)
            )
        except Exception:
            self.n = None

        # total_defeituosos
        try:
            self._getString3()
            string = self._string3
            str1 = 'DEFEITUOSAS ENCONTRADAS: '
            str2 = '\nVALOR'
            self.total_defeituosos = int(self._getValueBetweenStrings(
               string.upper(),
               str1,
               str2)
            )
        except Exception:
            self.total_defeituosos = None

        # valor_min_indiv (Qn - T)
        try:
            self._getString3()
            string = self._string3
            str1 = 'VALOR MÍN. INDIVIDUAL: '
            str2 = ' G'
            strV = self._getValueBetweenStrings(string.upper(), str1, str2)
            strV = strV.replace(',', '.')
            self.valor_min_indiv = float(strV)
        except Exception:
            self.valor_min_indiv = None

        # T
        try:
            self._getString2()
            string = self._string2
            str1 = 'TOLERÂNCIA INDIVIDUAL: '
            str2 = ' G'
            strT = self._getValueBetweenStrings(string.upper(), str1, str2)
            strT = strT.replace(',', '.')
            self.T = float(strT)
        except Exception:
            self.T = None

        # perc_defeituosos
        df = self.total_defeituosos
        n = self.n
        self.perc_defeituosos = int(math.ceil((df * 100)/n))

    # Calcula 'total_T3' e 'valor_erro_T3'. Só deve ser chamado pelo método
    # 'loadProdData' nas classes filhas
    def _getValoresT3(self):
        # valor_erro_T3
        self.valor_erro_T3 = float(self.valor_min_indiv - 2 * self.T)

        # total_T3
        df = self.getMedicoesDataFrame()
        df_def = df.query('Cont_liq < @self.valor_erro_T3')
        self.total_T3 = len(df_def)

    def getErrosTxt(self):
        """
        getErrosTxt(): Retorna uma string com os erros encontrados no laudo.
        Só deve ser chamada após o método 'loadProdData' ser chamado. Retorna
        '' (string vazia) se não houver erros. Se houver erros, retorna uma
        string com os erros encontrados.
        """

        # Percentual de erro T1
        perc_T1 = self.perc_defeituosos

        # Total de erros T3
        total_T3 = self.total_T3

        # Início do texto a ser definido se houver erros
        txt_erros_start = f'o produto {self.nome_prod.upper()}, marca {self.marca_prod.upper()}, examinad'  # noqa:E501
        txt_erros_start += f'o em nosso laboratório em {self.data_exame} é passível de a'  # noqa:E501
        txt_erros_start += f'preensão pois referente ao conteúdo nominal {self.qn_prod} '  # noqa:E501
        txt_erros_start += f'{self.unid_exame} determinado no laudo n.º {self.num_laudo} '  # noqa:E501

        # String com o texto completo, se houver erros
        txt_erros = ''

        # Montando o texto se houver os dois erros
        if perc_T1 > 30 and total_T3 > 0:
            txt_erros += txt_erros_start
            txt_erros += "apresenta pelo menos uma unidade amostral com déficit de conteúdo "  # noqa:E501
            txt_erros += "efetivo três vezes maior que o estabelecido pelo RTM em vigor e apr"  # noqa:E501
            txt_erros += f"esenta {perc_T1}% de unidades amostrais com erro individual (o li"  # noqa:E501
            txt_erros += "mite para apreensão é 30%)"
        # Montando o texto só com o erro T3
        elif not perc_T1 > 30 and total_T3:
            txt_erros += txt_erros_start
            txt_erros += "apresenta pelo menos uma unidade amostral com déficit de conteúdo "  # noqa:E501
            txt_erros += "efetivo três vezes maior que o estabelecido pelo RTM em vigor."  # noqa:E501
        # Montando o texto só com o erro T1
        elif perc_T1 > 30 and not total_T3:
            txt_erros += txt_erros_start
            txt_erros += f"apresenta {perc_T1}% de unidades amostrais com erro individual (o"  # noqa:E501
            txt_erros += " limite para apreensão é 30%)"

        return txt_erros


class LaudoMassa(Laudo):
    def __init__(self):
        super().__init__()

    # Sobrescreve 'loadProdData' apenas para calcular 'valor_erro_T3'
    def loadProdData(self):

        # Chamando o método da classe pai. Em seguida é carregado o que
        # o método da classe pai não é capaz de carregar
        super().loadProdData()

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getValoresT3()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    # das strings
    def _getListaMedicoes(self):
        # Carregando 'lista_medicoes' com o método da classe pai
        super()._getListaMedicoes()

        # Atribuindo lista_medicoes 'bruta' à lista 'rows'
        rows = self.lista_medicoes
        lst_tmp = []

        # Varrendo rows
        for row in rows:

            # Atribuindo row a lst sem o índice (unidade amostral)
            lst = row.split(' ')[1:]

            # Subsituindo as vírgulas das strings por ponto
            lst = [x.replace(',', '.') for x in lst]

            # Transformando todas as strings em float
            lst = [float(x) for x in lst]

            # Se o último item de lst for negativo (nº defeituosos), atribui
            # a lst_tmp o último e penúltimo itens de lst
            size = len(lst)
            if lst[size-1] < 0:
                lst_tmp.append([lst[size-2], lst[size-1]])

            # O último item é positivo (peso líquido). Acrescenta o último
            # item e o valor zero (nenhum defeituoso)
            else:
                lst_tmp.append([lst[size-1], 0])

            self.lista_medicoes = lst_tmp
            return self.lista_medicoes


class LaudoVolume(Laudo):
    def __init__(self):
        super().__init__()

    # Sobrescreve o método 'loadProdData' p/ carregar 'T' e 'valor_min_indiv'
    # que não são carregados na classe pai
    def loadProdData(self):
        # Chamando o método da classe pai. Em seguida é carregado o que o
        # método da classe pai não é capaz de carregar
        super().loadProdData()

        # T
        self._getString2()
        string = self._string2
        str1 = 'TOLERÂNCIA INDIVIDUAL: '
        str2 = ' M'
        strT = self._getValueBetweenStrings(string.upper(), str1, str2)
        strT = strT.replace(',', '.')
        self.T = float(strT)

        # valor_min_indiv (Qn - T)
        self._getString3()
        string = self._string3
        str1 = 'VALOR MÍN. INDIVIDUAL: '
        str2 = ' ML'
        strV = self._getValueBetweenStrings(string.upper(), str1, str2)
        strV = strV.replace(',', '.')
        self.valor_min_indiv = float(strV)

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getValoresT3()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    #  das strings
    def _getListaMedicoes(self):
        # Carregando 'lista_medicoes' com o método da classe pai
        super()._getListaMedicoes()

        # Atribuindo lista_medicoes 'bruta' à lista 'rows'
        rows = self.lista_medicoes
        lst_tmp = []

        # Varrendo rows
        for row in rows:

            # Atribuindo row a lst sem o índice (unidade amostral)
            lst = row.split(' ')[1:]

            # Subsituindo as vírgulas das strings por ponto
            lst = [x.replace(',', '.') for x in lst]

            # Transformando todas as strings em float
            lst = [float(x) for x in lst]

            # Se o último item de lst for negativo (nº defeituosos), atribui
            #  a lst_tmp o último e penúltimo itens de lst
            size = len(lst)
            if lst[size-1] < 0:
                lst_tmp.append([lst[size-2], lst[size-1]])

            # O último item é positivo (conteúdo líquido). Acrescenta o último
            # item e o valor zero (nenhum defeituoso)
            else:
                lst_tmp.append([lst[size-1], 0])

        self.lista_medicoes = lst_tmp
        return self.lista_medicoes


class LaudoComp(Laudo):
    def __init__(self):
        super().__init__()

    # Sobrescreve o método 'loadProdData' p/ carregar 'unid_exame', 'T' e
    # 'valor_min_indiv' que não são carregados na classe pai
    def loadProdData(self):

        # Chamando o método da classe pai. Em seguida é carregado o que o
        # método da classe pai não é capaz de carregar
        super().loadProdData()

        # unid_exame
        self._getString3()
        string = self._string3
        str_un_ex = self._getValueBetweenStrings(
            string.upper(),
            'VALOR MÍN. ACEITÁVEL: ',
            '\nRESULTADO'
        )
        lst_un_ex = str_un_ex.split(' ')
        self.unid_exame = lst_un_ex[1].lower()

        # T
        self._getString2()
        string = self._string2
        str1 = 'TOLERÂNCIA INDIVIDUAL: '
        str2 = ' CM'
        try:
            strT = self._getValueBetweenStrings(string.upper(), str1, str2)
        except Exception:
            strT = self._getValueBetweenStrings(string.upper(), str1, ' MM')
        strT = strT.replace(',', '.')
        self.T = float(strT)

        # valor_min_indiv (Qn - T)
        self._getString3()
        string = self._string3
        str1 = 'VALOR MÍN. ACEITÁVEL: '
        str2 = ' CM'
        try:
            strV = self._getValueBetweenStrings(string.upper(), str1, str2)
        except Exception:
            strV = self._getValueBetweenStrings(string.upper(), str1, ' MM')
        strV = strV.replace(',', '.')
        self.valor_min_indiv = float(strV)

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getValoresT3()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    # das strings
    def _getListaMedicoes(self):
        # Carregando 'lista_medicoes' com o método da classe pai
        super()._getListaMedicoes()

        # Atribuindo lista_medicoes 'bruta' à lista 'rows'
        rows = self.lista_medicoes
        lst_tmp = []

        # Varrendo rows
        for row in rows:

            # Atribuindo row a lst sem o índice (unidade amostral)
            lst = row.split(' ')[1:]

            # Subsituindo as vírgulas das strings por ponto
            lst = [x.replace(',', '.') for x in lst]

            # Transformando todas as strings em float
            lst = [float(x) for x in lst]

            # Se o último item de lst for negativo (nº defeituosos), atribui
            # a lst_tmp o último e penúltimo itens de lst
            size = len(lst)
            if lst[size-1] < 0:
                lst_tmp.append([lst[size-2], lst[size-1]])

            # O último item é positivo (medição). Acrescenta o último item e
            # o valor zero (nenhum defeituoso)
            else:
                lst_tmp.append([lst[size-1], 0])

        self.lista_medicoes = lst_tmp
        return self.lista_medicoes


class LaudoUnid(Laudo):
    def __init__(self):
        super().__init__()

    # Sobrescreve o método 'loadProdData' p/ carregar 'marca_prod', 'qn_prod',
    # 'unid_prod', 'T' e 'valor_min_indiv' que não são carregados na classe pai
    def loadProdData(self):
        self._getString1()
        string = self._string1

        # Chamando o método da classe pai. Em seguida é carregado o que o
        # método da classe pai não é capaz de carregar
        super().loadProdData()

        # marca_prod
        self.marca_prod = self._getValueBetweenStrings(
            string.upper(),
            'MARCA: ',
            '\nCONTEÚDO NOMINAL'
        )

        # qn_prod
        str_qn = self._getValueBetweenStrings(
            string.upper(),
            'CONTEÚDO NOMINAL (QN):',
            '\nTEMPERATURA'
        ).lower()
        lst_qn = str_qn.split(' ')
        self.qn_prod = lst_qn[0]

        # unid_prod
        self.unid_prod = 'un.'

        # T
        self._getString2()
        string = self._string2
        str1 = 'TOLERÂNCIA INDIVIDUAL: '
        str2 = ' UN.'
        strT = self._getValueBetweenStrings(string.upper(), str1, str2)
        self.T = int(strT)

        # valor_min_indiv (Qn - T)
        self._getString3()
        string = self._string3
        str1 = 'VALOR MÍN. INDIVIDUAL: '
        str2 = ' UN.'
        self.valor_min_indiv = int(self._getValueBetweenStrings(
            string.upper(),
            str1,
            str2)
        )

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getValoresT3()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    # das strings
    def _getListaMedicoes(self):
        data = self.list_raw_data
        linhas_com_medicoes = False

        for row in data:
            if row[0] is not None and 'Valor da menor unidade:' in row[0]:
                linhas_com_medicoes = False
            if row[0] is not None and 'Observação' in row[0]:
                linhas_com_medicoes = False
            if row[0] is not None and 'Observações' in row[0]:
                linhas_com_medicoes = False
            if row[0] is not None and 'Produto: ' in row[0]:
                linhas_com_medicoes = False
            if linhas_com_medicoes:  # and row[1] is not None and len(row[1]) > 0:  # noqa:E501
                # Retirando todos os elementos nulos das linhas
                while None in row:
                    row.remove(None)
                # Retirando todos os elementos de strings vazias das linhas
                while '' in row:
                    row.remove('')
                # Transformando todos os elementos de row em inteiros
                row = [int(x) for x in row]

            # row tem 3 itens (índice, cont. efet. e cont. efet.)
            if len(row) == 3:
                self.lista_medicoes.append(row[2:] + [0])
            # row tem 4 itens  (índice, cont. efet., cont. efet., n.º defeit.)
            elif len(row) == 4:
                self.lista_medicoes.append(row[2:])
            if row[0] is not None and 'UNIDADE AMOSTRAL' in str(row[0]).upper():  # noqa:E501
                linhas_com_medicoes = True

        return self.lista_medicoes
