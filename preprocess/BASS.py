from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np
#time intervals
t= np.array([3, 4, 5])
# sales vector
sales=np.array([1000000 ,1349583 ,1450994 ])
# cumulatice sales
c_sales=np.cumsum(sales)
# initial variables(M, P & Q)
vars = [3800577 
,  0.03,0.38]

# residual (error) function
def residual(vars, t, sales):
    M = vars[0]
    P = vars[1]
    Q = vars[2]
    Bass = M * (((P+Q)**2/P)*np.exp(-(P+Q)*t))/(1+(Q/P)*np.exp(-(P+Q)*t))**2 
    return (Bass - (sales))
                 
# non linear least square fitting
varfinal,success = leastsq(residual, vars, args=(t, sales))

# estimated coefficients
m = varfinal[0]
p = varfinal[1]
q = varfinal[2]


print(varfinal)
#sales plot (pdf)
#time interpolation
tp=(np.linspace(1.0, 110.0, num=100))/10
tp= np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
cofactor= np.exp(-(p+q) * tp)
sales_pdf= m* (((p+q)**2/p)*cofactor)/(1+(q/p)*cofactor)**2
for i in sales_pdf:
    print(i)
print(sales_pdf)
plt.plot(tp, sales_pdf,t,sales, marker = 'o')
plt.title('Sales pdf')
plt.legend(['Fit', 'True'])
plt.show()


# Cumulative sales (cdf)
sales_cdf= m*(1-cofactor)/(1+(q/p)*cofactor)
plt.plot(tp, sales_cdf,t,c_sales)
plt.title('Sales cdf')
plt.legend(['Fit', 'True'])
plt.show()