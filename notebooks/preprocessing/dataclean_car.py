from pyspark.sql.types import *
from pyspark.sql.functions import col, isnan, when, split, regexp_replace, to_date, year, month, dayofmonth, dayofweek, dayofyear, weekofyear, upper, translate, trim
import pandas as pd
import unicodedata

class Dataclean:
    _df = None
    
    def __init__(self, df):
        self._df = df
        
    def drop_columns(self):
        self._df = self._df.drop("ANO_BO",
        "NUM_BO", 
        "NUMERO_BOLETIM", 
        "BO_INICIADO", 
        "BO_EMITIDO", 
        "BO_AUTORIA",
        "FLAGRANTE",
        "DATACOMUNICACAO", 
        "DATAELABORACAO", 
        "NUMERO_BOLETIM_PRINCIPAL", 
        "PLACA_VEICULO",
        "ESPECIE",
        "SOLUCAO",
        "EXAME",
        "RUBRICA",
        "DESDOBRAMENTO",
        "NATUREZAVINCULADA",
        "RELACIONAMENTO",
        "TIPOVINCULO",
        "NACIONALIDADE",
        "GRAUINSTRUCAO",
        "PARENTESCO")
        
    def drop_columns_after_formatted(self):
        self._df = self._df\
            .drop("DESCR_MARCA_VEICULO")
        
    def to_upper_case(self):
        self._df = self._df\
            .withColumn("SEXO", upper("SEXO"))\
            .withColumn("ESTADOCIVIL", upper("ESTADOCIVIL"))\
            .withColumn("CORCUTIS", upper("CORCUTIS"))\
            .withColumn("PERIDOOCORRENCIA", upper("PERIDOOCORRENCIA"))\
            .withColumn("LOGRADOURO", upper("LOGRADOURO"))\
            .withColumn("BAIRRO", upper("BAIRRO"))\
            .withColumn("CIDADE", upper("CIDADE"))\
            .withColumn("DESCRICAOLOCAL", upper("DESCRICAOLOCAL"))\
            .withColumn("DESCR_TIPO_VEICULO", upper("DESCR_TIPO_VEICULO"))\
            .withColumn("STATUS", upper("STATUS"))\
            .withColumn("CIDADE_VEICULO", upper("CIDADE_VEICULO"))\
            .withColumn("DESCR_COR_VEICULO", upper("DESCR_COR_VEICULO"))\
            .withColumn("NATURALIDADE", upper("NATURALIDADE"))
                
    def remove_accents(self):
        accents = 'áéíóúçãõàèìòùâêîôûñÁÉÍÓÚÇÃÕÀÈÌÒÙÂÊÎÔÛÑ'
        without_accents = 'aeioucaoaeiouaeiounAEIOUCAOAEIOUAEIOUN'
        
        self._df = self._df\
            .withColumn("PERIDOOCORRENCIA", translate("PERIDOOCORRENCIA", accents, without_accents))\
            .withColumn("LOGRADOURO", translate("LOGRADOURO", accents, without_accents))\
            .withColumn("BAIRRO", translate("BAIRRO", accents, without_accents))\
            .withColumn("CIDADE", translate("CIDADE", accents, without_accents))\
            .withColumn("DESCRICAOLOCAL", translate("DESCRICAOLOCAL", accents, without_accents))\
            .withColumn("DESCR_TIPO_VEICULO", translate("DESCR_TIPO_VEICULO", accents, without_accents))\
            .withColumn("STATUS", translate("STATUS", accents, without_accents))\
            .withColumn("CIDADE_VEICULO", translate("CIDADE_VEICULO", accents, without_accents))\
            .withColumn("DESCR_COR_VEICULO", translate("DESCR_COR_VEICULO", accents, without_accents))\
            .withColumn("NATURALIDADE", translate("NATURALIDADE", accents, without_accents))
                
    def format_dates(self):
        self._df = self._df\
            .withColumn("DATAOCORRENCIA", to_date(col("DATAOCORRENCIA"), "dd/MM/yyyy"))\
            .withColumn("HORAS", split(col("HORAOCORRENCIA"), ":", 2).getItem(0).cast(IntegerType()))\
            .withColumn("MINUTOS", split(col("HORAOCORRENCIA"), ":", 2).getItem(1).cast(IntegerType()))\
            .withColumn("ANO", year(col("DATAOCORRENCIA")))\
            .withColumn("MES", month(col("DATAOCORRENCIA")))\
            .withColumn("DIA_MES", dayofmonth(col("DATAOCORRENCIA")))\
            .withColumn("DIA_SEMANA", dayofweek(col("DATAOCORRENCIA")))\
            .withColumn("DIA_ANO", dayofyear(col("DATAOCORRENCIA")))\
            .withColumn("SEMANA_ANO", weekofyear(col("DATAOCORRENCIA")))
            
                
    def format_saint_names(self):
        self._df = self._df\
            .withColumn("CIDADE_VEICULO", 
                when((col("CIDADE_VEICULO").contains("SAO ")), regexp_replace("CIDADE_VEICULO", "SAO ", "S\."))
                .when((col("CIDADE_VEICULO").contains("SANTO ")), regexp_replace("CIDADE_VEICULO", "SANTO ", "S\."))
                .when((col("CIDADE_VEICULO").contains("SANTA ")), regexp_replace("CIDADE_VEICULO", "SANTA ", "S\."))
                .when((col("CIDADE_VEICULO").contains("STO.")), regexp_replace("CIDADE_VEICULO", "STO\.", "S\."))
                .when((col("CIDADE_VEICULO").contains("S. ")), regexp_replace("CIDADE_VEICULO", "S\. ", "S\."))
                .otherwise(col("CIDADE_VEICULO")))\
            .withColumn("CIDADE", 
                when((col("CIDADE").contains("SAO ")), regexp_replace("CIDADE", "SAO ", "S\."))
                .when((col("CIDADE").contains("SANTO ")), regexp_replace("CIDADE", "SANTO ", "S\."))
                .when((col("CIDADE").contains("SANTA ")), regexp_replace("CIDADE", "SANTA ", "S\."))
                .when((col("CIDADE").contains("STO.")), regexp_replace("CIDADE", "STO\.", "S\."))
                .when((col("CIDADE").contains("S. ")), regexp_replace("CIDADE", "S\. ", "S\."))
                .otherwise(col("CIDADE")))\
            .withColumn("NATURALIDADE", 
                when((col("NATURALIDADE").contains("SAO ")), regexp_replace("NATURALIDADE", "SAO ", "S\."))
                .when((col("NATURALIDADE").contains("SANTO ")), regexp_replace("NATURALIDADE", "SANTO ", "S\."))
                .when((col("NATURALIDADE").contains("SANTA ")), regexp_replace("NATURALIDADE", "SANTA ", "S\."))
                .when((col("NATURALIDADE").contains("STO.")), regexp_replace("NATURALIDADE", "STO\.", "S\."))
                .when((col("NATURALIDADE").contains("S. ")), regexp_replace("NATURALIDADE", "S\. ", "S\."))
                .otherwise(col("NATURALIDADE")))\
            
    def cast_types(self):
        self._df = self._df\
            .withColumn("ANO_FABRICACAO", col("ANO_FABRICACAO").cast(IntegerType()))\
            .withColumn("ANO_MODELO", col("ANO_MODELO").cast(IntegerType()))\
            .withColumn("LATITUDE", regexp_replace("LATITUDE", ",", ".").cast(DoubleType()))\
            .withColumn("LONGITUDE", regexp_replace("LONGITUDE", ",", ".").cast(DoubleType()))\
            .withColumn("IDADE", col("IDADE").cast(IntegerType()))
        
    def format_vehicle_brands_models(self):
        self._df = self._df\
            .withColumn("MARCA_VEICULO", 
                when(col("DESCR_MARCA_VEICULO").startswith("I/"), 
                    split(split("DESCR_MARCA_VEICULO", "I/", 2).getItem(1), " ", 2).getItem(0))
                .when(col("DESCR_MARCA_VEICULO").startswith("H/"), 
                    split(split("DESCR_MARCA_VEICULO", "H/", 2).getItem(1), " ", 2).getItem(0))
                .otherwise(split("DESCR_MARCA_VEICULO", "/", 2).getItem(0)))\
            .withColumn("MARCA_VEICULO", 
                when((col("MARCA_VEICULO") == "GM") | 
                    (col("MARCA_VEICULO") == "CHEV"), "CHEVROLET")
                .when((col("MARCA_VEICULO") == "VW"), "VOLKSWAGEN")
                .when(col("MARCA_VEICULO").contains("M.BENZ"), "MERCEDES-BENZ")
                .otherwise(col("MARCA_VEICULO")))\
            .withColumn("MODELO_VEICULO", 
                when(col("DESCR_MARCA_VEICULO").startswith("I/"), 
                    split(split("DESCR_MARCA_VEICULO", "I/", 2).getItem(1), " ", 2).getItem(1))
                .otherwise(split("DESCR_MARCA_VEICULO", "/", 2).getItem(1)))
            
    def format_abstence_with_null(self):
        self._df = self._df\
            .withColumn("ANO_FABRICACAO", 
                when(col("ANO_FABRICACAO") > 2023, None)
                .when(col("ANO_FABRICACAO") < 1900, None)
                .otherwise(col("ANO_FABRICACAO")))\
            .withColumn("ANO_MODELO", 
                when(col("ANO_MODELO") > 2023, None)
                .when(col("ANO_MODELO") < 1900, None)
                .otherwise(col("ANO_MODELO")))\
            .withColumn("ESTADOCIVIL", when(col("ESTADOCIVIL") == "IGNORADO", None).otherwise(col("ESTADOCIVIL")))\
            .withColumn("CORCUTIS", 
                when((col("CORCUTIS").contains("INFORMADA")) | (col("CORCUTIS").contains("OUTROS")), None)
                .otherwise(col("CORCUTIS")))\
            .withColumn("DESCR_TIPO_VEICULO", 
                when(col("DESCR_TIPO_VEICULO") == "NAO INFORMADO", None)
                .when(col("DESCR_TIPO_VEICULO").contains("INEXIST"), None)
                .otherwise(col("DESCR_TIPO_VEICULO")))\
            .withColumn("DESCR_COR_VEICULO", when(col("DESCR_COR_VEICULO") == "NAO INFORMADO", None).otherwise(col("DESCR_COR_VEICULO")))
            
    def format_street_name(self):
        self._df = self._df\
            .withColumn("LOGRADOURO", when((col("LOGRADOURO").contains("RUA")), regexp_replace("LOGRADOURO", "RUA", "R"))
                .when((col("LOGRADOURO").startswith("ALAMEDA")), regexp_replace("LOGRADOURO", "ALAMEDA", "AL"))
                .when((col("LOGRADOURO").startswith("AVENIDA")), regexp_replace("LOGRADOURO", "AVENIDA", "AV"))
                .when((col("LOGRADOURO").startswith("BECO")), regexp_replace("LOGRADOURO", "BECO", "B"))
                .when((col("LOGRADOURO").startswith("ESTRADA")), regexp_replace("LOGRADOURO", "ESTRADA", "EST"))
                .when((col("LOGRADOURO").startswith("RODOVIA")), regexp_replace("LOGRADOURO", "RODOVIA", "ROD"))
                .when((col("LOGRADOURO").startswith("TRAVESSA")), regexp_replace("LOGRADOURO", "TRAVESSA", "TV"))
                .otherwise(col("LOGRADOURO")))
            
    def format_cities_names(self):
        self._df = self._df\
            .withColumn("NATURALIDADE", 
                when(col("NATURALIDADE").contains("-"), 
                    split("NATURALIDADE", "-", 2).getItem(0))
                .when(col("NATURALIDADE").contains("/"), 
                    split("NATURALIDADE", "/", 2).getItem(0))
                .otherwise(col("NATURALIDADE")))\
            .withColumn("NATURALIDADE", trim("NATURALIDADE"))
            
    def drop_duplicates(self):
        self._df = self._df\
            .dropDuplicates(["BAIRRO", "CIDADE", "LOGRADOURO", "NUMERO", "ANO", "MES", "DIA_MES", "MARCA_VEICULO", "MODELO_VEICULO", "DESCR_COR_VEICULO"])
            
    def format_empty_values(self):
        for c in self._df.schema.fields:
            if c.dataType != DateType():
                self._df = self._df.withColumn(c.name, when(isnan(col(c.name)), None).otherwise(col(c.name)))        
                
    def get_df(self):
        return self._df
