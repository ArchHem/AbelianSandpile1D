import numpy as np

from Oslo_model import *

plt.rcParams.update({'font.size': 20,'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large'})

"""Testing via animation of BTW model, especially steady state 'stair' system"""
test0 = Oslo_model(32,display=True,upper_lim=1,hide_labels=True)
test0.iterate(4000)
test0.animate(interval=300)

"""Testing of Oslo model via animation"""
test1 = Oslo_model(32,display=True,upper_lim = 2,hide_labels=True)
test1.iterate(4000)
test1.animate(interval=300)

"""Testing of pile heights of L=16"""
iternum = 10000
fig2, ax2 = plt.subplots()
test2 = Oslo_model(16)
test2.iterate(iternum)
y2 = test2.get_pile_height()
avgr_pile2 = np.average(y2[16**2::])
print('Detected post stable pile height for L=16 is: %.2f' %(avgr_pile2))
ax2.scatter(np.arange(iternum+1),y2,s=0.2,color='red',label='L=16 pile heights')
ax2.grid()
ax2.set_ylabel('Pile height')
ax2.set_xlabel('Iteration number')
ax2.legend()
"""Testing of pile heights of L=32"""
iternum = 10000
fig3, ax3 = plt.subplots()
test3 = Oslo_model(32)
test3.iterate(iternum)
y3 = test3.get_pile_height()
avgr_pile3 = np.average(y3[32**2::])
print('Detected post stable pile height for L=32 is: %.2f' %(avgr_pile3))
ax3.scatter(np.arange(iternum+1),y3,s=0.2,color='red',label='L=32 pile heights')
ax3.grid()
ax3.set_ylabel('Pile height')
ax3.set_xlabel('Iteration number')
ax3.legend()

'The above two tests can be run multiple times, confirming the agreements with the provided values'

"""Testing inflow and outflow amount."""
fif4, ax4 = plt.subplots()
model4 = Oslo_model(32)
cutoff = 32**2
softrun = 10**5
run_iter = softrun + cutoff
model4.iterate(run_iter)
outflows = np.array(model4.outflows)[cutoff::]
cords = np.arange(softrun)
'''kernel length must be even'''
kernel_length_og = 500
kernel_length = kernel_length_og + 1
kernel = np.ones((kernel_length))/kernel_length
avgrd = np.convolve(outflows, kernel, mode='valid')[::2]

ax4.scatter(cords,outflows,s=6,color='green',label='Outflow for L=32')
ax4.scatter(cords,np.ones_like(cords),s=4,color='red',label='Inflow for L=32')
ax4.plot(2*np.arange(avgrd.shape[-1]),avgrd,lw=0.3,color='blue',label='Time-averaged outflow with kernel length of %.0f' %(kernel_length))
ax4.grid()
ax4.set_xlabel(r'$t$')
ax4.set_ylabel('Grain number changes in system')
ax4.legend()


"""Testing n.o. of post-stable configs, L=4"""
L = 4
gold = (1+np.sqrt(5))/2
Num_expected = int((gold*(1+gold)**L + 1/(gold*(gold+1)**L))/np.sqrt(5))

model5 = Oslo_model(L)
model5.iterate(10**6)
to_check = model5.height_doc[L**2::]
unique_rows = np.vstack({tuple(row) for row in to_check})
no_rows = unique_rows.shape[0]

print('Number of found unique states: %.2f' %no_rows)
print('Number of expected unique states %.2f:' %Num_expected)
print('Change L between 1 and 4 for to see for different values.')

plt.show()