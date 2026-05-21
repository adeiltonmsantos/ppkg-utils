import math

import pandas as pd
import pdfplumber as p


class ExamReport():
    """
    class ExamReport(): Instancia um laudo genérico. Deve ser instanciada apenas
    para extração de dados com o método 'loadRawData()' e determinar o tipo
    de exame do laudo ('m': massa, 'v': volume: 'c': comprimento/largura/
    altura ou'u': unidade). Demais ações devem ser realizadas com suas
    classes filha: LaudoMassa, LaudoVolume, LaudoComp ou LaudoUnid.

    """

    def __init__(self):
        self.exam_report_num = None
        self.exam_report_type = None
        self.product_name = None
        self.product_brand = None
        self.qn_product = None
        self.unit_product = None
        self.unit_exam = None
        self.exam_report_date = None
        self.tc = None  # Termo de coleta
        self.n = None  # Tamanho da amostra
        self.c = None  # Critério de aceitação individual
        self.T = None  # Tolerância individual (erro tipo T1)
        self.T3 = None  # Erro tipo T3
        self.total_defective = None  # Total de unidades com erro tipo T1
        self.total_T3 = None  # Total de unidades com erro tipo T3
        self.min_individual_value = None  # Qn - T
        self.T3_error_value = None  # Qn - 3.T
        self.min_average = None
        self.perc_defective = None
        self.list_raw_data = []
        # String para extrair informações do produto (nome, marca, Qn)
        self._string1 = None
        # String para extrair n, c e T
        self._string2 = None
        # String para extrair n.º defeituosas encontradas e média mínima
        self._string3 = None
        # Lista com linhas das string de medições
        self.mesurements_list = []
        # DataFrame Pandas com as medições de 'lista_medicoes'
        self.df_medicoes = None

    # Carrega para a propriedade list_raw_data o conteúdo bruto do PDF do laudo
    def loadRawData(self, url_or_object_file):
        # Resetando dados de laudo anterior
        self.__init__()

        try:
            # Carregando todo o conteúdo do laudo
            pdf = p.open(url_or_object_file)

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

            str_wanted = 'LAUDO DE EXAME QUANTITATIVO DE PRODUTOS PRÉ-MEDIDOS'
            if str_wanted in self.list_raw_data[0][0]:
                return True
            else:
                return False
        except Exception:
            return False

    # Retorna o tipo de exame e o atribui à 'tipo_exame'
    def getExamType(self):
        if self.exam_report_type is None:
            raw_data = self.list_raw_data
            try:
                for item in raw_data:
                    # Exam type is 'number of units'
                    if 'Unidade amostral' in str(item[0]):
                        return 'u'
                    elif 'Unidade nº' in str(item[0]):
                        # Removing all the blank spaces from string item
                        item = str(item).replace(' ', '').lower()
                        if 'ml' in item:
                            return 'v'
                        if '(g)' in item:
                            return 'm'
                        if '(cm)' in item:
                            return 'c'
            except Exception as e:
                print(repr(e))
                return False

    def getTC(self):
        string = self._getDataByString('Termo de Coleta')
        if len(string) > 0:
            lst_tmp = string.split('Matr. Metrol.:')
            tmp = lst_tmp[0]
            tmp = tmp.split(':')
            tmp = tmp[1].strip()

        self.tc = tmp
        return tmp

    # Método protegido que dada uma string chave 'str_key' varre 'list_raw_data'
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
                self.mesurements_list.append(row[0])
            if row[0] is not None and 'Unidade nº ' in row[0]:
                linhas_com_medicoes = True

        return self.mesurements_list

    # Transforma o conteúdo de lista_medicoes em dataframe Pandas
    def getMedicoesDataFrame(self):
        """
        Transforma o conteúdo de 'lista_medicoes' em um dataframe Pandas
        (df_medicoes). Retorna o dataframe
        """

        # Carregando 'lista_medicoes'
        if self.mesurements_list == []:
            data = self._getListaMedicoes()
        else:
            data = self.mesurements_list

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
            self.product_name = self._getValueBetweenStrings(
               string.upper(),
               'PRODUTO: ',
               ' CÓDIGO: '
            )
        except Exception:
            self.product_name = None

        # marca_prod
        try:
            self.product_brand = self._getValueBetweenStrings(
               string.upper(),
               'MARCA: ',
               ' FATOR DE CORREÇÃO:'
            )
        except Exception:
            self.product_brand = None

        # qn_prod, unid_prod
        try:
            str_qn = self._getValueBetweenStrings(
               string.upper(),
               'CONTEÚDO NOMINAL: ',
               ' MASSA ESPECÍFICA'
            ).lower()
            lst_qn = str_qn.split(' ')
            self.qn_product = lst_qn[0]
            self.unit_product = lst_qn[1]
        except Exception:
            self.qn_product = None
            self.unit_product = None

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
            self.unit_exam = lst_un_ex[1].lower()
        except Exception:
            self.unit_exam = None

        # data_exame e num_laudo
        rows = self.list_raw_data
        for row in rows:
            try:
                if row[1] is not None and 'Data e Hora do Exame:' in row[1]:
                    lst_date = row[1].split(' ')
                    self.exam_report_date = lst_date[5]
                if row[2] is not None and 'Data e Hora do Exame:' in row[2]:
                    lst_date = row[2].split(' ')
                    self.exam_report_date = lst_date[5]
            except Exception:
                self.exam_report_date = None

            try:
                for item in row:
                    if item is not None and 'NÚMERO DO LAUDO:' in item.upper():
                        lst_num = item.split(' ')
                        self.exam_report_num = lst_num[3]
            except Exception:
                self.exam_report_num = None

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
            self.total_defective = int(self._getValueBetweenStrings(
               string.upper(),
               str1,
               str2)
            )
        except Exception:
            self.total_defective = None

        # valor_min_indiv (Qn - T)
        try:
            self._getString3()
            string = self._string3
            str1 = 'VALOR MÍN. INDIVIDUAL: '
            str2 = ' G'
            strV = self._getValueBetweenStrings(string.upper(), str1, str2)
            strV = strV.replace(',', '.')
            self.min_individual_value = float(strV)
        except Exception:
            self.min_individual_value = None

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
        try:
            df = self.total_defective
            n = self.n
            self.perc_defective = int(math.ceil((df * 100)/n))
        except Exception:
            self.perc_defective = None

    # Calcula 'total_T3' e 'valor_erro_T3'. Só deve ser chamado pelo método
    # 'loadProdData' nas classes filhas
    def _getT3Values(self):
        # valor_erro_T3
        try:
            self.T3_error_value = float(self.min_individual_value - 2 * self.T)
        except Exception:
            self.T3_error_value = None

        # total_T3
        try:
            df = self.getMedicoesDataFrame()
            df_def = df.query('Cont_liq < @self.T3_error_value')
            self.total_T3 = len(df_def)
        except Exception:
            self.total_T3 = None

    def isSubjectToDispatch(self):
        try:
            self.loadProdData()
            return self.perc_defective > 30
        except Exception as e:
            print(repr(e))

    def getErrosTxt(self):
        """
        getErrosTxt(): Retorna uma string com os erros encontrados no laudo.
        Só deve ser chamada após o método 'loadProdData' ser chamado. Retorna
        '' (string vazia) se não houver erros. Se houver erros, retorna uma
        string com os erros encontrados.
        """

        # Percentual de erro T1
        perc_T1 = self.perc_defective

        # Total de erros T3
        total_T3 = self.total_T3

        # Início do texto a ser definido se houver erros
        txt_erros_start = f'o produto {self.product_name.upper()}, marca {self.product_brand.upper()}, examinad'  # noqa:E501
        txt_erros_start += f'o em nosso laboratório em {self.exam_report_date} é passível de a'  # noqa:E501
        txt_erros_start += f'preensão pois referente ao conteúdo nominal {self.qn_product} '  # noqa:E501
        txt_erros_start += f'{self.unit_exam} determinado no laudo n.º {self.exam_report_num} '  # noqa:E501

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


