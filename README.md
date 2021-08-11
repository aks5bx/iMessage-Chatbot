# Analyzing My Group Chat Text Messages


## Overview 

The "Group Chat" is a cultural advent that took the world by storm in lockstep with the popularization of texting. Throw your close friends into a single message group and you've got the Group Chat. The Group Chat in this project involves myself and eight of my friends shooting the breeze on a daily basis. The group is active and includes messages from all participants. I decided to analyze how this group operates by diving into the text data. What follows is an overview of what I did and the findings my work yielded. 

## Data Sourcing 

I sourced data by querying the chat.db database, which is a hidden but ultimately available database built into any Mac OS. I leaned on a public GitHub repository (https://stmorse.github.io/journal/iMessage.html) to access the database. From there, I tried various queries to extract the information I needed. I ultimately discovered the following query: 

~~~~sql
SELECT
    datetime (message.date / 1000000000 + strftime ("%s", "2001-01-01"), "unixepoch", "localtime") AS message_date,
    message.text,
    message.is_from_me,handle_id, 
    chat.chat_identifier
FROM
    chat
    JOIN chat_message_join ON chat. "ROWID" = chat_message_join.chat_id
    JOIN message ON chat_message_join.message_id = message. "ROWID"
WHERE chat.chat_identifier = 'chat602411273960483331'  ORDER BY
    message_date ASC;
~~~~

This query extracts and formates the datetime of the message, the text contents of the message, whether I sent the message, who sent the message, and finally the message ID. 

I had to find the chat_identifier ID of my group chat. In order to do this I queried all of the Messsage table in chat.db and manually grabbed my chat_identifier. This is not a perfect system, but a little bit of digging should allow anyone to get the chat identifier that they need. 

I exported this table to a csv as outlined in the aforementioned GitHub repository. 

## Data Preview 

Because of the sensitive nature of the text messages, I am not attaching the dataset for this project. However, below is a preview of the dataframe that I used after I read it into a Pandas Dataframe. 

Index | Datetime | Text | I_Sent | UserID | chatID |
| --- | --- | --- | --- |--- |--- |
1 | 2021-07-16 16:57:22 | 'Sample text message' | 0 | 5 | chat602411273960483331 |

## Data Processing

### Data Cleaning/Labelings

In order to make the data usable, I conducting the following simple data processing steps 
- Mapped users ids to user names (anonymized for this repo)
- Converted data type for datetime
- Created a column that calculates how many seconds after the previous text the text came in
- Created a second grouped dataframe, grouping number of total characters, total texts, and characters per text send by each user 

Here is the grouped dataframe 

User | Characters | Texts | Characters/Text |
| --- | --- | --- |--- |
Friend1	| 17390.0	|293	|59.351536 |
Friend4	| 31618.0	|531	|59.544256 |
Friend2|	31571.0	|530	|59.567925 |
Friend6|	8546.0	|136	|62.838235 | 
Friend3|	17792.0	|258	|68.961240 |
Friend7|	11009.0	|157	|70.121019 |
Me	|16346.0	|231	|70.761905 | 
Friend5|	4398.0	|62	|70.935484 |
Friend8	|14028.0	|187	|75.016043 |

