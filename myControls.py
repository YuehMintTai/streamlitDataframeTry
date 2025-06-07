import json, pandas as pd
import os, json
from openai import AzureOpenAI
endpoint = "https://azureaifoundrytryxxxxxxxxx.openai.azure.com/"
model_name = "gpt-4o"
deployment = "gpt-4o"
subscription_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
api_version = "2024-12-01-preview"

def select_case_by_index(index:int):
    '''
    return one record of index of dbJSON.json
    '''
    index=str(index)
    with open('dbJSON.json','r') as file:
        data=json.load(file)
    # return [index, data[index]['現在病史'], data[index]['病患性別'],
    #    data[index]['病患年齡'], data[index]['主訴'],data[index]['出院診斷'],
    #    data[index]['DEP'],data[index]['ADHD'],data[index]['ASD'],data[index]['pDEPm'], 
    #    data[index]['pADHDm'],data[index]['pASDm'], data[index]['pDEPgpt'],data[index]['pASDgpt'],
    #    data[index]['pADHDgpt'],data[index]['pDEPrag'],data[index]['pADHDrag'],data[index]['pASDrag']
    #    ]    
    return data[index]

def list_cases(begin:int, end:int):
    '''
    input two numbers (begin, end) then return a list of 
    full fields of records from begin to end of dbJSON.json
    '''
    with open('dbJSON.json','r') as file:
        data=json.load(file)
    myList=[]
    for index in range(begin,end):
        index=str(index)
        myList.append(data[index])
    return myList

def list_cases_simple(begin:int, end:int):
    '''
    input two numbers (begin, end) then return a list of 
    fewer fields from begin to end of dbJSON.json
    '''
    with open('dbJSON.json','r') as file:
        data=json.load(file)
    myList=[]
    for index in range(begin,end):
        index=str(index)
        myList.append(
            [index,  data[index]['病患性別'],data[index]['病患年齡'], 
             data[index]['主訴'],data[index]['DEP'],data[index]['ADHD'],
             data[index]['ASD']] 
        )
    return myList

def input_ratting(email:str,index:str,DEP:int,ASD:int,ADHD:int,satisfy:int,comment:str):
    '''
    convert ratting result into json string
    '''
    myJson={
        "email":email, "index":index, "DEP":DEP, "ASD":ASD,
        "ADHD":ADHD,"satisfy":satisfy, "comment":comment
    }
    return myJson

def save_rattting(myjson:json,index:int):
    index=str(index)
    with open('ratting.json','r')as file:
        data=json.load(file)
        data[index]=myjson
    try:
        with open('ratting.json','w',
                encoding='utf-8',errors='ignore')as file:
            json.dump(data,file,indent=4)
        return "save successfully"
    except Exception as e:
        return e

def AI_answer(myHx:str):
    client = AzureOpenAI(api_version=api_version,
                         azure_endpoint=endpoint,
                         api_key=subscription_key,)

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "你是精神襎專科醫師,根據所給予的病歷,推斷出精神科診斷(憂鬱症,\
                    注意力不足過動症 ,躁症, 自閉症,精神科飲食障礙, 環境適應障礙,\
                    思覺失調症, 自殺風險)的機率百分比,使用繁體中文和台灣常用用詞"\
                    "請使用json模式回答,且不要回答其他的精神疾病,也不用解釋原因。",
                },
                {
                    "role": "user",
                    "content": f"病歷內容:個案為12歲女性，由案父母陪同下步行入病室，精神可，情緒自控，外觀修飾尚可，被動配合入院護理及安檢，個案自小個性內向,學業成績差，畢業於國小，預就讀江翠國中，目前為暑假期間，因個案智能不足，加上過動症，課堂期間會唱歌或是遊走教室，甚至是往樓下丟物品，因此人際關係差，也容易在案母午休期間開門跑至阿公阿嬤家，小學三年級因有腦部有血塊，出現癲癇症狀，容易右側無力，於桃園長庚醫院做過質子刀手術治療後，情緒起伏大，未滿足需求，謾罵家人，摔家務，幻聽幻視症狀存，個案表示會看見影子以及聽到聲音要他做壞事，因此第一次於本院精神科門診追蹤，同年，個案不想寫作業撕掉作業，趁案母外出影印作業時，拿刀想要砍妹妹，妹妹跑回房間將門反鎖，案母回家後制止，而未受傷，因案母心軟，認為個案可再教化，故無入院接受治療，從此時開始個案會拿刀背壓手前臂和掐自己的行為，六年級下學期，曾於住家附近的攤位至留不走或是至小兒科診所將門反鎖，當時警察戒入後，案母仍選擇原諒個案，以及同校同學取笑個案智商下，個案想不開，欲從二樓走廊往下跳，在老師阻止下未成功，7/15號下午案母於玄關門準備案妹補習班的物品，個案趁案母不注意時鎖門，並威脅喊要傷害案妹，因案妹當時剛好拿著案母手機，案母聯絡案妹快躲進房間將房門反鎖，案母和親戚於門外哄騙個案開門要找案阿公阿嬤後，個案才開門，並將個案帶上救護車，入本院急診就醫，經主治醫師評估後收入院治療，此次為第一次住院"
                },
                {
                    "role": "assistant",
                    "content":  "憂鬱症機率:78.53%, 注意力不足過動症機率:25.13%,躁症機率:18.33%, 自閉症機率:13.09%,"\
                                "精神科飲食障礙: 3.66%, 環境適能障礙機率: 2.00%, 思覺失調症: 1.57%,自殺風險: 49.21%"
                },
                {
                    "role": "user",
                    "content": f"病歷內容:{myHx}",
                }
            ],
            max_tokens=4096,
            temperature=1.0,
            top_p=1.0,
            model=deployment
        )
        myResponse=response.choices[0].message.content.replace("\n","").replace("json","").replace('`',"")
        return myResponse

    except Exception as e:
        return str(e)



