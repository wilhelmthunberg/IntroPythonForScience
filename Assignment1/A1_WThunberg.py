#Q1
import numpy as np 
import matplotlib.pyplot as plt

pulses = np.loadtxt('pulses.csv',delimiter=',')#pulses.csv read and saved in variable "pulses" using numpy.loadtxt()
print('pulses: ', pulses)#print the numpy.ndarray pulses

#Q2
def adc_to_volts(adc):
    """
    Function to convert the ADC readings in arrays of same format as pulses.csv.

    Parameters
    ----------
    adc: array
        The ADC reading to be converted. The first column is a timestamp.

    Returns
    -------
    volts: array
          Reading converted to volts. First column is timestamps.
          
    """
    volts = np.copy(adc)#make a copy so as to not edit "adc"
    volts[:,1:] = volts[:,1:] / (2**10 - 1) * 0.6 #convert according to formula. Index '1:' used for columns since 0th column is timestamp.
    return volts

voltages= adc_to_volts(pulses)
print('\nvoltages: ' , voltages )#print voltages

#Q3

plt.figure()#create figure
plt.plot(voltages[0,1:])#plot the 0th entry of voltages
plt.xlabel('reading #')#deifine xlabel
plt.ylabel('Voltage [volts]')#define ylabel
plt.title('ADC readings of first entry in "pulses" converted to volts')#define title of the plot 
plt.savefig('Q3')#save the plot


#Q4
def baseline_correction(reading, bl_ind):
    """
    Function to adjust array in same format as pulses.csv for baseline noise 

    Parameters
    ----------
    reading: array
             The reading to be adjusted. The first column is a timestamp.
    bl_ind: array-like
            The indices that constitue baseline noise.

    Returns
    -------
    bl_corr: array
             Reading adjusted for baseline noise volts. First column is timestamps.
    """  
    bl_corr = np.copy(reading) #make a copy so as to not edit "reading"
    for i in range(0,len(bl_corr)): #for all enntries
        bl_corr[i][1:] = bl_corr[i][1:] - \
                     np.mean(bl_corr[i][bl_ind])#subtract mean of bl_ind from all readings
    return bl_corr

BL_INDICES = np.array(range(1,11)) #indices for mean of baseline 
baseline_corr = baseline_correction(voltages, BL_INDICES)
    
#Q5
ENTRY=0 #choose wich entry to plot

plt.figure()#plot the entry
plt.plot(baseline_corr[ENTRY,1:])
plt.xlabel('reading #')
plt.ylabel('Voltage [volts]')
plt.title('Readings of entry '+str(ENTRY)+' in baseline corrected voltages of "pulses"')
plt.savefig('Q5')


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


plt.figure()
plt.hist(sum_list)
plt.xlabel('Sensor reading absolute value of sum [volts]')
plt.ylabel('# of readings')
plt.title('Sensor reading sum absolute values')
plt.savefig('Q6_sum')
plt.show()


    
    
    


