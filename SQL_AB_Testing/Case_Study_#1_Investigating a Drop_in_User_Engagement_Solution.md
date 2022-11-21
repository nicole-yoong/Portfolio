# Investigating a Drop in User Engagement #

Yammer was founded 2008 as a freemium enterprise social networking service used for private communication within organizations. It was acquired by Microsoft for $1.2 billion in 2012 and is now available in all Office 365 products.

This is a case study of Yammer’s drop in user engagement from May to August of 2014. Due to privacy reasons, the data used is not real and did not reflected real user engagement of the Yammer app at the time. 

## The problem ##
You show up to work Tuesday morning, September 2, 2014. The head of the Product team walks over to your desk and asks you what you think about the latest activity on the user engagement dashboards. You fire them up, and something immediately jumps out:

View Mode Analysis
The above chart shows the number of engaged users each week. Yammer defines engagement as having made some type of server call by interacting with the product (shown in the data as events of type "engagement"). Any point in this chart can be interpreted as "the number of users who logged at least one engagement event during the week starting on that date."

You are responsible for determining what caused the dip at the end of the chart shown above and, if appropriate, recommending solutions for the problem.

## Getting oriented ##
Before you even touch the data, come up with a list of possible causes for the dip in retention shown in the chart above. Make a list and determine the order in which you will check them. Make sure to note how you will test each hypothesis. Think carefully about the criteria you use to order them and write down the criteria as well.

Also, make sure you understand what the above chart shows and does not show.

If you want to check your list of possible causes against ours, read the first part of the answer key.

## Digging in ##
Once you have an ordered list of possible problems, it's time to investigate.

For this problem, you will need to use four tables. The tables names and column definitions are listed below—click a table name to view information about that table. Note: this data is fake and was generated for the purpose of this case study. It is similar in structure to Yammer's actual data, but for privacy and security reasons it is not real.

### Table 1: Users ### 

This table includes one row per user, with descriptive information about that user's account.
This table name in Mode is tutorial.yammer_users

| Field | Description |
| ------------- | ------------- |
| user_id: | A unique ID per user. Can be joined to user_id in either of the other tables. |
| created_at:	|The time the user was created (first signed up) |
| state:	|The state of the user (active or pending) |
| activated_at:	|The time the user was activated, if they are active |
| company_id:	|The ID of the user's company |
| language:	|The chosen language of the user |

### Table 2: Events ### 

This table includes one row per event, where an event is an action that a user has taken on Yammer. These events include login events, messaging events, search events, events logged as users progress through a signup funnel, events around received emails.
This table name in Mode is tutorial.yammer_events

| Field | Description |
| ------------- | ------------- |
| user_id:	| The ID of the user logging the event. Can be joined to user\_id in either of the other tables. |
| occurred_at: | The time the event occurred. |
| event_type:	 | The general event type. There are two values in this dataset: "signup_flow", which refers to anything occuring during the process of a user's authentication, and "engagement", which refers to general product usage after the user has signed up for the first time. |
| event_name:	 | The specific action the user took. Possible values include: create_user: User is added to Yammer's database during signup process enter_email: User begins the signup process by entering her email address enter_info: User enters her name and personal information during signup process complete_signup: User completes the entire signup/authentication process home_page: User loads the home page like_message: User likes another user's message login: User logs into Yammer search_autocomplete: User selects a search result from the autocomplete list search_run: User runs a search query and is taken to the search results page search_click_result_X: User clicks search result X on the results page, where X is a number from 1 through 10. send_message: User posts a message view_inbox: User views messages in her inbox |
| location:	 | The country from which the event was logged (collected through IP address). |
| device:	 | The type of device used to log the event. |

### Table 3: Email Events ### 

This table contains events specific to the sending of emails. It is similar in structure to the events table above.
This table name in Mode is tutorial.yammer_emails

| Field | Description |
| ------------- | ------------- |
| user_id:	| The ID of the user to whom the event relates. Can be joined to user_id in either of the other tables. |
| occurred_at:	| The time the event occurred. |
| action: | The name of the event that occurred. "sent_weekly_digest" means that the user was delivered a digest email showing relevant conversations from the previous day. "email_open" means that the user opened the email. "email_clickthrough" means that the user clicked a link in the email. |

