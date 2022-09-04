# ANOVAs and Survival Analysis

## **1. The ConcHard.csv file on the Blackboard provides data on the compressive strength of Concrete Hardness (PSI) for a company producing concrete slabs under a range of industrial process Types A-E, as well as control data for the currently sold type.**

### **(a) Load the data into R, and provide a graphical display to demonstrate concrete hardness variation across the product types, and provide an initial interpretation.**

> df = read.csv('ConcHard.csv')

> Boxplot:
> colnames(df)[1]

[1] "Group"

> colnames(df)[2] = 'Hardness..PSI'
> colnames(df) = c('Group', 'Hardness..PSI')
> colnames(df)

[1] "Group"     "Hardness..PSI"

> boxplot(Hardness..PSI~Group,data = df, main='Concrete Hardness', xlab='Group', ylab='Hardness..PSI')
> points(df)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307496-ae96b0bf-e387-4afa-80ce-6bb0aad3370c.png" width = "450">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307552-c0c7b267-a83d-48c0-bfa6-c72c42cb99cb.png" width = "450">
</p>

**Interpretation**

**Range:**

• The lowest Hardness..PSI observed is 5523 while the highest is around 8382.

• Group C has the widest range among all, which ranges from around 5500 to 6350, showing that its data points significantly vary from each other.

**Median:**

• From the boxplot it can be observed that the median of different groups of concrete varies. The median Hardness..PSI of Group B and D are higher than that of Group A and Control Group, followed by Group C and E, and the dispersion across Hardness..PSI is significantly greater.

• Group A has the median that is closest to the Control Group. Group B and D have similar median, but D has a wider range. Group C and E have similar median, but C has a wider range.

**Normally distributed/Skewed:**

• None of the groups is normally distributed. They are all skewed.

• Group B are left skewed with their mean greater than median. This also means that most of the data points are small, and few are very large compared to the smaller values.

• Group A, C and D are right skewed with their means smaller than median.

• Control Group and Group D has a distribution that is almost normal.

**Outliers:**

• There are outliers in all the groups, shown by the long whiskers of each box.

**Standard deviation:**

• The standard deviations of Control Group, Group C, D, and E are similar so the hardness..PSI within each group is equally spread out. 

### **(b) Set up the null and alternative hypotheses and carry out a one way ANOVA to determine if there are any significant differences in the types of concrete produced.**

Null and alternative hypotheses:

Null Hypothesis, H0: There is no significant differences in the types of concrete produced.

Alternative Hypothesis, H1: There is significant differences in the types of concrete produced.

**One-way ANOVA using lm:**

**Step 1: Define y**
> colnames(df) = c('Group', 'Hardness..PSI')
> grp = factor(df$Group)
> y = df$Hardness..PSI

**Step 2: Perform the ANOVA**
> df.lm = lm(y ~ grp)
> anova(df.lm)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307674-73e3a97a-d02d-44dd-93da-533c330940a0.png" width = "450">
</p>

**Step 3: Examine summary**
> summary(df.lm)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307691-8ab37544-a95b-409b-aea9-e17bce25ab81.png" width = "450">
</p>

**Interpretation**

• p-value: Tells whether there is a significant difference in the mean values between the 5 groups. Since the p-value in our ANOVA table (0.8583e-10) is less than 0.05, we have sufficient evidence to reject the null hypothesis. Therefore, there are significant differences in the types of concrete produced.

**One-way ANOVA using oneway.test:**

**Step 1: Define y (previously defined)**

