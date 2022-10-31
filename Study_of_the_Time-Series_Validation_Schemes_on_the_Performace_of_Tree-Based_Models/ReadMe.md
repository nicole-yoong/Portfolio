# Study of the Time-series Validation Schemes on The Performance of Tree-based Models #

## Introduction ##
With respect to time-series stock price prediction, cross-validation (CV) is an essential statistical method to evaluate the performance of machine learning models. 

Traditional validation schemes such as k-folds CV usually pose a limitation of the temporal dependencies issue as data selected in each fold is completely random. 

Reviewing the existing studies on stock price prediction reveals that there is only a limited number of papers examining the time-series CV scheme. Therefore, it provides an incentive to investigate the various validation schemes and the deterministic factors of their performances.

## Aims/Objectives ##
To investigate the performance of validation schemes on the time-series  S&P 500 stock price prediction.

To examine the performance of the tree-based models in  S&P 500 stock price prediction. 

To study if input feature affects the performance of the proposed validation schemes and models

To explore the predictive power of VIX on S\&P 500 stock price prediction

## Methods/Design ##
Model selection procedures are proposed based on the:

Validation schemes: i) Single Train-Validation, ii) K-Fold CV, iii) Rolling Window CV, and iv) Expanding Window CV

Tree-based models: i) Decision Tree Classifier (DTC), ii) Random Forest Classifier (RFC), iii) Extra Trees Classifier (ETC), iv) AdaBoost Classifier (ADA), v) Bagging Classifier (BC)

Input Features: ATR, BB, RSI, %K, %R, ADX, SMA, EMA, and MACD, Daily percentage change of VIX

## Results/Conclusions ##
Time-series validation – RW_CV and EW_CV are less computational expensive than traditional STV and KF_CV.

RW_CV is efficient in handling class imbalance issue, which commonly plagues the instable models like DTC, however, it yields negative Sharpe ratio in most models.  

EW_CV to be more suitable in the application of stock price prediction as it achieves a satisfying Sharpe ratio in most models while being less computationally expensive. While STV also yields a positive Sharpe ratio in most models, it is less recommended due to the extremely high computational cost. 

ADA and BC are less sensitive to class imbalance, while RFC is more robust in achieving a positive Sharpe ratio in all validation schemes. 

Input features to be one of the deterministic factors in affecting the validation schemes and model performance. 

VIX does not contain predictive power on the time-series S&P 500 stock price prediction

