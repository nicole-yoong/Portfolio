# Data-Preprocessing 

## **Handling missing values**

We'll consider that when more than 15% of the data is missing, we should delete the corresponding variable after confirming their importance.

There are approximately 48 variables showing over 15% of missing values, and out of them there are a huge proportion of variables with over 60% of missing values. From the table below, a large proportion of the missing values are related to the first hour (h1) tests conducted during the patients’ unit stay. It might indicate that the first 24 hours (d1) tests are more important to diagnose diabetes. In these cases, we assume that these variables with large missing values play lesser
importance and can be removed.

If we were to remove all the columns with missing values, there would only be 13 columns left.

If we were to remove all the rows with missing values, there would only be 9940 rows left.

### **Imputation**

For the variables with less than 60% of missing values, we will impute the values of all variables except ethnicity and gender with mean value. We fill the missing values with the value before it (in the cell before) and then with 0. This method seems to work well as the new mean is closer to the original data. 

### **Random Fill-in**

The missing values of ethnicity and gender are replaced with a random choice. We do not want to remove these features as they might be correlated to the diabetes.

## **Removing columns**

### **Removing not useful columns**

height and weight are removed since they are related to bmi. encounter_id and hospital_id is the primary keys of the data frame that do not seem to affect the diabetes, therefore, are removed. 

readmission_status is removed as no one is re-admitted.

### **Removing highly correlated variable**

The correlation test presents the highly correlated variables to be removed.

'd1_albumin_min', 'd1_bilirubin_min', 'd1_bun_min', 'd1_platelets_min', 'd1_wbc_min', 'h1_glucose_min' show high correlation with other variables in the data frame and this is verified by examining their correlation with a potential correlated variable, e.g. d1_bilirubin_min and d1_bilirubin_max shows a correlation of 0.99.

### **Categorical encoding**

gender, ethnicity, icu_type are transformed into numeric using Label Encoder as Label Encoder since there is no ordinal scale

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189850057-09f3c89c-e5ed-42a3-90a8-923998ee5b36.png" width = 200">
</p>
                                                                                                                               
### **Examining outliers**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189850147-bf5fd336-8729-4d04-b87c-700bf1675b68.png" width = 800">
</p>

From the boxplot we can observe outliers in several variables such as h1_glucose_min and h1_glucose_max. It raises the questions whether these outliers should be removed, which might potentially result in overfitting. A basic rule of thumb for the outliers in question is: It is a measurement error or data entry error, correct the error if possible. If I can’t fix it, remove
that observation. In this case, this is the outcome of a health report, so it is unlikely that this was a data entry error.

Since this dataset is about diabetes and these outliers might be the indication of extreme health conditions, I have decided to keep these outliers. Besides, we only remove the outliers if it is a potential data entry error, and it is not too likely for this type of report to have data error.

This boxplot also shows that all the variables are in different range, meaning that they should be standardized before fitting the model, which explains why the scaling pipeline to scale the data using StandardScaler is included in the model building in the later stage. 
