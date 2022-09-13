# Supervised Model Training and Evaluation

The experiment aims to answer the following questions:

• Feature Selection - Does high correlation among features affect the performance of ensembles of tree-based models?

• Class imbalance - Does class imbalance affect the performance of models?

• Hyperparamater Tuning - Which hyperparameter tuning yields better performance? GridSearchCV or RandomizedSearchCV?

• Model Performance – Model comparisons and the findings of different models

## **Resampling imbalance class**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189850810-1af8dad0-cb59-450d-9d3d-abbdd5fcf26c.png" width = 700">
</p>
                                                                                                                               
From the pie chart, the dataset is observed to have the class imbalance issue where there is more 0 than 1. The patients who are contracted with diabetes_mellitus is about 44.8% less than those who are not. This might result in bias to the majority class. Resampling is performed to balance the classes.

### **Class imbalance - Does class imbalance affect the performance of models?**
                                                                                                                               
DTC is used as the model to compare the performance of model built on the imbalance and balance class. Feature selection is conducted before resampling as most variable selection methods assume that the samples are independent and resampling with methods such as SMOTE violates the independence assumption (Blagus & Lusa, 2013).

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189852211-55d058b4-9ff5-4e98-b548-53bd5bdce5b9.png" width = 300">
</p>

Before resampling: Support shows an imbalance dataset that may indicate structural weaknesses. From the recall (positive cases being caught), it is shown that the percentage for majority class, 0 is way higher the minority class, proving that the model is bias towards the majority class. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189852015-91144025-9898-489d-836e-7c00c91020c2.png" width = 300">
</p>

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189852450-e3eefb1f-65b7-4d13-98ce-3ff78c1219ac.png" width = 300">
</p>
                                                                                                                               
Plain upsampling/downsampling: Downsampling outperforms upsampling in terms of recall in minority class despite of the slight decrease of overall accuracy. Accuracy is not a good measure of performance on unbalanced classes. The reason of the reduced accuracy could be because it is now a more realistic representation of how the model will generalize instead of predicting 0 every time.                                                                                                                             

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189852564-c055c94e-2c3c-48c8-b4e5-3e32d05976ed.png" width = 300">
</p>
                                                                                                                               
SMOTE upsampling: SMOTE yields similar performance as plain downsampling but with a higher precision on the majority class. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189852661-9dce43ab-75e9-4942-b959-2a8807dfe482.png" width = 300">
</p>
                                                                                                                               
Random Under Sampler downsampling: Random Under Sampler yields the best performance with the greatest improvement in minority recall and overall accuracy.   

## **Feature Selection**

### **Correlation**

#### **Heatmap to examine correlation**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189853225-13c6653c-0b2e-43f8-9560-8c587b825bf7.png" width = 800">
</p>
                                                                                                                               
The heatmap shows that h1_glucose_max has a strongest correlation with diabetes_mellitus, followed by bmi, d1_bun_max, age, d1_glucose_min, d1_potassium_max and creatinine_apache, age, d1_potassium_max. To confirm the correlation, the Spearman correlation is computed. Spearman correlation test is used because we can’t identify whether our data is linear or monotonic and the test works well with monotonic relationship.
                                                                                                                               
#### **Spearman rank test**
                                                                                                                               
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189853434-ebb67119-d287-426a-9a47-18f8b77bb1ed.png" width = 250">
</p>

The spearman rank test shows confirms that h1_glucose_max has the strongest correlation with diabetes_mellitus, also the correlation with the rest of the 7 features. It is worth highlighting that d1_sodium_min demonstrates a negative coefficient, indicating a negative monotonic relationship with diabetes_mellitus.

#### **SelectKBest**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189853715-2e9e22e3-6e4e-4581-950c-0702c276a47c.png" width = 250">
</p>
                                                                                                                               
Apart from the above -mentioned correlation test, feature selection using SelectKBest is performed to identify the most important features. Like the heatmap correlation, h1_glucose_max is identified to be the most important feature. 
                                                                                                                               
### **Feature Selection - Does high correlation among features affect the performance of ensembles of treebased models?**

The result of DTC base model is shown as follows:
                                                                                                                               
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189856323-56efd4df-183e-4687-a509-3e07c5e78299.png" width = 700">
</p>

The result of DTC tuned model is shown as follows:
                                                                                                                               
<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189856448-794a636f-cd05-4d77-b792-364f6be90f58.png" width = 700">
</p>
                                                                                                                               
Study shows that ensembles of tree-based models such as XGBoost are not easily affected by the highly correlated features as it will pick up exactly 50%|50% each feature (Laurae, 2016). Hence, we run the same experiment with and without retaining all the highly correlated features to compare the performance. 

The performance of base and tuned model are both improved with feature selection in terms of the precision, recall and f1-score. The combination of feature selection and hyperparameter tuning yields the best result. 
                                                                                                                               
## **Classification models**
                                                                                                                               
For supervised model training, Decision Tree Classifier (DTC), Extra Trees Classifier (EDTC), KNeighbors Classifier (KNN), Random Forest Classifier (RFC), Gaussian Naïve Bayes (GNB) and Gradient Boosting Classifier (GBC) are selected. The top 5 most importance features including 'h1_glucose_max', 'd1_glucose_min', 'bmi', 'creatinine_apache', 'd1_bun_max' are selected to be X, and diabetes_mellitus to be the target variable, Y.                                                                                                                                

### **Train-test-split**                                                                                                                              

The data is split into 70% training data and 30% testing data. The parameter is set as follows:
                                                                                                                               
