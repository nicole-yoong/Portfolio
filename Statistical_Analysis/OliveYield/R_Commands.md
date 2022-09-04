# **ANOVAs and Survival Analysis**

## **1. The data in the file OliveYield.csv contains the olive oil yield (kg/season) from some olive trees. The Height (m) of the trees are also known, which are also grouped into a HeightGroup variable (low and high). The Type of tree (thought to be related to yield) is also known for each tree tested (Arbequina, Koroneiki and Maurino). You may presume the assumptions for ANOVAs and ANCOVAs are satisfied in the following questions.**
### **(a) Visualize the data and interpret what you see.**

**Step 1: Read dataset**
> df = read.csv('OliveYield.csv')

**Step 2: Drop NA (row 19)**
> df = df[-c(19),]

**Step 3: Produce table and visualization**

Effect of HeightGroup on Yield..kg.season

> df$HeightGroup = factor(df$HeightGroup)
> table(df$Yield..kg.season, df$HeightGroup)

> plot(df$Yield..kg.season~HeightGroup, data=df)
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188268276-d7644525-e3cd-4d56-bbf6-f027097c7f90.png">
</p>

> plot(df$Height..m.~df$Yield..kg.season,
+ main = 'Yield..kg.season vs HeightGroup',
+ xlab = ' Yield..kg.season ', ylab = 'HeightGroup')
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188268289-6d0998b3-25f7-4321-b4e9-e281dfbb8642.png">
</p>

Effect of Type on Yield..kg.season

> df$Type = factor(df$Type)
> table(df$Yield..kg.season, df$Type)

> plot(Yield..kg.season ~ Type, data=df)
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188268336-0c7cfb60-e03a-4fce-859b-013848a07ab5.png">
</p>

**Interpretation**

• From the boxplot, we can observe that the effect of HeightGroup on Yield..kg.season looks big,
while the effect of Type on Yield..kg.season looks big between Arbequina, Koroneiki, these both
with Maurino.

• From the scatterplot, we cannot capture a linear relationship. However, we can roughly see that
olive trees that fall in the high HeightGroup generally produce more yield in kg compared to the
ones in the low HeightGroup.

• From the interaction plot, we can observe 3 almost parallel lines, meaning that there might be no
interaction occurring. The effects for Maurino, Koreneiki and Arbequina all look similar. 

### **(b) Run a two way ANOVA to look for significant effects, using HeightGroup and Type as factors, and provide an interpretation of what you discover.**

**Questions and Hypotheses:**

**Q1: Does Yield..kg.season depend on HeightGroup?**

Null Hypothesis, H0: There are no significant differences between Yield..kg.season and HeightGroup.

Alternative Hypothesis, H1: There are significant differences between Yield..kg.season and HeightGroup.

**Q2: Does Yield..kg.season depend on Type?**

Null Hypothesis, H0: There are no significant differences between Yield..kg.season and Type.

Alternative Hypothesis, H1: There are significant differences between Yield..kg.season and Type.

**Q3: Does Yield..kg.season HeightGroup response differ by Type (I.e., are there interactions)?**

**Q4: Are there any significant effects (the ‘omnibus’ test)?**
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269399-d7eff262-b24b-42ff-9655-4a642c9e3e3b.png"  width = "550">
</p>                                                                                                          
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269411-b3781a24-78c4-4fc3-9fc9-79157258b14c.png" width = "550">

>
**Step 1: Two-way ANOVA**
> contrasts(df$HeightGroup) <- contr.sum

> contrasts(df$Type) <- contr.sum

> results = lm(df$Yield..kg.season~HeightGroup*Type, data=df)

> anova(results)

> summary(results)


**Interpretation**
• Q1: Does Yield..kg.season depend on HeightGroup? Yes (p = 0.001597)

• Q2: Does Yield..kg.season depend on Type? Yes (p < 3.153e-05)

• Q3: Are HeightGroup*Type interactions present? No (p = 0.750460)

• Q4: Are there any significant effects (the ‘omnibus’ test)? (The answer is the ‘omnibus’ test p value at the bottom of summary(results). P < 9.873e-05 indicates high significance; non-zero effects are present.)

