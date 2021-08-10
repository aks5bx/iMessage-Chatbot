#%%
########################
### IMPORT LIBRARIES ###
########################

## Importing libraries
import pandas as pd 
pd.set_option('display.max_rows', None)
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
import networkx as nx
from math import isnan

## Read in Data
chatData = pd.read_csv('chatExport.csv', header = None)
chatData.columns = ['Datetime', 'Text', 'I_Sent', 'UserID', 'ChatID']
chatData.head(50)
# %%
#####################
### DATA CLEANING ###
#####################
2
## Mapping User ID to User Name
di = {0: "Adi", 1: "Shubs", 2: "Morgan", 3: "Steve", 4: "Jesse", 5: "Andrew", 6: "Geoff", 7: "Connor", 8: "Will"}
chatData['User'] = chatData["UserID"].map(di)

## Changing Datetime data type
chatData['Datetime'] = pd.to_datetime(chatData['Datetime'])

## Number of Messages/Reactions by User 
chatData['User'].value_counts().plot(kind='bar')

## Number of characters per text 
chatData['Characters'] = chatData['Text'].str.len()
chatDataGrouped = chatData.groupby('User').agg({'Characters':'sum', 
                         'UserID':'count'}).reset_index()
chatDataGrouped.columns =['User', 'Characters', 'Texts']
chatDataGrouped['Characters/Text'] = chatDataGrouped['Characters'] / chatDataGrouped['Texts']
chatDataGrouped = chatDataGrouped.sort_values(by = 'Characters/Text')


#%%
#################################
### CONVERSATION SEGMENTATION ###
#################################

## Get difference between current text and previous text 
chatData['TimeAfterPrevious'] = chatData.Datetime - chatData.Datetime.shift()
chatData['TimeAfterPrevious'] = chatData['TimeAfterPrevious'].dt.seconds

## Define a conversation ending if nobody replies within 15 minutes 
chatData['NewConversation'] = (chatData['TimeAfterPrevious'] > 900)
chatData['ConversationID'] = 0

## Give each conversation a unique conversation ID
convoID = 1
for idx, row in enumerate(chatData.itertuples(), 1):
    idx = idx - 1
    if row.NewConversation:
        convoID += 1
        chatData.loc[idx,'ConversationID'] = convoID
    else:
        chatData.loc[idx,'ConversationID'] = convoID

## For each conversation, identify who participated   
conversationDict = {}
for convoID in range(1, int(max(chatData.ConversationID)) + 1):
    subset = chatData[chatData.ConversationID == convoID]
    participants = list(set(subset.User))
    conversationDict[convoID] = participants

## Users list
usersList = list({x for x in set(chatData.User) if x==x})

#%%
## Initialize Graph
G = nx.complete_graph(len(usersList))
for user in usersList:
    G.add_node(user)

mapping = dict(zip(chatData.UserID, chatData.User))
mapping = {k: mapping[k] for k in mapping if not isnan(k)}
G = nx.relabel_nodes(G, mapping)
nx.set_edge_attributes(G, values = 1, name = 'weight')

## For each person 
numberOfConversationsDict = {}
## For each person, 
for user in usersList:
    userNumConvos = 0
    for key, value in conversationDict.items():
        if user in value:
            userNumConvos += 1
    numberOfConversationsDict[user] = userNumConvos


## For each person, 
for user in usersList:
    userConvoList = []
    userNumConvos = 0
    for key, value in conversationDict.items():
        if user in value:
            userNumConvos += 1
            userConvoList += value
    
    userConvoListUpdated = list(filter((user).__ne__, userConvoList))

    for user2 in list(set(userConvoListUpdated)): 
        ## If there has not been an edge weight set yet 
        if G[user][user2]['weight']  == 1:
            edgeWeight = userConvoListUpdated.count(user2) / numberOfConversationsDict[user]
            ## Then update the edge weight
            G[user][user2]['weight'] = edgeWeight
        else:
            edgeWeight = userConvoListUpdated.count(user2) / numberOfConversationsDict[user]
            newEdgeWeight = (edgeWeight + G[user][user2]['weight']) / 2

sortedEdges = sorted(G.edges(data=True), key=lambda t: t[2].get('weight', 1), reverse=True)


    



# %%
#######################
### CHATBOT ATTEMPT ###
#######################

## Not enough training data, conversations weren't direct enough

chatDataList = chatData['Text'].tolist()
chatDataList = [str(i) for i in chatDataList]

bot = ChatBot(
    'Buddy',  
    logic_adapters=[
        'chatterbot.logic.BestMatch',
        'chatterbot.logic.TimeLogicAdapter'],
)

trainer = ListTrainer(bot)
trainer.train(chatDataList)

response = bot.get_response('I have a complaint.')

# %%
