from pymongo import MongoClient;
client=MongoClient("mongodb+srv://admin:paAKVPjrPEYDJ9QK@cluster0.llnavj9.mongodb.net/") # connect with DB server 

globaldb=client["Global_moduls"]    # Connect global DB

collection = globaldb["Tenant"] #   use
globalrule = globaldb["GlobalRule"] #   use

tenantDB = client['tenant_module']  # connect tenantDB

llmconfigcol = tenantDB["LLMConfig"] # in use
tokenlimitcol = tenantDB["TokenLimit"]
tenantrulecol = tenantDB["TenantRule"]

save = tenantrulecol.save()

# tenantID = input('Entet tenant ID:')

# def resolve_tenant_context(tenant_id:str): 
    
#     pipeline = [
#         {'$match':{'tenantId':tenant_id}},
#         {'$lookup':{
#             'from': 'TokenLimit',
#             'localField':'tenantId',
#             'foreignField':'tenantId',
#             'as':'tenantToken'
#         }},
#         {'$unwind':'$tenantToken'},
#         {'$lookup':{
#             'from': 'TenantRule',
#             'localField':'tenantId',
#             'foreignField':'tenantId',
#             'as':'ruleID'                                        
#         }},
#         {'$unwind':'$ruleID'},
#         {'$project': {
#             '_id':0,
#             'tenantToken._id':0,
#             'tenantToken.role':0,
#             'tenantToken.llm':0,
#             'tenantToken.createdDate':0,
#             'rule._id':0,  
#         }}
#     ]
       
#     llmCon = list(llmconfigcol.aggregate(pipeline))
#     tenant = collection.find_one({'tenantId':tenant_id})
    
#     if not tenant:
#         print('This ',tenant_id,' id is not found')
#         return
    
#     ruleID=llmCon[0]['ruleID']['globalRuleId']
#     globalrules= globalrule.find_one({'_id':ruleID})
    
#     mongourl = tenant['mongoUrl']
#     tokenlimit= llmCon[0]['test']['tokenLimit']
    
#     llmCon[0].pop('tenantToken')
#     llmCon[0].pop('ruleID')
    
    
#     TenantContext={
#         "mongourl":mongourl,
#         'tokenlimit':tokenlimit,
#         'llmConfig':llmCon[0],
#         "globalrules":globalrules
#         }
    
    
#     return TenantContext    
    
# print(resolve_tenant_context(tenantID))   #tenantid-----tenant-001