class ExamReportMass(ExamReport):
    def __init__(self):
        super().__init__()

    # Sobrescreve 'loadProdData' apenas para calcular 'valor_erro_T3'
    def loadProdData(self):

        # Chamando o método da classe pai. Em seguida é carregado o que
        # o método da classe pai não é capaz de carregar
        super().loadProdData()

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getT3Values()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    # das strings
    def _getListaMedicoes(self):
        # Carregando 'lista_medicoes' com o método da classe pai
        super()._getListaMedicoes()

        # Atribuindo lista_medicoes 'bruta' à lista 'rows'
        rows = self.mesurements_list
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

            self.mesurements_list = lst_tmp
            return self.mesurements_list


class ExamReportVol(ExamReport):
    def __init__(self):
        super().__init__()

    # Sobrescreve o método 'loadProdData' p/ carregar 'T' e 'valor_min_indiv'
    # que não são carregados na classe pai
    def loadProdData(self):
        # Chamando o método da classe pai. Em seguida é carregado o que o
        # método da classe pai não é capaz de carregar
        super().loadProdData()

        # T
        try:
            self._getString2()
            string = self._string2
            str1 = 'TOLERÂNCIA INDIVIDUAL: '
            str2 = ' M'
            strT = self._getValueBetweenStrings(string.upper(), str1, str2)
            strT = strT.replace(',', '.')
            self.T = float(strT)
        except Exception:
            self.T = None

        # valor_min_indiv (Qn - T)
        try:
            self._getString3()
            string = self._string3
            str1 = 'VALOR MÍN. INDIVIDUAL: '
            str2 = ' ML'
            strV = self._getValueBetweenStrings(string.upper(), str1, str2)
            strV = strV.replace(',', '.')
            self.min_individual_value = float(strV)
        except Exception:
            self.min_individual_value = None

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getT3Values()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    #  das strings
    def _getListaMedicoes(self):
        # Carregando 'lista_medicoes' com o método da classe pai
        super()._getListaMedicoes()

        # Atribuindo lista_medicoes 'bruta' à lista 'rows'
        rows = self.mesurements_list
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

        self.mesurements_list = lst_tmp
        return self.mesurements_list


