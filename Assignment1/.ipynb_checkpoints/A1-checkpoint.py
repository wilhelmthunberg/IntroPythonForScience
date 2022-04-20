#Q1
import numpy as np #
import matplotlib.pyplot as plt

pulses = np.loadtxt('pulses.csv',delimiter=',')#pulses.csv read and saved in variable "pulses" using numpy.loadtxt()
print(pulses)#print the numpy.ndarray pulses

#Q2
voltages = np.copy(pulses)#make a copy so as to not edit "pulses"
voltages[:,1:] =  voltages[:,1:] / (2**10 - 1) * 0.6 #convert according to formula. Index 1: used for columns since 0th column is timestamp.
print(voltages)#print voltages

#Q3
plt.figure()#create figure
plt.plot(voltages[0,1:])#plot the 0th entry of voltages
plt.xlabel('reading #')#deifine xlabel
plt.ylabel('Voltage [volts]')#define ylabel
plt.title('ADC readings of first entry in "pulses" converted to volts')#define title of the plot 
plt.savefig('Q3')#save the plot
plt.show()#show the plot

#Q4
baseline_corr = np.copy(voltages) #make a copy so as to not edit "voltages"
BL_INDICES = range(1,10) #indices for mean of baseline defined for 
for i in range(0,len(baseline_corr)): #for all enntries
    baseline_corr[i][1:] = baseline_corr[i][1:] - np.mean(baseline_corr[i][BL_INDICES])#subtract mean of first 10 from all readings
    
#Q5
ENTRY=0 #choose wich entry to plot

plt.figure()#plot the entry
plt.plot(baseline_corr[ENTRY,1:])
plt.xlabel('reading #')
plt.ylabel('Voltage [volts]')
plt.title('Readings of entry '+str(ENTRY)+' in baseline corrected voltages of "pulses"')
plt.savefig('Q5')
plt.show()

#Q6
max_list= [] #create lists to store max values and sums
sum_list = []

for i in baseline_corr[:,1:]: #for each line(entry) in pulses append max absolute value and sum of all values
    max_list.append(np.abs(np.min(i)))
    sum_list.append(np.abs(np.sum(i)))

plt.figure() #Plot results as histograms
plt.hist(max_list)
plt.xlabel('Sensor reading maximum absolute value [volts]')
plt.ylabel('# of readings')
plt.title('Sensor reading maximum absolute values')
plt.savefig('Q6_max')
plt.show()

plt.figure()
plt.hist(sum_list)
plt.xlabel('Sensor reading sum absolute value [volts]')
plt.ylabel('# of readings')
plt.title('Sensor reading sum absolute values')
plt.savefig('Q6_sum')
plt.show()


    
    
    


