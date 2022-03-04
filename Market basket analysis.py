# Emergent

import pandas as pd
import numpy as np
# for market basket analysis
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
# for visulizations
import matplotlib.pyplot as plt
from collections import Counter
import random
import squarify
import seaborn as sns


print('Introduction: ')
print('The code is designed to do market basket analysis.')
print('There are two main function of this program: ')
print(' ')
print('Firstly, it could return a list of product combination and the support rate of each combination.')
print('The support rate is calculated by the frequence of the specific combination be bought and the frequence of all different combinations be bought.')
print('Higher the support rate, more likely these items will be bought together.')
print('The result will be recorded into a file called: market basket analysis result.csv')
print('The path of this file could be customized. ')
print(' ')
print('Another application of this program is to make relevant product recommendation.')
print('Later, there will be instruction about product recommendation.')

# transfer original dataset
# 'excel_path' needs to be changed based on the path of document
# excel_path = 'C:/Users/HP/Desktop/emergent/live-light-Inventory.xlsx'
print('In the following question, you are required to enter the full path your document.')
print('Please be cautious that current program only support the Inventory.xlsx document.')
print('An example of form of path: C:/Users/HP/Desktop/emergent/live-light-Inventory.xlsx')
excel_path = input('Please enter your path here: ')
data_org = pd.read_excel(excel_path, sheet_name='Order Pending')
data_org = data_org.iloc[:, 1:]
columns = []
for i in data_org.iloc[4]:
    columns.append(i)
data_org = data_org.iloc[6:]
data_org.columns = columns

data_order_org = pd.DataFrame({'customer': data_org.CUSTOMER, 'itemid': data_org['ITEM ID'], 'itemname': data_org['ITEM NAME']})

customer_list_dup = list(data_order_org.customer)
# delete duplicate customer name
seen = set()
customer_list = []
for item in customer_list_dup:
    if item not in seen:
        seen.add(item)
        customer_list.append(item)

# convert dataset to the type we need
buy_list = {}
for name in customer_list:
    il = data_order_org[data_order_org.customer == name]
    buy_list[name] = il.itemname.tolist()
# convert dictionary to dataframe
buy_list_frame = pd.DataFrame(buy_list.items())
buy_list_frame.columns = ['name', 'itemname']
buy_list_frame.shape
buy_list_frame.describe()

pure_list = []
for namelist in buy_list_frame.itemname:
    for i in namelist:
        pure_list.append(i)

# create unique list of items
pure_list_un = list(set(pure_list))

# looking at the frequency of most popular items
count = Counter(pure_list)
count = dict(count)
sorted_count = dict(sorted(count.items(), key=lambda x: x[1], reverse=True))
keys = sorted_count.keys()
values = sorted_count.values()

# keep top 10 item
keys_10 = list(keys)
keys_10 = keys_10[:10]
print(' ')
print('Top 10 best selling item/itemse:')
for key in keys_10:
    print(key)
# values_10 = list(values)
# values_10 = values_10[:10]
# plt.bar(keys_10, values_10)
# plt.title('the selling frequency of top 10 most popular products')
# plt.show()

data_pro = buy_list_frame.itemname

# transaction encoder
from mlxtend.preprocessing import TransactionEncoder
te = TransactionEncoder()
data_tran = te.fit_transform(data_pro)
data_tran_frame = pd.DataFrame(data_tran, columns=te.columns_)

# data_tran_frame.shape

# return the items and itemsets with at least 5% support
frequent_itemsets = apriori(data_tran_frame, min_support=0.05, use_colnames=True)
frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))

# compute all association rules for frequent_itemsets
rules = association_rules(frequent_itemsets)
rules = rules.sort_values(by='support')

frequent_itemsets
itemlists = []
for i in frequent_itemsets.itemsets:
    itemlist = list(i)
    itemlists.append(itemlist)
frequent_itemsets['itemlists'] = itemlists

# get the item sets with length>=2 and support more than 10%
# length equals to expected length of item sets(it can be changed)
length = 2
support_rate = 0.01
fa2 = frequent_itemsets[(frequent_itemsets['length'] >= length) & (frequent_itemsets['support'] >= support_rate)]
freq_abov_2 = fa2.sort_values(by = ['support'], ascending=False)
print(' ')
print(r'Please enter the path you prefer for storing the result. Example: C:\Users\HP\Desktop\ ')
result_path = input('Where do you hope to store the analysis result: ')
result_path1 = result_path+'market basket analysis result.csv'
freq_abov_2.to_csv(result_path1)
print('The market basket ananlysis result has been stored in '+ result_path1)

print(' ')
part2 = input('Do you want to enter the item recommendation procedure? (Please answer yes/no)')
if part2 == 'no':
    exit()
else:
    print('Please follow the following instruction.')
    print(' ')

# get support of each specific item
print(' ')
print('Note: Please only enter the name of one item(example:Slatted bed base) or one type of items(example: sofa).')
print('      And please note the case of latter.')
print(r'      If you expect to search the relevant items for specific type of item. It is supported. ')
print(r'      Multiple names are not supported.')
it = input('Which specific item do you hope to discuss : ')
maxlength = len(pure_list_un)-1
print(' ')
print('Note: The expected number of relevant items are suppose to be shorter than ' + str(maxlength) + ' which is the total longth of item list.')

# to make code more robust for the mistyping condition
item = [s for s in pure_list_un if it in s]
print (' ')
print('The item/items will be discussed here are illustrated below.')
for j in item:
    print(j)
print(' ')

long = input('How many relevant items are you expected to illustrate : ')
long = int(long)



for i in item:
    a = list()
    a.append(i)
    item_freq_an = rules[rules.antecedents == frozenset(a)]
    item_freq_co = rules[rules.consequents == frozenset(a)]
    item_freq = item_freq_an.append(item_freq_co)
    item_freq = item_freq.sort_values(by = ['support'], ascending=False)
    item_freq_list_an = list(item_freq.antecedents)
    item_freq_list_co = list(item_freq.consequents)
    item_freq_list = item_freq_list_an + item_freq_list_co
    item_freq_list = list(set(item_freq_list))
    if frozenset(a) in item_freq_list:
        item_freq_list.remove(frozenset(a))
    else:
        justwanttoskiphere = 0
    item_freq_list_un = []
    for z in item_freq_list:
        z = list(z)
        for q in z:
                item_freq_list_un.append(q)
    item_freq_list_un = list(set(item_freq_list_un))
    item_freq_list_un = item_freq_list_un[0:long]
    if len(item_freq) == 0:
        print(' ')
        print('Sorry, there is not enough historical data to support recommendation system for '+ i + ' .')
        print('Here are randomly generated item list which might be helpful.')
        random_item = random.sample(pure_list_un, long)
        for i in random_item:
            print (i)
    else:
        print(' ')
        print ('Here are items which are more likely to be bought with '+ i + '.')
        for y in item_freq_list_un:
            print(y)
        if len(item_freq_list_un) < long:
            print('Sorry. The relevant items are shorter than your expected. Here are some random items which might help.')
            random_item = random.sample(pure_list_un, long-len(item_freq_list_un))
            for i in random_item:
                print(i)


