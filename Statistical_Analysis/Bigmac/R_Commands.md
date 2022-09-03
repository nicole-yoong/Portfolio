# Statistical Analysis on the Bigmac.csv

## **1. Consider the data set bigmac.cvs dataset obtainable from the module’s Blackboard site.**
### **(a) Using the relevant R-commands, find the names of the variables. **

> bigmac <- read.csv('C:/Users/wgq21ryu/bigmac.csv')

[1] "bigmac" "bread" "busfare" "engsal" "engtax" "service"
[7] "teachsal" "teachtax" "vacdays" "workhrs" "city" 

### **(b) Using the relevant R-commands:
i. Compute the mean, variance and standard deviation for the variable bus fare. In each case
exclude the values for Mexico City, Milan, Montreal, Nairobi, New York, Nicosia and Sydney using
the relevant R-commands. **


**Step 1: Create a new dataframe ‘bigmac2’ to exclude these countries:**
> bigmac2<-subset(bigmac,city!="Mexico City" & city!="Milan" & city!="Montreal" &
city!="Nairobi" & city!="New York" & city!="Nicosia" & city!="Sydney")

**Step 2: Double check the row numbers for the new dataframe:**
> nrow(bigmac)
[1] 45

> nrow(bigmac2)
[2] 38

**Step 3: Compute the mean, variance and standard deviation for the variable bus fare using the
new dataframe ‘bigmac2’**

**Step 3.1: Define variable bus fare**
x = c(bigmac2[,3])

Mean:
> mean(x)
[1] 0.9610526

Variance:
var(x)
[1] 0.4271502

Standard Deviation:
sd(x)
[1] 0.6535673

**ii. Name the cities that have the lowest bus fare, the highest bus fare. Which city’s bus fare is below
the mean but above the median?**

Lowest bus fare:
bigmac[(bigmac$busfare==min(x)),11]
[1] "Bogota" "Bombay" "Mexico City"

Highest bus fare:
> bigmac[(bigmac$busfare==max(x)),11]
[1] "Stockholm"

Below mean and above median:
> bigmac[(bigmac$busfare<mean(x))&(bigmac$busfare>median(x)),11]
character(0)

### **(c) Construct notched box-and-whisker plots in blue for the list of original bus fares and also the list
of bus fares with Mexico City, Milan, Montreal, Nairobi, New York, Nicosia and Sydney excluded.**

**Step 1: Define the bus fares for original list, and new list excluding certain countries**
> x = c(bigmac2[,3]) ----- new list excluding certain countries
> x
[1] 1.27 0.27 0.09 0.09 1.11 0.24 0.20 1.13 2.46 1.18 1.49 1.37 1.21 1.80 0.77 0.85 1.00 0.23
[19] 0.70 1.85 1.10 0.84 1.06 0.30 1.88 0.20 0.82 0.24 0.37 0.59 0.52 2.66 0.33 0.73 1.32 0.99
[37] 1.38 1.88

> y = c(bigmac[,3]) ----- original list
> y
[1] 1.27 0.27 0.09 0.09 1.11 0.24 0.20 1.13 2.46 1.18 1.49 1.37 1.21 1.80 0.77 0.85 1.00 0.23
[19] 0.70 1.85 1.10 0.84 1.06 0.30 0.09 0.77 1.25 0.20 1.15 0.51 1.88 0.20 0.82 0.24 0.37 0.59
[37] 0.52 2.66 2.06 0.33 0.73 1.32 0.99 1.38 1.88

