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


*********************************tenant_resolver_function_lovic********************************

In i connect two database

1.Global_modules for get mongoUrl and global rule    
2.tenant_modules for get tokenlimit,Llm confi and tenantrule(for get globalID) 

**In tenant_modules i add tenantid field for TenantRule collection,TokenLimit collection,LLMconfig collection**

What i done in this code

Get the tenantid as a argument from user and using if condition to check the user is exist or not

**pipeline** to connect three collections llmconfig,tenanturl and teananttoken by tenantid

What This Pipeline Does

Filters the documents in the base collection to only include those matching the specified tenantId.

Joins:

TokenLimit collection to fetch token usage/limit settings.

TenantRule collection to get rules configured for that tenant.

Flattens the results using $unwind to simplify access to nested documents.

Cleans the output using $project by removing internal or unnecessary fields 


*get mongourl*--->  using tenant id in find_one() to get the tenantuser in Tenantcollection inv that we get the mongourl field

*get tokenlimit*---> pipeline return the llmCon in that we have tenantToken inside that i filter tokenlimit

*get llmconfig*---> pipeline return llmCon in that we get all data with join collection so using **pop()** to remove ruleID and tenantToken 

*get rules*---> in ruleID we get global ruleId field stored in new variable then connect globalrule collection and using **find_one()** and get rule for tenant 
