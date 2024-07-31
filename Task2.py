from Oslo_model import *
from scipy.optimize import curve_fit

lengths = np.array([2 ** i for i in range(9)])
stable_cycles = 10 ** 5
iteration_length = np.amax(lengths) ** 2 + stable_cycles
plt.rcParams.update({'font.size': 16,'axes.labelsize': 32,
         'axes.titlesize': 32})
figa, axa = plt.subplots()
heights_vs_time = np.zeros((len(lengths), int(iteration_length + 1)))


for i in range(len(lengths)):
    modelsa = Oslo_model(lengths[i])
    modelsa.iterate(iteration_length)
    heights_vs_time[i] = modelsa.height_doc[:, 0]
    axa.plot(np.arange(iteration_length + 1), heights_vs_time[i], label='System of length %.0f' % lengths[i], lw=1,ls='--')

axa.legend(loc='upper right')
axa.set_ylabel('Pile Height')
axa.set_xlabel('Iteration number')

"""
axa.set_yscale('log')
axa.set_xscale('log')
"""

axa.grid()
axa.set_title('Plot of time evolution of heights')

figb, axb = plt.subplots()
linlength = np.array([2 ** i for i in range(9)])
maxiter = linlength ** 2 + linlength
avg_system_number = 30
avg_num = []
height_evuls = []

for i in range(len(linlength)):
    loavg = 0
    avg_heigh_evul = np.zeros((maxiter[i]+1,))
    for j in range(avg_system_number):
        loc_model = Oslo_model(linlength[i])
        loc_model.iterate((maxiter[i]))
        outflows = np.array(loc_model.outflows)
        heights = loc_model.height_doc[:,0]
        index_finder = np.where(np.array(outflows) > 1, 1, np.array(outflows))
        TC = np.argmax(index_finder)
        loavg = loavg + TC
        avg_heigh_evul = avg_heigh_evul + heights
    avg = loavg / avg_system_number
    avg_num.append(avg)
    height_evuls.append(avg_heigh_evul/avg_system_number)

axb.scatter(linlength, np.array(avg_num), lw=0.2, color='red', label='Average cross-over-time')


def parabola(x, a):
    return a * x ** 2


param, cov = curve_fit(parabola, linlength, np.array(avg_num))
print('Covariant matrix of parabolic fit is:')
print(cov)
plotval = np.linspace(linlength[0],linlength[-1],5000)
axb.plot(plotval, parabola(plotval, *param), color='green', label='Fitted parabolic function',ls='--')
axb.grid()
axb.legend()
axb.set_xlabel('System length')
axb.set_ylabel('Cross-over-time')
axb.set_title('Cross-over-time')

b = param
figd, axd = plt.subplots()

def estimated_growth(t,a):

    return a*np.sqrt(t)


pvals = []
cvals = []

for i in range(3,len(height_evuls)):
    nruns = len(height_evuls)
    loctime = (np.arange(0,len(height_evuls[i]),1)/(b*linlength[i]**2))
    locy = (height_evuls[i]/(linlength[i]))[0:int(avg_num[i])]
    sqrtparam, sqrtcov = curve_fit(estimated_growth,loctime[0:int(avg_num[i])],locy)
    cvals.append(np.sqrt(sqrtcov[0,0]))
    pvals.append(sqrtparam[0])
    axd.plot(loctime,height_evuls[i]/(linlength[i]),label = 'Time evolution for system of size %.0f' %(linlength[i]),
             ls='--',color=(0.2,1-i/nruns,i/nruns))


sparam = np.average(np.array(pvals),weights=1/np.array(cvals))
print('Found sqrt factor is: %.3f' %(sparam))
plotting_regime = np.linspace(0,1,1000)
axd.plot(plotting_regime,estimated_growth(plotting_regime,sparam),color = 'red',label = "Transient regime's time evolution",lw=2.5)

axd.grid()
axd.legend()
axd.set_xlabel(r"$t' = \frac{t}{bL^2}$")
axd.set_ylabel(r"$\frac{H(t',L)}{L}$")
axd.set_title('Rescaled height evolution')

"""
axd.set_yscale('log')
axd.set_xscale('log')
"""

plt.show()