### Table 4: Rollup Periods ### 

The final table is a lookup table that is used to create rolling time periods. Though you could use the INTERVAL() function, creating rolling time periods is often easiest with a table like this. You won't necessarily need to use this table in queries that you write, but the column descriptions are provided here so that you can understand the query that creates the chart shown above.
This table name in Mode is benn.dimension_rollup_periods

| Field | Description |
| ------------- | ------------- |
| period_id: |	This identifies the type of rollup period. The above dashboard uses period 1007, which is rolling 7-day periods. |
| time_id: | This is the identifier for any given data point — it's what you would put on a chart axis. If time_id is 2014-08-01, that means that is represents the  rolling 7-day period leading up to 2014-08-01. |
| pst_start: | The start time of the period in PST. For 2014-08-01, you'll notice that this is 2014-07-25 — one week prior. Use this to join events to the table. |
| pst_end: | The start time of the period in PST. For 2014-08-01, the end time is 2014-08-01. You can see how this is used in conjunction with pst_start to join events to this table in the query that produces the above chart. |
| utc_start: |	The same as pst_start, but in UTC time. |
| pst_start: | The same as pst_end, but in UTC time. |

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

## Hypothesis 2: Engagement rate by locations ##

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

## Hypothesis 3: Engagement rate by events ##

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

## Hypothesis 4: Engagement rate by devices ##
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

Engagement rate by devices for phone and tablet started dropping since first week of August (2014-08-04 00:00:00), especially for phone the drop is the most significant. Although tablet user count shows the same downward trend, the total number of Yammer users on tablet are not the significant. Computer devices remain the most popular device among Yammer users and it looks like the quality of the software is up to standard. It is also worth highlighting that the phone and tablet usage for the Yammer app has regressed back to May level, indicating that strategies to increase the engagement on phone and tablet were not successful if there was any, or else like previously mentioned, there might be some other issues hampering the usage.

## Hypothesis 5: Engagement rate by emails ##

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

The number of email sent increases over time. Users generally open the email by they started reducing the clickthrough since first week of August (2014-08-04 00:00:00). This might indicates that the contents fail to grab the attention of the users, possibly due to the lack of creative and innovative topics. However, the emails open rate is still desirable, which means that the emails remain to be well-received by users and the sent frequency is appropriate, and the users are probably caught by the subject lines to open the email, but the dull contents have caused them to stop clicking through. 

We can also see that the number of reengagement emails have increased slightly but it does not improve the clickthrough rate, indicating that the content quality is the key to increase the clickthrough rate but not the quantity of the email sent. The increased number of reengagament emails could potentially annoy the users and hurt the marketing efforts if the contents are not improved.

In the meantime, there are several weeks where the email clickthrough rate is higher than usual, > 600. The marketing team might want to look into the content of those weeks, it could be the speficic types of contents catching the attention of the users, or they were drawn to some marketing campaigns like big promotion, christmas mega sales etc. 


# Recommendation #

**What seems like the most likely cause of the engagement dip?**

The most likely cause of the engagement dip are:
- Use of phone device 
- The email clickthrough rates

Several possible causes can contribute to these issues. First, the email contents are dull and do not catch the attention of the users to read through the them. Users are already drowning in written content and they usually need appealling contents to keep their interests. Second, there might be some weaknesses in the phone UIUX which deteriorate the user navigation experiences. It can be poor interface design, or even broken features or links to affect the customer experiences. Other possibilities could be the distorted email format on phone, such as the font size, images resoluton etc. 

**What, if anything, should the company do in response?**

Company should be informed about the problems so they could figure out the changes that have been made to make sure something isn't broken or poorly implemented.
It is not completely clear that what the problem is or how it should be solved, thus I suggest several checks that can be implemented:
- perform beta testing on the phone and tablet views to detect poor structure, and functionality
- perform page funnel analysis mapping the flow of users to check which specific steps result in funnel drop-offs
- perform A/B testing for weekly digest email contents