**Step 2: Plot individual box-and-whisker plots in blue**
Original:
> boxplot(y, col='Blue', notch=TRUE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267545-46853ab7-b4bf-4f5f-a04b-ef93196a1409.png">
</p>

New List:
> boxplot(x, col='Blue', notch=TRUE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267556-7b1aeba4-c876-49bb-94aa-5958a8e0e571.png">
</p>


**i) Use the relevant R commands to combine your two notched box-and-whisker plots into a single
figure such that the y-axis is entitled bus fare and the x-axis is entitled study. The x-axis should have
two values called with and without where with refers to the original list of bus fares and without to
the list of bus fares with Mexico City, Milan, Montreal, Nairobi, New York, Nicosia and Sydney
excluded.**

> boxplot (y,x, col='Blue',names=c('With','Without'), ylab = 'Bus Fare', notch=TRUE)
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267565-a3971724-33f9-4ac8-8fbc-4cf6917c45df.png">
</p>

**ii. Interpret your result with regards to the notches and the horizontal lines and explicitly state their
respective values for both box-and whisker plots (maximum of 120 words.)**

[With (W) / Without (WO)]
> summary(y) [W]
 Min. 1st Qu. Median Mean 3rd Qu. Max.
0.0900 0.3300 0.8500 0.9456 1.2700 2.6600
1.
> summary(x) [WO]
 Min. 1st Qu. Median Mean 3rd Qu. Max.
0.0900 0.3400 0.9200 0.9611 1.3075 2.6600

The upper and lower whisker show values of 2.66 and 0.09, and there is no obvious outlier being
shown in the graph.
WO shows a slightly higher Q3 an Q1 than W, indicating that 50% of the bus fare in the dataset of
WO is more expensive. This plot suggests that WO has a greater bus fare, but the overlapping
notches indicate the difference in medians is not statistically significant.
The median of both plots is not in the middle of the box, meaning that the data is positively
skewed, where the median is closer to the lower or bottom quartile. This indicates that the mean
is greater than median. The imbalance in the whisker lengths also indicates that the number of
outliers is greater in one side.

### **(d) Create a scatterplot for the variables engsal and teachsal such that the x-axis is labelled by
teachsal, the plot characters are red crosses, the y-axis is labelled by engsal and the plot is entitled
teacher salary vs engineer salary.**

**Step 1: Define engsal (y) and techsal (x)**
> y = c(bigmac[,4])
> x = c(bigmac[,7])

**Step 2: Create the scatterplot**
> plot(x,y, xlab='teachsal', ylab='engsal', main = 'Teacher Salary vs Engineer Salary',pch = 4, col = 'Red')

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267636-416c8248-1f95-4123-86be-9dd7ad54f7d8.png">
</p>

### **(e) Assuming that the relationship between teacher salary and engineer salary is captured by a
simple linear regression model, fit a Least Squares Regression line through the dataset where
engineer salary is the response variable.
Redo the plot you have generated in Question 1d with the Least Squares Regression line included. **

For this to work we are implicitly assuming there is a linear relationship between x and y i.e. y = ax + b

**Step 1: Compute the Least Regression Line**
> Sxy = sum((x - mean(x)) * (y - mean(y)))
> Sxx = sum((x - mean(x)) ^ 2)
> Syy = sum((y - mean(y)) ^ 2)
> c(Sxy, Sxx, Syy)
[1] 11612.750 9569.532 17144.359

> beta_1_hat = Sxy / Sxx
> beta_0_hat = mean(y) - beta_1_hat * mean(x)
> c(beta_0_hat, beta_1_hat)
[1] 6.831594 1.213513

> lm (y~x)
Call:
lm(formula = y ~ x)
Coefficients:
(Intercept) x
 6.832 1.214

**Step 2: Create the scatterplot**
> plot(x,y, xlab='teachsal', ylab='engsal', main = 'Teacher Salary vs Engineer Salary',pch = 4, col =
'Red')
> abline(lm(y~x))

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267673-f3afc9a5-c332-47b8-bd95-76a6ad4cee11.png">
</p>

### **(f) Using the relevant R commands, find the city for which the predicted engineer salary is above 60
monetary units.**

**Step 1: Define variable to predict engsal based on teachsal**
> y = c(bigmac[,4])
> x = c(bigmac[,7])
>
**Step 2: Predict the number**
> linear_model = lm(y~x)
> predicted = predict(linear_model)

**Step 3: Add another new column ‘pred_engsal’ to the dataframe**
> bigmac$pred_engsal <- predicted

**Step 4: Filter the city with pred_engsal greater than 60**
> bigmac[(bigmac$pred_engsal>60),11]
[1] "Geneva" "Luxembourg" "Zurich"

### **(g) Redo the plot in Question 1e with the residuals added.**
> plot(x,y, xlab='teachsal', ylab='engsal', main = 'Teacher Salary vs Engineer Salary')
> abline(lm(y~x))
> fitted<- predict(lm(y~x))
> for (i in 1 : 24) lines(c(x[i], x[i]),c(y[i],fitted[i]))

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267711-0d929038-7c9b-49f0-9522-f8d193384627.png">
</p>

### **(h) Are the variables engsal and teachsal correlated? Justify your answer using the relevant formulas
but not a scatterplot.**
> cor.test(x, y)
      Pearson's product-moment correlation
      
 data: x and y
 t = 14.09, df = 43, p-value < 2.2e-16
 alternative hypothesis: true correlation is not equal to 0
 95 percent confidence interval:
   0.8354214  0.9479007
 sample estimates:
      cor
 0.9066279
 
ANSWER: Yes they are highly correlated. 

**(i) Create a histogram for workhrs using 11 bins. **

**Step 1: Define x**
> x <- bigmac[,10]
> x
[1] 1714 1792 2152 2052 1708 1971 2041 1924 1717 1759 1693 1650 1880 1667 2375
[16] 1978 1945 2167 1786 1737 2068 1768 1710 2268 1944 1773 1827 1958 1942 1825
[31] 1583 2078 1744 1749 1856 1842 2042 1805 1668 2145 2015 1880 1888 1780 1868

**Step 2: Create histogram**
> hist(x,breaks = 11, xlab = 'Workhrs', main = 'Histogram of workhrs (11 bins)')

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188267800-9f747e9a-3086-49eb-b8c0-e520e54c747e.png">
</p>

###**(j) Is the assumption that workhrs is normally distributed justified?**
ANSWER: No, the histogram shows that the workhrs is skewed to the left and the mean is not
equal to median. 

### **(k) Assume that the values in workhrs are distributed normally. For each of the following two
questions assume symmetry and use as mean and standard deviation the mean and standard
deviation of the dataset, respectively.
i. Find the probability that a value for workhrs selected at random lies between 1700hrs and
1900hrs.**

ASSUMPTION: We assume that it is a normal distribution whose mean is zero, and whose
variance is one is called the Standard Normal distribution (SND). We apply SND to compute the
z-score.

**Step 1: Compute z-score**
> (1700-mean(x))/sd(x)
[1] -1.045259

> (1900-mean(x))/sd(x)
[1] 0.09723929

**Step 2: Compute probability**
> pnorm(0.09723929)
[1] 0.5387318

> pnorm(-1.045259)
[1] 0.1479516

> 0.5387318 - 0.1479516

ANSWER: [1] 0.3907802

**ii. Find the two values so that we can expect 40% of the reported workhrs to lie between them.**

> qnorm(c(0.30, 0.70))



