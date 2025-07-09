from bson import ObjectId
from fastapi import FastAPI
from odmantic import AIOEngine
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorClient;
from pydantic import BaseModel
client = AsyncIOMotorClient('mongodb+srv://admin:paAKVPjrPEYDJ9QK@cluster0.llnavj9.mongodb.net/')

engine_global = AIOEngine(client= client,database='Global_moduls')
engine_tenant = AIOEngine(client = client,database='tenant_module')

app=FastAPI()

class TenantContext(BaseModel):
    tenantId:str
    mongoDburl:str
    llmConfig:list
    tokenLimit:list
    enabledRules:list
    tier:list

@app.get("/tenant/{tenant_id}")
async def resolve_tenant_context(tenant_id:str):
    pipeline = [
        {'$match':{'tenantId':tenant_id}},
        {'$lookup':{
            'from': 'TokenLimit',
            'localField':'tenantId',
            'foreignField':'tenantId',
            'as':'tenantToken'
        }},
        {'$unwind':'$tenantToken'},
        {'$lookup':{
            'from': 'TenantRule',
            'localField':'tenantId',
            'foreignField':'tenantId',
            'as':'ruleID'                                        
        }},
        {'$unwind':'$ruleID'}
    ]
    tenantpipeline=[
        {'$match':{'tenantId':tenant_id}},
        {'$lookup':{
            'from':'Tier',
            'localField':'tierId',
            'foreignField':'_id',
            'as':'Tier'
        }},
        {'$unwind':'$Tier'}
    ]
    tenant = await engine_global.database["Tenant"].aggregate(tenantpipeline).to_list(length=None)
    llmcon = await engine_tenant.database["LLMConfig"].aggregate(pipeline).to_list(length=None)
    
    if not tenant:
        return f"This '{tenant_id}' id is not found"
    
    ruleID= llmcon[0]['ruleID']['globalRuleId']
    globalrule = await engine_global.database["GlobalRule"].find_one({'_id':ruleID})

    mongourl = tenant[0]['mongoUrl']
    tokenlimit= llmcon[0]['tenantToken']
    
    llmcon[0].pop('tenantToken')
    llmcon[0].pop('ruleID')
    

    Tenant_Context = TenantContext(
            tenantId=tenant_id,
            mongoDburl=mongourl,
            llmConfig=[llmcon[0]],
            tokenLimit=[tokenlimit],
            enabledRules=[globalrule],
            tier=[tenant[0]['Tier']]
    )
    
    return  jsonable_encoder(Tenant_Context.model_dump(),custom_encoder={ObjectId: str})


    