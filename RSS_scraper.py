import feedparser
import sqlite3
import threading as th


def rssParser(url1,url2,url3,url4):
    #It pulls RSS information from sites. 
    #RSS bilgilerini sitelerden çekiyor.
    parser1, parser2 = feedparser.parse(url1), feedparser.parse(url2)
    parser3, parser4 = feedparser.parse(url3), feedparser.parse(url4)
    
    global data1, data2, data3, data4
    
    
    #I appointed it to more than one variable because I created more than one table in the database.
    #Veritabanında birden fazla tablo oluşturduğum için birden fazla değişkene atadım. 
    data1 = [(entries.title, entries.author, entries.link, entries.summary, entries.published) for entries in parser1.entries]
    data2 = [(entries.title, entries.author, entries.link ,entries.summary, entries.published) for entries in parser2.entries]
    data3 = [(entries.title, entries.author, entries.link ,entries.summary, entries.published) for entries in parser3.entries]
    data4 = [(entries.title, entries.author, entries.link ,entries.summary, entries.published) for entries in parser4.entries]
    



def create_table(dbname):
    #I created the tables. 
    #Tabloları oluşturdum.
    db = sqlite3.connect(dbname)
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS datas(title, author, link, summary,  published)")
    # cursor.execute("CREATE TABLE IF NOT EXISTS bleepingcomputer(title, author, link, published)")
    # cursor.execute("CREATE TABLE IF NOT EXISTS threatpost(title, author, link, published)")
    # cursor.execute("CREATE TABLE IF NOT EXISTS thehackernews(title, author, link, published)")
    db.commit()
    cursor.close()


def Insertdata_and_check(dbname,data1,data2,data3,data4):
    db = sqlite3.connect(dbname)
    cursor = db.cursor()
    
    #Here, I checked whether the data from rss and the data in the database are the same. 
    #Burada rss den gelen veri ile, databasedeki verilerin aynı olup olmadığını kontrol ettirdim.
    for i in range(len(data4)):
        
        threatpost_datas = cursor.execute("SELECT link from datas where link=?", (data4[i][2],))
        threatpost_database_rows = threatpost_datas.fetchall()
        
        if threatpost_database_rows:
            continue
        else:
            d = (data4[i][0], data4[i][1], data4[i][2], data4[i][3], data4[i][4])
            cursor.execute("INSERT INTO datas VALUES(?,?,?,?,?)", d)


    for i in range(len(data1)):
        thehackernews_datas = cursor.execute("SELECT link from datas where link=?", (data1[i][2],))
        thehackernews_database_rows = thehackernews_datas.fetchall()

        ehackingnews_datas = cursor.execute("SELECT link from datas where link=?", (data3[i][2],))
        ehackinnews_database_rows = ehackingnews_datas.fetchall()
        
        if thehackernews_database_rows:
            continue
        elif ehackinnews_database_rows:
            continue
        else:
            thehackernews_dd = (data1[i][0], data1[i][1], data1[i][2], data1[i][3], data1[i][4])
            cursor.execute("INSERT INTO datas VALUES(?,?,?,?,?)", thehackernews_dd)
            ehackingnews_dd = (data3[i][0], data3[i][1], data3[i][2], data3[i][3], data3[i][4])
            cursor.execute("INSERT INTO datas VALUES(?,?,?,?,?)", ehackingnews_dd)
    
    
    for i in range(len(data2)):
        bleepingcomputer_datas = cursor.execute("SELECT link from datas where link=?", (data2[i][2],))
        bleepingcomputer_database_rows = bleepingcomputer_datas.fetchall()

        if bleepingcomputer_database_rows:
            continue
        else:
            bleepingcomputer_dd = (data2[i][0], data2[i][1], data2[i][2], data2[i][3], data2[i][4])
            cursor.execute("INSERT INTO datas VALUES(?,?,?,?,?)", bleepingcomputer_dd)
    db.commit()
    cursor.close()

def main():
    print("Starting scraper...")
    dbname = "rss_blogs.db"
    create_table(dbname)

    the_hacker_news_url = ["https://feeds.feedburner.com/TheHackersNews"]
    bleepingcomputer_url = ["https://www.bleepingcomputer.com/feed/"]
    ehackingnews_url = ["https://www.ehackingnews.com/feeds/posts/default"]
    threatpost_url = ["https://threatpost.com/feed/"]
    data = rssParser(the_hacker_news_url[0],bleepingcomputer_url[0],ehackingnews_url[0],threatpost_url[0])
    Insertdata_and_check(dbname, data1, data2, data3,data4)
    

    
    

if __name__ == "__main__":
    #It will run the main function every 3600 seconds 
    #Her 3600 saniye de bir main isimli fonksiyon çalışacak
    while True:
        timing = th.Timer(1.0,main)
        timing.run()



