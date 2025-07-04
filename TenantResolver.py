from pymongo import MongoClient;

client=MongoClient("mongodb+srv://admin:paAKVPjrPEYDJ9QK@cluster0.llnavj9.mongodb.net/") # connect with DB server 

globaldb=client["Global_moduls"]    # Connect global DB

collection = globaldb["Tenant"]
globalrule = globaldb["GlobalRule"]

tenantDB = client['tenant_module']  # connect tenantDB

llmconfigcol = tenantDB["LLMConfig"]
tokenlimitcol = tenantDB["TokenLimit"]
tenantrulecol = tenantDB["TenantRule"]

tenantID = input('Entet tenant ID:\n')

def tenant_resolver(tenant_id:str): 
    
    tenant = collection.find_one({'tenantId':tenant_id})
    
    if not tenant:
        print('tenant Id not found')
        return
    
    print('mongourl------------->',tenant['mongoUrl'],'\n\n')   # for mongoURL

    llmconfig = list(llmconfigcol.find({'tenantId':tenant_id}))
    print('llm------------>',llmconfig[0],'\n\n') # for llmConfig
    
    tokenlimit = list(tokenlimitcol.find({'tenantId':tenant_id}))
    print('tokenlimit======>',tokenlimit[0]['tokenLimit'],'\n\n')  # for Limit
    
    ruleid = list(tenantrulecol.find({'tenantId':tenant_id}))
    globalID =ruleid[0]['globalRuleId']
    globalRule = globalrule.find_one({'_id':globalID})
    
    print('rule-------------->',globalRule,'\n\n')
tenant_resolver(tenantID)
