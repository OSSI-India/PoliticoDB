import urllib
import sqlite3
from bs4 import BeautifulSoup

db = sqlite3.connect('test.db')
c = db.cursor()
#c.execute('''CREATE TABLE mp ( name TEXT NOT NULL, constituency TEXT NOT NULL, state TEXT NOT NULL, perm_addr TEXT, perm_tel TEXT, delhi_addr TEXT, contact TEXT)''')

page = urllib.urlopen("MemberContactDetails.htm").read()

soup = BeautifulSoup(page,'html.parser')
rows = soup.findAll("tr")
vals = []
for tr in rows:
	cells = tr.findAll("td")
	if len(cells)>5:
		first = cells[1].text.strip().split('\n')
		name = first[0]
		place = first[2].replace(")","").split('(')
		const = place[0].strip()
		state = place[1].strip()
		perm_addr = cells[2].text.strip()
		perm_tel = cells[3].text.strip()
		delhi_addr = cells[4].text.strip()
		contact = cells[5].text.strip().replace("[AT]","@").replace("[DOT]",".")
		
		vals.append((name,const,state,perm_addr,perm_tel,delhi_addr, contact))

c.executemany('''INSERT INTO mp(name, constituency, state, perm_addr, perm_tel, delhi_addr, contact) VALUES(?,?,?,?,?,?,?)''', vals)

db.commit()

c.execute('''SELECT * FROM mp''')
for row in c:
    print(row)
 
db.close()
