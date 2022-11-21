# Solution #

## Hypothesis 1: Growth rate ##
```sql
 -- Return growth rate by week
select date_trunc('week', e.occurred_at) as week,
       count(distinct e.user_id) AS weekly_active_users
from tutorial.yammer_events e
where e.event_type = 'engagement' and e.event_name = 'login'
group by week
order by week
```
![image](https://user-images.githubusercontent.com/77920592/203055634-922557d7-d7ce-4668-a9be-6de0edaf4062.png)
![image](https://user-images.githubusercontent.com/77920592/203089680-af58d0ed-6c07-4a43-accc-e8a627677419.png)

```sql
--- Return growth rate by month
select date_trunc('month', e.occurred_at) as month,
       count(distinct e.user_id) AS monthly_active_users
from tutorial.yammer_events e
where e.event_type = 'engagement' and e.event_name = 'login'
group by month
order by month
```
![image](https://user-images.githubusercontent.com/77920592/203055734-9674e8d2-6ab7-4611-854e-4ff4592a0ca8.png)
![image](https://user-images.githubusercontent.com/77920592/203089836-b5f2b81f-b440-487c-bb37-0d8a8e060815.png)

Weekly and monthly growth rates do not show any significant changes. Therefore, the drop in user engagement may be caused by the existing users facing different issues (slow loading speed, broken features, traffic anommalies, marketing events, etc.)

## Hypothesis 2: Engagement rate ##

### Engagement rate by location ###
```sql
--- Return engagement rate by continents
select date_trunc('week', occurred_at) as week,
sum(case when location in ('Indonesia', 'Singapore', 'Israel', 'Malaysia', 'Hong Kong', 'Philippines', 
                          'United Arab Emirates', 'Taiwan', 'Thailand', 'India', 'Iran', 'Japan', 'Iraq', 'Russia', 'Pakistan') then 1 else 0 end) as Asia,
sum(case when location in ('Brazil', 'Venezuela', 'Colombia', 'Argentina') then 1 else 0  end) as South_America,
sum(case when location in ('Nigeria', 'Egypt', 'South Africa') then 1 else 0  end) as Africa,
sum(case when location in ('Australia') then 1 else 0  end) as Oceania,
sum(case when location in ('United States', 'Canada', 'Mexico') then 1 else 0  end) as North_America,
sum(case when location in ('Sweden', 'Ireland', 'Portugal', 'Finland', 'France', 'Spain', 'Italy', 
                          'United Kingdom', 'Greece', 'Chile', 'Denmark', 'Switzerland', 'Norway', 'Austria', 'Poland') then 1 else 0  end) as Europe
from tutorial.yammer_events 
where event_type = 'engagement'
group by week
order by week
```
![image](https://user-images.githubusercontent.com/77920592/203087505-90027948-709d-40ea-9014-5b09ce05824f.png)
![image](https://user-images.githubusercontent.com/77920592/203087823-7240d480-0475-43fc-b948-89d308c9e0ab.png)

Apart from the users in Africa, the engagement rate dropped significantly across the rest of the continents since first week of August (2014-08-04 00:00:00) where North America witnesses the sharpest drop due to its largest user proportion. 

### Engagement rate by events ###
```sql
--- Return the engagement rate by events
select date_trunc('week', occurred_at) as week,
       count(case when e.event_name = 'home_page' then e.user_id else null end) as home_page,
       count(case when e.event_name = 'like_page' then e.user_id else null end) as like_page,
       count(case when e.event_name = 'login' then e.user_id else null end) as login,
       count(case when e.event_name = 'search_autocomplete' then e.user_id else null end) as search_autocomplete,
       count(case when e.event_name = 'search_run' then e.user_id else null end) as search_run,
       count(case when e.event_name = 'send_message' then e.user_id else null end) as send_message,
       count(case when e.event_name = 'view_inbox' then e.user_id else null end) as view_inbox 
from tutorial.yammer_events e
where e.event_type = 'engagement'
group by week
order by week
```
![image](https://user-images.githubusercontent.com/77920592/203062238-532f7a85-8e43-4bbd-8dff-216e4750e05d.png)
![image](https://user-images.githubusercontent.com/77920592/203090238-8eaf2358-a17c-43d6-97be-409daa1c3d37.png)

Engagement rate of all events except search_autocomplete and search_run started dropping since first week of August (2014-08-04 00:00:00). Periods around 2014-08-04 00:00:00 are worth a deeper examination to investigate if any significant changes have been implemented to have caused a drop in engagement rate. Therefore, we need to look into the various reasons that might be the underlying factors that might be the drivers.
- Devices >>> By comparing the engagement rate on different devices we can find out the potential UIUX issues, of the broken features or links in a specific device
- Email >>> By comparing the emails open and clickthrough rate we can have a gauge on the performance of the email marketing contents. 

### Engagement rate by devices ###
```sql
--- Return types of device
select distinct e.device AS devices
from tutorial.yammer_events
```

```sql
--- Return engagement rate by devices
select date_trunc('week', occurred_at) as week,
count(distinct user_id) as active_weekly_user,
sum(case when device in('iphone 5','samsung galaxy s4', 'nexus 5', 'iphone 5s', 'iphone 4s','nexus 7', 'nokia lumia 635','nexus 10','htc one','amazon fire phone','samsung galaxy note') then 1 else 0 end) as phone_users,
sum(case when device in('ipad air','ipad mini', 'kindle fire', 'samsung galaxy tablet') then 1 else 0 end) as tablet_users,
sum(case when device in('lenovo thinkpad','macbook pro','macbook air','dell inspiron desktop', 'dell inspiron notebok','asus chromebook','acer aspire notebook','hp                            pavilion desktop', 'acer aspire desktop','windows surface','mac mini') then 1 else 0 end) as computer_users
from tutorial.yammer_events
where event_type = 'engagement' and event_name = 'login'
group by week
order by week
```
![image](https://user-images.githubusercontent.com/77920592/203059211-efedefd2-960a-46c9-99fc-38d77d28e410.png)
![image](https://user-images.githubusercontent.com/77920592/203090690-f5bf8628-ee92-43d7-842b-83e4d2c562d7.png)

Engagement rate by devices for phone and tablet started dropping since first week of August (2014-08-04 00:00:00), especially for phone the drop is the most significant. Although tablet user count shows the same downward trend, the total number of Yammer users on tablet are not the significant. Computer devices remain the most popular device among Yammer users and it looks like the quality of the software is up to standard. It is also worth highlighting that the phone and tablet usage for the Yammer app has regressed back to May level, indicating that strategies to increase the engagement on phone and tablet were not successful if there was any, or else like previously mentioned, there might be some other issues hampering the usage such as the poor UIUX affecting the customer experiences.

### Engagement rate by email ###
```sql
--- Return engagement rate by email
select date_trunc('week', occurred_at) as week,
       count(case when e.action = 'sent_weekly_digest' then e.user_id else null end) as weekly_emails,
       count(case when e.action = 'sent_reengagement_email' then e.user_id else null end) as reengagement_emails,
       count(case when e.action = 'email_open' then e.user_id else null end) as email_opens,
       count(case when e.action = 'email_clickthrough' then e.user_id else null end) as email_clickthroughs
from tutorial.yammer_emails e
group by week
order by week
```
![image](https://user-images.githubusercontent.com/77920592/203061092-4e9ccd72-c875-4741-a1bc-41b48fa7ef35.png)
![image](https://user-images.githubusercontent.com/77920592/203091490-16d12551-209a-4e10-894b-c75799068e67.png)

The number of email sent increases over time. Users generally open the email by they started reducing the clickthrough since first week of August (2014-08-04 00:00:00). This might indicates that the contents fail to grab the attention of the users, possibly due to the lack of creative and innovative topics. However, the emails open rate is still desirable, meaning that the email sent frequency is appropriate, and the users are probably caught by the subject lines to open the email, but the dull contents have caused them to stop clicking through. 

There are several weeks where the email clickthrough rate is higher than usual, > 600. The marketing team might want to look into the content of those weeks, it could be the speficic types of contents catching the attention of the users, or they were drawn to some marketing campaigns like big promotion, christmas mega sales etc. 


# Recommendation #
Answer the following questions:

Do the answers to any of your original hypotheses lead you to further questions?
If so, what are they and how will you test them?
If they are questions that you can't answer using data alone, how would you go about answering them (hypothetically, assuming you actually worked at this company)?
What seems like the most likely cause of the engagement dip?
What, if anything, should the company do in response?

Users are already drowning in written content and 