class ExamReportLength(ExamReport):
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
        self.unit_exam = lst_un_ex[1].lower()

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
        self.min_individual_value = float(strV)

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getT3Values()

    # Sobrescreve _getListaMedicoes() da classe pai para extrair os dados
    # das strings
    def _getListaMedicoes(self):
        # Carregando 'lista_medicoes' com o método da classe pai
        super()._getListaMedicoes()

        # Atribuindo lista_medicoes 'bruta' à lista 'rows'
        rows = self.mesurements_list
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

        self.mesurements_list = lst_tmp
        return self.mesurements_list


class ExamReportUnit(ExamReport):
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
        self.product_brand = self._getValueBetweenStrings(
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
        self.qn_product = lst_qn[0]

        # unid_prod
        self.unit_product = 'un.'

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
        self.min_individual_value = int(self._getValueBetweenStrings(
            string.upper(),
            str1,
            str2)
        )

        # Chamando método da classe pai para carregar os valores
        # 'valor_erro_T3' e 'total_T3'
        super()._getT3Values()

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
                self.mesurements_list.append(row[2:] + [0])
            # row tem 4 itens  (índice, cont. efet., cont. efet., n.º defeit.)
            elif len(row) == 4:
                self.mesurements_list.append(row[2:])
            if row[0] is not None and 'UNIDADE AMOSTRAL' in str(row[0]).upper():  # noqa:E501
                linhas_com_medicoes = True

        return self.mesurements_list
