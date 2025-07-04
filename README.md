TenantResolver file is function of Task1
input:tenant-001
mongoDb server url:mongodb+srv://admin:paAKVPjrPEYDJ9QK@cluster0.llnavj9.mongodb.net/

**above db file for if u cant reach mongo server use mongodump**

*step of use Mongodump*

1.Download -->MongoDB Command Line Database Tools Download in "https://www.mongodb.com/try/download/database-tool"

2.Use mongorestore with your Atlas connection URI:
bash
mongorestore --uri="mongodb+srv://<{username}>:<{password}>@<cluster-url>/{your-db-name}"

Replace:

username and password with your Atlas credentials.....
cluster-url with your Atlas cluster's URI...
your-db-name = name of the database you want to import....
./dump/your-db-name = path to the dumped database
