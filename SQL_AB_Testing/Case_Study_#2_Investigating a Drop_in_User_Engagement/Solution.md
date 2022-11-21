## Solution ##

### Hypothesis 1: Growth rate ###
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

```sql
 -- Return growth rate by month
select date_trunc('month', e.occurred_at) as month,
       count(distinct e.user_id) AS monthly_active_users
from tutorial.yammer_events e
where e.event_type = 'engagement' and e.event_name = 'login'
group by month
order by month
```
![image](https://user-images.githubusercontent.com/77920592/203055734-9674e8d2-6ab7-4611-854e-4ff4592a0ca8.png)

Weekly and monthly growth rates do not show any significant changes. Therefore, the drop in user engagement may be caused by the existing users facing different issues (slow loading speed, broken features, traffic anommalies, marketing events, etc.)

### Hypothesis 2: Engagement rate ###

**Engagement rate by events**
```sql
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

Engagement rate of all events started dropping since first week of August (2014-08-04 00:00:00).

**Engagement rate by devices**
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


Engagement rate by devices for phone and tablet started dropping since first week of August (2014-08-04 00:00:00). However, the engagement rate was quite consistent on the computer, showing that there might be issues on the UIUX of phone/tablet thus affecting the customer experiences. 

**Engagement rate by email**
```sql
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

The number of email sent increases over time. Users generally open the email by they started reducing the clickthrough since first week of August (2014-08-04 00:00:00). This might indicates that the contents fail to grab the attention of the users, possibly due to the lack of creative and innovative topics. However, the emails open rate is still desirable, meaning that the email sent frequency is appropriate, and the users are probably caught by the subject lines to open the email, but the dull contents have caused them to stop clicking through. 

There are several weeks where the email clickthrough rate is higher than usual, > 600. The marketing team might want to look into the content of those weeks, it could be the speficic types of contents catching the attention of the users, or they were drawn to some marketing campaigns like big promotion, christmas mega sales etc. 


## Recommendation ##
Answer the following questions:

Do the answers to any of your original hypotheses lead you to further questions?
If so, what are they and how will you test them?
If they are questions that you can't answer using data alone, how would you go about answering them (hypothetically, assuming you actually worked at this company)?
What seems like the most likely cause of the engagement dip?
What, if anything, should the company do in response?

Users are already drowning in written content and 
