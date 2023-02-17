import FinanceDataReader as fdr


df = fdr.DataReader("005930", "2018-01-01")
print(df.head())