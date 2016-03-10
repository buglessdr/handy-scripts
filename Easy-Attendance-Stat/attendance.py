try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
     print '''
                The program requests requests module and BeautifulSoup to run.
             You can easily install them using pip using the following command:
                pip install requests BeautifulSoup lxml
     '''
     user = raw_input("Do you want to install them now?(Y/n)")
     if user == "y" or user == "Y":
         try:
             import pip
         except ImportError:
             print "You have to install pip!"
         else:
             pip.main(['install','requests'])
             pip.main(['install','bs4'])


else:
    url = 'http://www-mec.mec.ac.in/attn/view4stud.php'
    class_ = ['B2','B4','B6','B8','C2A','C2B','C4A','C4B','C6A','C6B','C8A','C8B','E2A','E2B','E4A','E4B','E6A','E6B','E8A','E8B','EE2','EE4','EE6','EE8']
    def getClass(c):
        print "Choose Your Class"
        for a,b in zip(c[::2],c[1::2]): print "%d.   %s   %d.   %s"%(c.index(a)+1,a,c.index(b)+1,b)
        choice = int(raw_input('Enter your choice(default=5):') or 5)
        return c[choice - 1]
    data = {'class': getClass(class_)}

    roll_no = input('Enter Your Roll no:')
    response = requests.post(url,data=data)

    soup = BeautifulSoup(response.text,"html.parser")
    table = soup.find(lambda t: t.name == 'table')
    rows = table.findAll(lambda t: t.name == 'tr')

    headers = [x.text.strip() for x in rows[1].findAll('td')]

    dataset = []
    c = 0
    for row in rows:
        if 'Name' in row.text: c = rows.index(row)
    for row in rows[c+1:]:
        d = [x.text.strip() for x in row.findAll('td')]
        dataset.append(zip(headers,d))

    def print_your_data(your_data):
        for a,b in your_data:
            print a,"      ",b
    while True:
        try:
            your_data = dataset[int(roll_no)]
        except ValueError:
            if roll_no != 'q' or roll_no != 'Q':
                break
            print "Invalid Input"
            break
        except IndexError:
            print "Invalid Roll Number"
            break
        else:
            print_your_data(your_data)

            roll_no = raw_input('Enter another roll no(q to quit):')


    
