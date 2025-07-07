from pymongo import MongoClient;

client=MongoClient("mongodb+srv://admin:paAKVPjrPEYDJ9QK@cluster0.llnavj9.mongodb.net/") # connect with DB server 

globaldb=client["Global_moduls"]    # Connect global DB

collection = globaldb["Tenant"]
globalrule = globaldb["GlobalRule"]

tenantDB = client['tenant_module']  # connect tenantDB

llmconfigcol = tenantDB["LLMConfig"]
tokenlimitcol = tenantDB["TokenLimit"]
tenantrulecol = tenantDB["TenantRule"]

tenantID = input('Entet tenant ID:')

def resolve_tenant_context(tenant_id:str): 
    
    pipeline = [
        {'$match':{'tenantId':tenant_id}},
        {'$lookup':{
            'from': 'TokenLimit',
            'localField':'tenantId',
            'foreignField':'tenantId',
            'as':'test'
        }},
        {'$unwind':'$test'},
        {'$lookup':{
            'from': 'TenantRule',
            'localField':'tenantId',
            'foreignField':'tenantId',
            'as':'rule'                                        
        }},
        {'$unwind':'$rule'},
        {'$project': {
            '_id':0,
            'test._id':0,
            'test.role':0,
            'test.llm':0,
            'test.createdDate':0,
            'rule._id':0,  
        }}
    ]
    
    
    llmCon = list(llmconfigcol.aggregate(pipeline))
    tenant = collection.find_one({'tenantId':tenant_id})
    
    if not tenant:
        print('This ',tenant_id,' id is not found')
        return
    
    # print(tenant)
    ruleID=llmCon[0]['rule']['globalRuleId']
    globalrules= globalrule.find_one({'_id':ruleID})
    
    
    
    mongourl = tenant['mongoUrl']
    tokenlimit= llmCon[0]['test']['tokenLimit']
    
    llmCon[0].pop('test')
    llmCon[0].pop('rule')
    
    
    TenantContext={
        "mongourl":mongourl,
        'tokenlimit':tokenlimit,
        'llmConfig':llmCon[0],
        "globalrules":globalrules
        }
    
    
    return TenantContext    
    
print(resolve_tenant_context(tenantID))   #tenantid-----tenant-001
