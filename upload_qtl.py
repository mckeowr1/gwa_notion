import requests, json

token = 'secret_Q5cktwWfIrqQK6udE6LK5A6Nb0B5QwSvmgVSlJuuooz'

databaseId = 'ab5c7392d488469d9d1ba5bfc8b3f802'

# Dictionary defining how to get to the API - first part of CURL request
headers = {
    "Authorization": "Bearer " + token, #
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}
def readDatabase(databaseId, headers):
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.request("POST", readUrl, headers=headers)
    data = res.json()
    print(res.status_code)
    print(res.text)

    #Dump the data base information into a JSON file
    with open('./db.json', 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)


def createPage(databaseId, headers):
    # Create a new page in the database
    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId }, #databaseId
        "properties": {
            "Description": { #Each property is its own dictionary
                "title": [
                    {
                        "text": {
                            "content": "Review"
                        }
                    }
                ]
            },
            "Value": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Amazing"
                        }
                    }
                ]
            },
            "Status": {
                "rich_text": [
                    {
                        "text": {
                            "content": "Active"
                        }
                    }
                ]
            }
        },

    "children": [
        {   "object": "block",
            "type": "image",
            "image": {
            "type" : "external",
            "external": {
                "url": "https://mckeowr1.github.io/gwas_results/20221102_Thiabendazole_CV_combined_GWA_status.png"
            }
             
            }
        }
        
    ]
    }
    
    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)

def createQTLPage(databaseId, headers, data):
    #Data is a dictionary for all the properties and images that will be uploaded
    # "QTL" : "QTL Name",
    # "Trait" : "Trait Name",
    #
    # Create a new page in the database
    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": databaseId }, #databaseId
        "properties": {
            "ID": { #Each property is its own dictionary
                "title": [
                    {
                        "text": {
                            "content": data['ID']
                        }
                    }
                ]
            },
            "CHROM": {
                "rich_text": [
                    {
                        "text": {
                            "content": data['CHROM']
                        }
                    }
                ]
            },
            "Trait": {
                "rich_text": [
                    {
                        "text": {
                            "content": data['Trait']
                        }
                    }
                ]
            },
            "log10p": {
                "rich_text": [
                    {
                        "text": {
                            "content": data['log10p']
                        }
                    }
                ]
            },        
            "peak_id": {
                "rich_text": [
                    {
                        "text": {
                            "content": data['peak_id']
                        }
                    }
                ]
            },
            "narrow_h2": {
                "rich_text": [
                    {
                        "text": {
                            "content": data['narrow_h2']
                        }
                    }
                ]
            }   
        },

    "children": [
        {   "object": "block",
            "type": "image",
            "image": {
            "type" : "external",
            "external": {
                "url": data['pxg']
            }
             
            }
        }
        
    ]
    }
    
    data = json.dumps(newPageData)
    # print(str(uploadData))

    res = requests.request("POST", createUrl, headers=headers, data=data)

    print(res.status_code)
    print(res.text)


createPage(databaseId, headers)