### **(c) Run an ANCOVA using Type factor and Height covariate to look for significant effects, and provide an interpretation of what you discover.**

Factor = Type
Covariate = Height..m.
Response = Yield..kg.season.

**Step 1: Pull out variables**
> Type = df$Type
> Height..m. = df$Height..m.
> Yield..kg.season. = df$Yield..kg.season.

**Step 2: Use effect coding**
> Type = factor(Type)
> contrasts(Type) = contr.sum

**Step 3: Verify the means as shown in the table**
> Xbari. = tapply(Height..m., Type, mean)
> Ybari. = tapply(Yield..kg.season., Type, mean)
> Xbari.
> Ybari.

**Step 4: Boxplot visualization**
> dev.new()
> boxplot(Yield..kg.season.~Type)
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188268727-30e284e6-c627-43b9-85de-4f1e6e151d8f.png">
</p>

**Step 5: Try one way anova**
> result = lm(Yield..kg.season.~Type)
> anova(result)
> summary(result)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269438-2aa4a506-41c4-4e3d-9d8d-26e8deca6dd6.png" width = "550>
</p>
                                                                                                                            
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269449-66ef6baa-e611-4bdb-b67e-c4ae3ec60424.png" width = "550>
</p>
  
>
**Step 6: Fit ancova model**
> Height..m.C = Height..m. - mean(Height..m.)
> result = lm(Yield..kg.season. ~ Height..m.C + Type)
> anova(result)
> summary(result)

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269457-ed868d61-ff1c-4775-99b2-cd406a564d14.png" width = "550>
</p>
                                                                                                                            
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269461-70d549ce-4c57-4d6a-91ae-f0e54d0f4113.png" width = "550>
</p>

> df$Type = unclass(df$Type)
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/188269083-7d72f928-bea5-460e-a8db-60b77084c966.png">
</p>

**Interpretation**

• Do factors affect response? With both ANOVA and ANCOVA, the effect of Type is significant (pvalue < 0.0003297, p-value < 2.508e-07). There was a significant difference in mean Yield..kg.season. between the Type, whilst adjusting for Height..m.. The answer is yes.

• Does covariate affect response? The relationship between the response and the covariate can be accessed from the scatterplot above. The graph looks like an ideal situation for classical one-way ANCOVA; a strong increasing relationship between the covariate (Height..m.) and the response (Yield..kg.season.) within each group, and the slopes in the 3 groups look similar, with group 3 (Type = Maurino) showing a steeper slope. The answer is yes.

• MSE: A smaller MSE value is found in ANCOVA, meaning a more precise estimate and more powerful model.

• p-value: A smaller p-value is found in ANCOVA, meaning that it is more likely to reject the null hypothesis. In our case, it means that the relationship between Type and Yield..kg.season. is less significant when we consider Height..m. as the covariate.

• R2: A larger R2 value is found in ANCOVA, meaning more variance explained, which indicates it as a better model.

• Relative efficiency: Relative efficiency of ANCOVA versus ANOVA is 2.356/0.716 = 3.29; using the covariate is greatly beneficial.


### **(d) Comment with reasons on whether Height is a suitable covariate for the ANCOVA.**

Yes. Height is a suitable covariate for the ANCOVA due to the following reasons:

• Notice that the MSE for ANCOVA is about 3 times smaller than that from the ANOVA -- by making the covariate ‘a predictor’ variation attributed to it is taken away from the error and so the model is more powerful.

• There is a significant effect for the covariate – suggests that including it will change the apparent group difference on the dependent variable, Yield..kg.season..

### **(e) Comment with reasons on which of (b) or (c) is the better approach.**
Using ANCOVA is a better approach due to the following reasons:

• ANCOVA allows the application of statistical control.

• Statistical control allows the inclusion of specific covariates into the analysis. A covariate is not usually part of the main research question but could influence the response and therefore needs to be controlled for. In our study, Height..m. which could have potentially impact on the Yield..kg.season. needs to be considered when computing the relationship between Type and Yield..kg.season. To produce a more accurate result.

• ANCOVA may yield more accurate results due to the use of covariates that helps reduce the error term and correct the initial nonequivalence.

• One of the points to take note of is the choice of covariate as results can be dependent on the choice of covariate included. 
