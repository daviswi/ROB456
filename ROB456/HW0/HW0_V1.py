#ROB456 HW0
#Import python libraries
import numpy as np
import matplotlib.pyplot as plt
np.random.seed(0)

#Step 1: Create a polynomial function
def f_x(x_in):
   c = np.array([-0.1, 4.0, -0.1, 10.0], float)
   p = np.polyval(c, x_in)
   return p

#plot formatting function
def plot_format(axh, xlim=None, title='', xlabel='x', ylabel='f(x)'):
   if xlim is not None:
      axh.set_xlim(xlim)
   axh.set_title(title)
   axh.set_xlabel(xlabel)
   axh.set_ylabel(ylabel) 

#Main program
#x = 5.5
#y = f_x(x)
#print(y)

#Setp 2: plot the polynomial
xlim = [-10.0, 25.0]
x = np.linspace(xlim[0], xlim[1], 351, float)
y = f_x(x)

#matplotlib stuff, declaring 2 variables
fh1, axh1 = plt.subplots()
axh1.plot(x, y, 'b-')

#Set Specification
#axh1.set_xlim(xlim)
#axh1.set_title('Original Polynomial')
#axh1.set_xlabel('x')
#axh1.set_ylabel('f(x)')
plot_format(axh1, xlim, 'Original polynomial')
fh1.savefig('hw0_Original_Polynomial.pdf', bbox_inches = 'tight')

#Step 3: Chop up into 14 bins
b_width = (xlim[1] - xlim[0])/14.0
x_bin = np.arange(xlim[0], xlim[1], b_width, float)
y_bin = f_x(x_bin)
fh2, axh2 = plt.subplots()
axh2.bar(x_bin + b_width/2.0, y_bin, width=b_width, edgecolor = 'k')


#Set Specification
#axh1.set_xlim(xlim)
#axh1.set_title('Discretized bins')
#axh1.set_xlabel('x')
#axh1.set_ylabel('f(x)')
plot_format(axh2, xlim, 'Discretized bins')
fh1.savefig('hw0_disretized_bins.pdf', bbox_inches = 'tight')

#step 4: Turn into pdf by normalizing
y_bin_norm = y_bin / y_bin.sum()
fh3, axh3 = plt.subplots()
axh3.bar(x_bin + b_width/2.0, y_bin_norm, width=b_width, edgecolor='k')
plot_format(axh3, xlim, 'Discetized bins (normalized) sum = %s' %(y_bin_norm.sum()), ylabel='p(x)') 
fh3.savefig('hw0_discretized_bins_normalized.pdf', bbox_inches='tight')

#Step 5: take 500 samples from pdf
#Step 5.1: use random(500) to generate 500 sameple from uniform random distribution
n_samples = 500
x_rand = np.arange(1, n_samples+1, 1, int)
y_rand = np.random.random(n_samples)
fh4, axh4 = plt.subplots()
axh4.plot(x_rand, y_rand, 'k+')
plot_format(axh4, [1, n_samples], '%s samples, uniformly distributed' % n_samples)
fh4.savefig('hw0%s_uniform_random.pdf' %n_samples, bbox_inches='tight')

#Step 5.2 (incorrect): shift points to lie between [-10, 25]
y_rand_scaled = y_rand * (xlim[1] - xlim[0]) + xlim[0]
fh5, axh5 = plt.subplots()
axh5.plot(x_rand, y_rand_scaled, 'k+')

#plot bin ranges
for i in range(0, len(x_bin)):
   axh5.plot([1, n_samples], [x_bin[i], x_bin[i]])

plot_format(axh5, [1, n_samples], 'Random samples mapped to x ranges of bins')
fh5.savefig('hw0_random_to_bin_ranges.pdf', bbox_inches='tight')


#Step 5.3
y_count_incorrect = np.zeros(x_bin.shape)
for i in range(0, len(y_rand_scaled)):
   for j in range(len(x_bin), 0, -1):
      if y_rand_scaled[i] > x_bin[j-1]:
         y_count_incorrect[j-1] += 1
         break

fxh6, axh6 = plt.subplots()
axh6.bar(x_bin + b_width/2.0, y_count_incorrect, width=b_width, edgecolor='k')
plot_format(axh6, xlim, 'Samples per bin (incorrect)', ylabel='smaples')
fxh6.savefig('hw0_samples_per_bin_incorrect.pdf', bbox_inches='tight')

#Step 5.2 (correct) leave the samples lying between 0 and 1
#step 5.3 (correct) use the cdf to divide up the space
y_bin_cdf = y_bin_norm.copy()
i=0
while i < len(y_bin_cdf) - 1:
   i += 1
   y_bin_cdf[i] += y_bin_cdf[i-1]

fh7, axh7 = plt.subplots() 
axh7.plot(x_rand, y_rand, 'k+')

for i in range(0, len(y_bin_cdf)):
   axh7.plot([1, n_samples], [y_bin_cdf[i], y_bin_cdf[i]])

