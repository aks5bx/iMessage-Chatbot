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