**Step 2: Perform the ANOVA**
> oneway.test(y ~ grp, var.equal = TRUE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307739-a114b679-8a8c-458f-ab0a-6bc1b74c22e0.png" width = "450">
</p>

**Interpretation**

• The oneway.test yields the same result as the lm. The output is more condensed compared to the lm, showing only what is important for the test. 

### **(c) Check the assumptions of your analysis and comment on the results.**

Test Assumptions:

Equal Variance Check - Levene Test
> require(lawstat)
> levene.test(y,grp,location = "median")
> levene.test(y,grp,location = "mean")
> levene.test(y,grp)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307783-0c69bb6e-e08f-4c6f-bf8b-ac36f224c008.png" width = "450">
</p>

• The p-value produced using Levene test based on absolute deviations from the median and mean is greater than 0.05 (0.9343 and 0.8542). Thus, we do not reject the null hypothesis, so we cannot reject the hypothesis that variances are equal between groups.

Equal Variance and Normality Check - lm fit to the one-way ANOVA
> plot(df.lm, which = 1)
> plot(df.lm, which = 2)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307809-7cf190f4-1651-4dcf-be7d-54a57301d77f.png" width = "450">
</p>

• The plot above shows that there is no evident relationship between residuals and fitted values (the mean of each group), so homogeneity of variances is assumed, meaning that variances are equal. If homogeneity of variances was violated, the red line would not be flat (horizontal).

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307827-4e2461c4-9ba1-4754-9457-8f7894574c29.png" width = "450">
</p>

• If the data points fall along a straight diagonal line in a Q-Q plot, then the dataset likely follows a normal distribution. Plot above shows that residuals follow approximately a normal distribution, so normality is assumed. This suggests that the samples come a normal distribution.

Normality check - Shapiro-Wilk Test
> shapiro.test(df$Hardness..PSI)

[1] w = 0.94262, p-value = 0.6728

• The Shapiro-Wilk Test tests the null hypothesis that the samples come from a normal distribution vs. the alternative hypothesis that the samples do not come from a normal distribution. In this case, the p-value of the test is 0.06728, which is more than the alpha level of 0.05. This suggests that the samples come a normal distribution.

Finding

• Variances are equal.

• Normal distribution is abided. 

### **(d) Implement comparison analyses for the following questions.**

**(i) Are any concrete types significantly harder than the control?**

Pairwise Comparison

**Step 1: Compute pairwise comparisons using t tests with pooled SD**
> pairwise.t.test(y,grp,p.adj = "none")

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307894-00cd1315-efe2-4df1-84bc-0053c2519846.png" width = "450">
</p>

**Interpretation**

• Post hoc tests (unadjusted) indicated that Group A produced a significantly harder concrete than Group Control (p-value = 0.25837).

• We found no evidence that other groups except Group A produced a significantly harder concrete than Group Control.

**(ii) Are types B and D significantly different?**

Null Hypothesis, H0: There are no significant differences between Group B and D.

Alternative Hypothesis, H1: There are significant differences between Group B and D

A. Pairwise Comparison

**Step 1: Compute pairwise comparisons using t tests with pooled SD**
> pairwise.t.test(y,grp,p.adj = "none")

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307917-fb322aaf-6f43-4a0c-b76a-fd46d1aeabb1.png" width = "450">
</p>

Interpretation

• The p-value of Group B and D is greater than 0.05 (0.91270), so we cannot reject null hypothesis. Therefore, there are significant differences between Group B and D.

B. Two-sample t-test

**Step 1: Obtain group mean, sd and length of Group B and D**
> tapply(y,grp,mean)
> tapply(y,grp,length)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307939-12f69677-dc53-493f-9528-3b9c016e54f5.png" width = "450">
</p>

**Step 2: Compute p-value**
> x2 = 7902.3
> x1 = 7878.3
> s2 = 359.7
> s1 = 373.3
> n2 = 7
> n1 = 7
> diff_in_means = x2 - x1 # µGroupD − µ1GroupB
> SE_diff_mean <- sqrt(s1^2/n1+s2^2/n2)
> t_stat <- diff_in_means/SE_diff_mean
> pvalue = 2* pt(t_stat, df=n1+n2-2)
> pvalue

[1] 1.095461

• The p-value is greater than 0.05 (1.095461), so we cannot reject null hypothesis. Therefore, there are significant differences between Group B and D.

### **(e) For all significance levels analysed, explicitly implement**

**(i) Bonferonni and**

> pairwise.t.test(y,grp,p.adj="bonferroni")

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188307989-8352fa0e-7344-4a73-9151-e8fdcc436dd2.png" width = "450">
</p>

**(ii) Holm correction for multiple testing.**

> pairwise.t.test(y,grp,p.adj="holm")
> pairwise.t.test(y,grp,p.adj="holm",pool.sd=FALSE)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308002-5ddb5c61-8cb9-467d-99b1-32c0cfb96b86.png" width = "450">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308012-6f7ead05-0cc8-43c2-acde-c6b41bd55821.png" width = "450">
</p>

**Interpretation**

• The one-way ANOVA previously executed shows a p-value of (.8583e-10), which is less than .05, rejecting the null hypothesis.

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188308038-3878492f-41dd-4fe7-b837-1764bd6d6780.png" width = "450">
</p>

Therefore, it can be concluded that not each group of concrete produces the same mean Hardness..PSI (Alternative Hypothesis, H1: There are significant differences in the types of concrete produced.). However, we can see that the ANOVA test merely indicates that a difference exists between 6 groups— it does not tell us anything about the nature of that difference. There is a risk of committing Type I error at α = .05 without any multiple testing corrections because of the false positive - when we claim there is a statistically significant effect, but there actually isn’t. 

**Comment on any differences to the conclusions for each case, and any differences observed between (i) and (ii).**

Bonferroni

Bonferroni correction is used whereby the significance level is adjusted to reduce the probability of committing a Type 1 error. When looking at the adjusted p-values, we can see that the differences between all pairs of groups except Control Group and A, Group B and D, Group C and E demonstrate a pvalue of less than 0.05. We can also see that these p-values are much higher than the unadjusted pvalues, thus, we are less likely to reject each test. Given that the Bonferroni correction has been used to guard against Type 1 errors, we can be more confident in rejecting the null hypothesis of no significant differences across these groups. That said, we can see that there exists a p-value of 1.00 between Control Group and A, Group B and D, Group C and E, implying that we cannot reject the null hypothesis of no significant differences between these 3 groups. Bonferroni can guard against Type 1 error, but it also comes with a downside of increasing the probability of committing a Type 2 error: Accepting a false null hypothesis.

Holm

Using the Holm with pooled SD, Control Group and A, Group B and D, Group C and E demonstrate a pvalue of less than 0.05, yielding a similar result as Bonferroni. The p-value produced in this case is generally smaller compared to the Bonferroni. However, when pool.sd is set to FALSE, meaning that the standard two sample t-test is applied to all possible pairs of groups. The test just uses the p-values from the pairwise Welch t-tests, making the overall p-value for each pair increase compared to the pooled Holm. More groups produce a p-value greater than 0.05, including Group A and C, Control Group and A, Control Group and C, Group B and D,
Group C and E, implying that we cannot reject the null hypothesis of no significant differences between these 5 groups. Comparing the pooled and unpooled Holm testing, unpooled Holm is less likely to reject null hypothesis compared to pooled Holm, reducing the chance of committing Type 1 error causing the false positive, where we claim there is a statistically significant effect, but there actually isn’t. Overall, Holm is more superior. It has more power and still strictly controls the familywise error rate.
