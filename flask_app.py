x = 1
y = 2

try:
    data.to_csv("fsa.csv")
except Exception as e:
    print(e)
try:
    print(x+y)
except:
    pass