![image](https://user-images.githubusercontent.com/77920592/192091005-aaadcd85-aa97-4ffb-85f2-a7cb69612b7e.png)

# Introduction #
 
Subscription based businesses are super popular and Danny realised that there was a large gap in the market – he wanted to create a new streaming service that only had food related content – something like Netflix but with only cooking shows!
Danny finds a few smart friends to launch his new startup Foodie-Fi in 2020 and started selling monthly and annual subscriptions, giving their customers unlimited on-demand access to exclusive food videos from around the world!
Danny created Foodie-Fi with a data driven mindset and wanted to ensure all future investment decisions and new features were decided using data. This case study focuses on using subscription style digital data to answer important business questions.

# Available Data #

Danny has shared the data design for Foodie-Fi and also short descriptions on each of the database tables – our case study focuses on only 2 tables but there will be a challenge to create a new table for the Foodie-Fi team.
All datasets exist within the foodie_fi database schema – be sure to include this reference within your SQL scripts as you start exploring the data and answering the case study questions.
You can inspect the entity relationship diagram and example data below.

![image](https://user-images.githubusercontent.com/77920592/192091076-4296ae54-7e63-4938-9f77-cbddedaf8a32.png)

All datasets exist within the case1 database schema – be sure to include this reference within your SQL scripts as you start exploring the data and answering the case study questions.

** Table 1: plans **
Customers can choose which plans to join Foodie-Fi when they first sign up.
Basic plan customers have limited access and can only stream their videos and is only available monthly at $9.90
Pro plan customers have no watch time limits and are able to download videos for offline viewing. Pro plans start at $19.90 a month or $199 for an annual subscription.
Customers can sign up to an initial 7 day free trial will automatically continue with the pro monthly subscription plan unless they cancel, downgrade to basic or upgrade to an annual pro plan at any point during the trial.
When customers cancel their Foodie-Fi service – they will have a churn plan record with a null price but their plan will continue until the end of the billing period.

![image](https://user-images.githubusercontent.com/77920592/192091081-c32b48c4-a6bf-40be-9e61-e1824f719e3d.png)

** Table 2: subscriptions **
Customer subscriptions show the exact date where their specific plan_id starts.
If customers downgrade from a pro plan or cancel their subscription – the higher plan will remain in place until the period is over – the start_date in the subscriptions table will reflect the date that the actual plan changes.
When customers upgrade their account from a basic plan to a pro or annual pro plan – the higher plan will take effect straightaway.
When customers churn – they will keep their access until the end of their current billing period but the start_date will be technically the day they decided to cancel their service.

![image](https://user-images.githubusercontent.com/77920592/192091102-0255bb8c-1f7f-41e6-9047-be0c4c6d3e75.png)

# SQL Schema #