• Shuffle is set to True so data will be randomly splitted. 
                                                                                                                               
• Stratify is set so that the proportion of values in the sample produced in our test group will be the same as the proportion of values provided to parameter stratify. This results especially useful when working around classification problems, since it is possible to end with a non-representative distribution of our target classes in the test group if this parameter is not provided with an array-like object.
                                                                                                                               
• Random state is specified so that each iteration of the train_test_split will give the same groups, since the seed used to proceed with the randomness around the split would be same and we will not obtain different result each time the experiment is run. 

### **Scaling**       
                                                                                                                        
A scaling pipeline consisting of StandardScaler, and Principal Component Analysis are built and fit the X_train and X_test. The purpose is as follows:
                                                                                                                               
•	StandardScaler: standardize the variables to the same scale
                                                                                                                               
•	Principal Component Analysis: dimensionality reduction to reduce the number of features whilst keeping most of the original information
                                                                                                                               
The pipeline object is fitted first using our train group and then transform our test group using that same object. The purpose is for the StandardScaler object to register and proceed with the Mean and Standard Deviation of the train set and transform the test group using it. Otherwise, it will be two different transformations, taking two different Means and two different Standard Deviations treating as different data that’s supposed to be the same.
                                                                                                                              
### **Cross validation – K-fold**       

By just doing train-test split, a chunk of data is set aside, so I won't be able to use it to train my algorithm. And since the data is sampled at random, it has a chance of being skewed in some way, not representing the whole dataset properly. K-fold cross validation addresses these problems. Data is split into several (10 for example, if k = 10) subsets, called folds, and the model is trained and evaluated 10 times, setting aside each one of the folds in turn, and training the model on the remaining 9 folds. The issue with k-fold cross validation is that it is time-consuming if the dataset is huge, as proven in our experiments.
In our experiment, we adopt cv = 5, so the data will be split into train and test folds 5 times. The model will be fitted on train and scored on test.

### **Hyperparamater Tuning**
                                                                                                                               
GridSearchCV can be computationally expensive, especially if to search over a large hyperparameter space and deal with multiple hyperparameters. A solution to this is to use RandomizedSearchCV, in which not all hyperparameter values are tried out. Instead, a fixed number of hyperparameter settings is sampled from specified probability distributions. Two experiments using DT as the algorithms are performed to compare the performance of GridSearchCV and RandomizedSearchCV. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189859309-8629c895-ce25-4308-aae3-0280c50b6594.png" width = 700">
</p>
                                                                                                                               
GridSearchCV and RandomizedSearchCV present same result, but RandomizedSearchCV takes a shorter time. 4.49s compared to the 29.07s of RandomizedSearchCV as not all the values are tested and values tested are selected at random. For example, if there are 200 values in the distribution and if we input n_iter=50 then random search will randomly sample 20 values to test. Both are very effective ways of tuning the parameters that increase the model generalizability.

### **Model Performance – Model comparisons and the findings of different models**

We have come to understand that resampling using Random Under Sampler downsampling, feature selection and hyper-parameter tuning using RandomizedSearchCV can improve the model performance to a certain extent. Now we will build model based on these criteria and compare the results of base and tuned models.  

#### **Logistic Regression (LR)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860093-b5963228-dcdf-4d7c-99b3-4f26fae7680b.png" width = 700">
</p>
                                                                                                                               
#### **Decision Tree (DT)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860203-f31f9830-3af8-4f66-b3c7-47c57f29fdb7.png" width = 700">
</p>

#### **Bagged Decision Tree (BDTC)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860673-a3d34aeb-5cfe-494c-b071-91cbc23782c1.png" width = 700">
</p>
                                                                                                                               
#### **Extra Trees Classifier (EDTC)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860760-58b3fb3c-97fd-4db2-b147-afe3870a75e6.png" width = 700">
</p>

#### **Random Forest (RF)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860834-001868d5-36ca-49db-8be9-3b91a97cc702.png" width = 700">
</p>

#### **KNeighbors Classifier (KNN)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860903-c23c38f7-a57f-4965-912c-ffa38e40f760.png" width = 700">
</p>
                                                                                                                               
#### **Gaussian Naïve Bayes (GNB)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189860997-ce03754e-ca74-4f2f-badd-d521816c9aef.png" width = 700">
</p>

#### **Gradient Boosting Classifier (GBC)**

<p align="center">
  <img src="https://user-images.githubusercontent.com/77920592/189861091-a670ad85-3d40-4c77-8a36-fe03626de315.png" width = 700">
</p>

### **Model Comparison**

#### **Training time**
• GNB takes the shortest training time, and it is followed by LR, KNN and DT. GNB is claimed to be much faster compared to more sophisticated method.

• GBC takes the longest training time but still does not demonstrate a huge improvement in performance. 

• In general, tree-models take a longer training time compared to other simple classifiers such as KNN. This means it is computationally expensive, especially when tuning model hyperparameter via k-fold cross-validation. 

#### **Performance of supervised models by analysis of classification report**
• GNB and EDTC yield the best result with an accuracy of 0.63, and a recall of 0.69 and 0.52, and 0.66 and 0.57 respectively. Comparing the training time, GNB is way faster than EDTC. The decoupling of the class conditional feature distributions of GNB allows each distribution to be independently estimated as a one-dimensional distribution, alleviating problems coming from dimensionality.

• EDTC outperforms the rest of the tree modes, yielding a similar accuracy and recall to the RF. However, it compromises on the longer training time of around 1 minute. 

• GBC takes the longer time to train but does not improve the performance significantly compared to other models.
