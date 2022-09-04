# **ANOVAs and Survival Analysis**

## **1. The duration of a staphylococcus infection (days) for patients are recorded in a clinical trial comparing two new antibiotics (Entromyacin and Selovyacin) over a period of 2 weeks. Censoring information is also available (0=censored, 1=cured). The data can be found in StaphSurv.csv**

### **(a) Produce Kaplan Meier survival plot(s) for the data and provide an initial interpretation.**

> df = read.csv('StaphSurv.csv')
> require(KMsurv)
> library(survival)
> fit <- survfit(Surv(Time, Status) ~ 1, data = df) 
> dev.new()
> plot(fit, main="Censoring Done Properly", xlab="Time (Days)", ylab="S(t)",mark.time=TRUE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308261-fc2ee3b0-6c59-4e11-ba36-866759af9fac.png" width = "450">
</p>

Comparison of survival

> fit <- survfit(Surv(Time, Status) ~ Drug, data = df)
> print (fit)
> dev.new()
> plot(fit,main="Censoring Done Properly by Group", xlab="Time (Days)", ylab="S(t)",col=c(1,2),mark.time=TRUE,conf.int=TRUE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308285-e00b21ac-2345-4629-9103-d395873c92bc.png" width = "450">
</p>

**Interpretation**

• The probability of surviving 5 days is 100% for Selovyacin; conversely, it is around 96% for Entromyacin.

Survival probabilities

• The survival probabilities for the Selovyacin are higher than the survival probabilities for the Entromyacin at the first 5 days, suggesting a survival benefit. However, the survival probability of Selovyacin after 5 days drops lower than the Entromyacin (a lower survival curve), indicating a worse prognosis compared to Entromyacin.

• Entromyacin curve is higher than the Selovyacin after 5 days, showing a higher probability of survival and a better prognosis than the Selovyacin.

• The survival probability for seems that it decreases at a slightly higher rate in the first 9 days than the Entromyacin. 

Fluctuation of survival rate.

• For the Entromyacin the survival rate seems to have more fluctuations. Looking at the horizontal line, they tend to alternate from being shorter and longer from time to time. In the meantime, Selovyacin demonstrates a longer horizontal line as the number of days increase, implying that the beneficial effects of the Selovyacin over the Entromyacin are greater the longer one stays in remission.

Log-rank p-value

• The log-rank p-value of 0.03 indicates a significant result considering p < 0.05 to indicate the two curves are statistically significantly different. The sample can rule out a real difference and avoid Type II error (false negative). 

> summary(fit)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308366-ca90384a-f734-489e-ae9b-59211ae5f421.png" width = "450">
</p>

### **(b) Do a log-rank test to investigate the significance of differences between the two treatments, and interpret the results.**

Hypothesis:

Null Hypothesis, H0: There is no difference in survival between the two groups.

Alternative Hypothesis, H1: There is a difference in survival between the two groups.

> survdiff(Surv(Time,Status)~ Drug,data=df,rho=0)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308397-e412ce79-e400-4c80-88ef-f86667c94d74.png" width = "450">
</p>

Interpretation

• A p-value of 0.03 provides evidence that the two survival curves are different. We reject the null hypothesis stating that there is no difference in survival between the two groups. In other words, we have sufficient evidence to say that there is a statistically significant difference in survival between the two groups.

• Overall, the drug is significantly effective.
