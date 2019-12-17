# This class is used to scrape the htm file for messages to figure out the number of
# messages sent and received for a certain person. Really this is just kind of a method
# but I'm making it a class to practice how classes work in python.


# note, I think i should split it into class scrapes, class person, and class plot
import csv
from bs4 import BeautifulSoup
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns

me = "Jeremy Thaller"

# class object scrape_messages has attibutes of person's name and the total messages
# sent and received. could be useful to see lopsided friendships...
class scrape_messages:
    def __init__(self,name, total_messages_count=0):
        self.name = name
        self.total_messages_count = total_messages_count

person = scrape_messages('Rohan Kadambi')
print(person.name)
person.total_messages_count

# import the file to scrape.
messages_file_dir = "C:/Users/jerem/OneDrive/Documents/Python/messanger_count/facebook-jeremythaller/html/messages.htm"

# messages_file_dir = "C:/Users/jerem/OneDrive/Documents/Python/messanger_count/facebook-jeremythaller/html/simplified_ex.htm"
with open(messages_file_dir) as fp:
    soup = BeautifulSoup(fp,"html5lib")
print(soup.prettify())
	# // This is a note to myself to remember how the .htm is organized
	# /*
	#  * Theres only 1 </div> before the messages begin so ignore that
	#  * Next comes the overarching bucket
	#  * 		<div class = "contents"> - this div includes ALL of the messages (its not closed until the end of the doc)
	#  * Then begins the first thread
	#  * 		<div>
	#  * 		<div class="thread">INSERT PEOPLE'S NAMES DELIMED BY ","
	#  * 		<div class="message">
	#  * 		<div class="message_header">
	#  * 		<span class="user">INSERT NAME OF PERSON WHO SENT MESSAGE
	#  * 			<\span>- this closes the user
	#  * 		<span class="meta">{Day of WEEK}, {Month Text} {[D]D}, {YYYY} at [H]H:MM[a,p]m {Time Zone}
	#  * 			<\span>- this closes the meta
	#  * 			<\div>- this closes the message_header
	#  * 			<\div>- this closes the message
	#  * 		<p> INSERT MESSAGE TEXT
	#  * 			<\p> End Message Text
	#  *
	#  */

# Here's an example of on message, in this case one sent from me
    # <div class="message">
    #      <div class="message_header">
    #       <span class="user">
    #        Jeremy Thaller
    #       </span>
    #       <span class="meta">
    #        Monday, 17 December 2012 at 20:32 EST
    #       </span>
    #      </div>
    #     </div>
    #     <p>
    #      you're right
    #     </p>

messages = soup.find_all('p')

# for message in messages:
#     print(message)

# ok new idea is to just do this twice.once for names and once for timestamps. presumably they'll be in the same order
total_sent_by_me = 0
person.total_messages_count = 0

def write_to_csv(filename):
    total_sent_by_me = 0
    csvfile = open("chatdata.csv","w+")
    csvfile.close() #clear the spreadsheet if it exists.

    csvfile = csv.writer(open("chatdata.csv","w"))
    csvfile.writerow(["date", "sender"])
    # with open(messages_file_dir) as fp:
    #     # soup = BeautifulSoup(fp,"html5lib")
    #     soup = BeautifulSoup(fp,"lxml")
    with open(messages_file_dir, 'rb') as html:
        soup = BeautifulSoup(html)
    # get the dates, write them in a column for a csv file
    dates = soup.findAll('span',{'class' : 'meta'})
    senders = soup.findAll('span',{'class' : 'user'})
    # print(senders[5].contents[0])
    i=0
    for date in dates:
        date_data = date.contents[0].split(",", 1)
        # print(data)
        date_data = date_data[1].split("at")
        date_data = str(date_data[0])
        sender_data = str(senders[i].contents[0]) #get the name of the sender at the same index of the bs4 element
        csvfile.writerow([date_data,sender_data])
        i=i+1
        if sender_data == 'Jeremy Thaller':
            total_sent_by_me +=1

        if sender_data == person.name:
            person.total_messages_count +=1
    print("total sent by me: " + str(total_sent_by_me))
    print("Total sent by " + str(person.name) + ": " + str(person.total_messages_count))


write_to_csv(messages_file_dir)
df = pd.read_csv("C:/Users/jerem/OneDrive/Documents/Python/messanger_count/chatdata.csv", encoding = "ISO-8859-1")
df.describe()
df.head()
df.sender.value_counts()


#turns the dates from the previous function into YYY-MM-DD
#then sorts the dates from earliest to latest
def sort_data_by_dates(df):
    df['date'] = pd.to_datetime(df.date)
    df.head()
    print(df.sort_values('date').head())

sort_data_by_dates(df)


df.count()
df.shape
date = df['date'].values
count = df['0'].values
plt.plot()
plt.show()

plt.figure(figsize=(15,5))
plt.title('Cumsum messages vs. Time')
# The problem is that lineplot uses dashed lines for the second
# and any further column but the standard style only supports dashes for the first 6 colors.
plt.figure(figsize=(15,5))
plt.title('Messages sent+received per day')
sns.lineplot(data=df.iloc[:,0].value_counts(),dashes=False)
# sns.lineplot(data=flight_data.iloc[:,:6])
plt.plot(df.iloc[:,0].value_counts() )
plt.show()


df.iloc[:,0].value_counts()
df.iloc[:,0].max()
# briefly proving to myself that it's valid to find the attributes separately and combine them later because the list will
# be in the correct order. Thing are two things that I'm sure I said. Only I ran track and only rohan had a mac.
# print(soup.findAll('span',{'class' : 'user'})[7])
# print(soup.findAll('p')[7])
# print(soup.findAll('span',{'class' : 'user'})[4])
# print(soup.findAll('p')[4])
# print(soup.findAll('span',{'class' : 'meta'})[1].contents)
# print( soup.findAll(name='span', {'class' : 'meta'},text=lambda s: 'Jeremy Thaller' and 'Rohan Kadambi')) # all the messges sent by either me or rohan. includes timestamp data
# text=lambda s: "Fiscal" in s and "year" in s