axh7.set_title('Dividing up he samples according to bin height')
fh7.savefig('hw0_correct_sample_division.pdf', bbox_inches='tight')

#samples per bin ###########
#############################################if statement??
y_count_correct = np.zeros(x_bin.shape)
for i in range(0, len(y_rand)):
   for j in range(0, len(y_bin_cdf)):#len(y_count_correct)):#len(y_bin_cdf)):
      #if y_bin_cdf[i] < y_count_correct[j-1]:  #if y_rand[i] > x_bin[j-1]:
      if y_rand[i] < y_bin_cdf[j]:
         y_count_correct[j] += 1
         break

#fh8, axh8 = plt.subplots()
#axh8.bar(x_bin + b_width/2.0, y_count_correct, width=b_width, edgecolor = 'k')
#plot_format(axh8, xlim, 'Samples per bin (correct)', ylabel='samples')
#fh8.savefig('hw0_samples_per_bin_correct.pdf', bbox_inches='tight')

#xlimbar = [0.0, 1]

#y_count_correct = np.zeros(x_bin.shape)
#for i in range(0, len(y_rand_scaled)):
#   for j in range(len(x_bin), 0, -1):
#      if y_rand_scaled[i] > x_bin[j-1]:
#         y_count_correct[j-1] += 1
#         break
#sorted_list = y_count_correct.sort();

fxh8, axh8 = plt.subplots()
axh8.bar(x_bin + b_width/2.0, y_count_correct, width=b_width, edgecolor='k')
plot_format(axh8, xlim, 'Samples per bin (correct)', ylabel='samples')
fxh8.savefig('hw0_samples_per_bin_incorrect.pdf', bbox_inches='tight')

#y_pos = np.arange(len(objects))

#y_bin_norm = y_bin / y_bin.sum()

################
################
##Part 2
################
# Normalize original polynomial plot
p_area = y.sum() * (x[1]-x[0])
y_norm = y/p_area

# Create a figure handle to contain subplots
fh10 = plt.figure(figsize=(12, 4))

# Step 1: Generate 500 uniformly distributed samples in the range 0 to 1 as you did in Step 5.1 above. This time, for each sample, store two numbers - an x value (found by shifting the sample to lie in [-10,25], as in 5.2 above) and a y value (found by evaluating the polynomial at x). Normalize the polynomial (and the samples) as in Step 6 above.
n_samples = 500
s_rand = np.zeros([n_samples, 2])
s_rand[:, 0] = np.random.random(n_samples)
s_rand[:, 0] = s_rand[:, 0] * (xlim[1] - xlim[0]) + xlim[0]
s_rand[:, 1] = f_x(s_rand[:, 0])/p_area

axh10a = fh10.add_subplot(131)
axh10a.plot(x, y_norm, 'b-', label='Normalized polynomial')
axh10a.plot(s_rand[:, 0], s_rand[:, 1], 'k+', label='Samples')
plot_format(axh10a, title='Normalized polynomial with samples', ylabel='p(x)')
axh10a.legend()




#Second Problem
#nR_samples = 1000

#x_binMax = np.arange(xlimMax[0], xlimMax[1], b_width, float)
#xlim = [0.0, 1.0]
#x_binMax = np.arrange(xlimMax[0], xlimMax[1], b_width, float)

y_rand_scaled = y_rand * (xlim[1] - xlim[0]) + xlim[0]
fh11, axh11 = plt.subplots()
#axh5.plot(x_rand, y_rand, 'k+')

#plot bin ranges
for i in range(0, len(x_bin)):
   axh11.plot([1, n_samples], [x_bin[i], x_bin[i]])

plot_format(axh11, [1, n_samples], 'Random samples mapped to x ranges of bins')
fh11.savefig('hw0_random_to_bin_ranges.pdf', bbox_inches='tight')



#Part 3
p_area = y.sum() * (x[1]-x[0])
y_norm = y/p_area

# Create a figure handle to contain subplots
fh10 = plt.figure(figsize=(12, 4))

# Step 1: Generate 500 uniformly distributed samples in the range 0 to 1 as you did in Step 5.1 above. This time, for each sample, store two numbers - an x value (found by shifting the sample to lie in [-10,25], as in 5.2 above) and a y value (found by evaluating the polynomial at x). Normalize the polynomial (and the samples) as in Step 6 above.
n_samples = 500
s_rand = np.zeros([n_samples, 2])
s_rand[:, 0] = np.random.random(n_samples)
s_rand[:, 0] = s_rand[:, 0] * (xlim[1] - xlim[0]) + xlim[0]
s_rand[:, 1] = f_x(s_rand[:, 0])/p_area

axh10a = fh10.add_subplot(131)
axh10a.plot(x, y_norm, 'b-', label='Normalized polynomial')
axh10a.plot(s_rand[:, 0], s_rand[:, 1], 'k+', label='Samples')
plot_format(axh10a, title='Normalized polynomial with samples', ylabel='p(x)')
axh10a.legend()




#plot
plt.show()