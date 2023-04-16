import requests, json, csv, os

def createGENEPage(page_id, headers, gene_data):
    #Data is a dictionary for all the properties and images that will be uploaded
    # "QTL" : "QTL Name",
    # "Trait" : "Trait Name",
    #
    # Create a new page in the database
    createUrl = 'https://api.notion.com/v1/pages'

    newPageData = {
        "parent": { "database_id": page_id }, #databaseId
        "properties": {
            "GENE_NAME": { #Each property is its own dictionary
                "title": [
                    {
                        "text": {
                            "content": gene_data['GENE_NAME']
                        }
                    }
                ]
            },
            "CHROM": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['CHROM']
                        }
                    }
                ]
            },
            "POS": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['POS']
                        }
                    }
                ]
            },
            "VARIANT_IMPACT": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['VARIANT_IMPACT']
                        }
                    }
                ]
            },        
            "VARIANT_LD_WITH_PEAK_MARKER": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['VARIANT_LD_WITH_PEAK_MARKER']
                        }
                    }
                ]
            },
            "VARIANT_LOG10p": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['VARIANT_LOG10p']
                        }
                    }
                ]
            },
            "pct.divergent.ALT": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['pct.divergent.ALT']
                        }
                    }
                ]
            },
            "pct.divergent.REF": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['pct.divergent.REF']
                        }
                    }
                ]
            },
            "MAF_variant": {
                "rich_text": [
                    {
                        "text": {
                            "content": gene_data['MAF_variant']
                        }
                    }
                ]
            }  
        },
        "children": []
    }
    
    data = json.dumps(newPageData)
    # print(str(uploadData))
    print(data)
    res = requests.request("POST", createUrl, headers=headers, data=data)


    print(res.status_code)
    print(res.text)


    #Turn the response into a dictionary
    res_dict = json.loads(res.text)
    page_id = res_dict['id']

def updatePage(pageId, headers):
    updateUrl = 'https://api.notion.com/v1/databases/'

    gene_page_format = {
    "parent": {
            "type": "page_id",
            "page_id": pageId #QTL Page ID
        },
    "is_inline": True,        

        "title": [
            {
            "type": "text",
            "text": {
                "content": "Candidate Genes",
                "link": None
            }
            }
        ],
    "properties": {
        "GENE_NAME": {
            "title": {}
        },
        "CHROM": {
            "rich_text": {}
        },    
        "POS": {
            "rich_text": {}
        
        },
        "VARIANT_IMPACT": {
            "rich_text": {}
        },
        "VARIANT_LD_WITH_PEAK_MARKER": {
            "rich_text": {}
        },
        "VARIANT_LOG10p": {
            "rich_text": {}
        },
        "pct.divergent.ALT": {
            "rich_text": {}
        },
         "pct.divergent.REF": {
            "rich_text": {}
        },
        "MAF_variant": {
            "rich_text": {}
            }                              
        }
    }

    data = json.dumps(gene_page_format)

    response = requests.request("POST", updateUrl, headers=headers, data=data)

    print(response.status_code)
    print(response.text)
    


    #Turn the response into a dictionary
    res_dict = json.loads(response.text)
    
    #spit out the database ID that we just created
    return(res_dict['id'])

def createQTLPage(databaseId, headers, qtl_data):
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
                            "content": qtl_data['ID']
                        }
                    }
                ]
            },
            "CHROM": {
                "rich_text": [
                    {
                        "text": {
                            "content": qtl_data['CHROM']
                        }
                    }
                ]
            },
            "Trait": {
                "rich_text": [
                    {
                        "text": {
                            "content": qtl_data['Trait']
                        }
                    }
                ]
            },
            "log10p": {
                "rich_text": [
                    {
                        "text": {
                            "content": qtl_data['log10p']
                        }
                    }
                ]
            },        
            "peak_id": {
                "rich_text": [
                    {
                        "text": {
                            "content": qtl_data['peak_id']
                        }
                    }
                ]
            },
            "narrow_h2": {
                "rich_text": [
                    {
                        "text": {
                            "content": qtl_data['narrow_h2']
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
                "url": qtl_data['pxg']
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
    
    #Turn the response into a dictionary
    res_dict = json.loads(res.text)

    print("QTL Page Created, Creating Gene Page in " + res_dict['id'])
    
    #Add the gene table to the QTL page
    gene_db_id = updatePage(res_dict['id'], headers)
    
    #Get the candidate gene data for the QTL
    candidate_gene_dir = "20230411candidate_genes"

    #Search the candidate gene_dir for the QTL ID
    print("Searching for candidate genes file for QTL: " + qtl_data['Trait'] + "_" + qtl_data['CHROM'] + "_" + qtl_data['startPOS'] + "-" + qtl_data['endPOS'] + "_" + "loco_candidates.csv")
    for file in os.listdir(candidate_gene_dir):
        if file == (qtl_data['Trait'] + "_" + qtl_data['CHROM'] + "_" + qtl_data['startPOS'] + "-" + qtl_data['endPOS'] + "_" + "loco_candidates.csv"):
            print("Found file: " + file)
            candidate_gene_file = open(candidate_gene_dir + "/" + file, 'r+')
            csv_reader = csv.DictReader(candidate_gene_file)
            for i, row in enumerate(csv_reader):

                formatted_entry = {
                    'GENE_NAME': row['GENE_NAME'],
                    'CHROM': row['CHROM'],
                    'POS': row['POS'],
                    'VARIANT_IMPACT': row['VARIANT_IMPACT'],
                    'VARIANT_LD_WITH_PEAK_MARKER': row['VARIANT_LD_WITH_PEAK_MARKER'],
                    'VARIANT_LOG10p': row['VARIANT_LOG10p'],
                    'pct.divergent.ALT': row['pct.divergent.ALT'],
                    'pct.divergent.REF': row['pct.divergent.REF'],
                    'MAF_variant': row['MAF_variant'],
                    'Status': 'Active',

                    #Could add URL to wormbase if we wanted
                }
                createGENEPage(gene_db_id, headers, formatted_entry)
            
            candidate_gene_file.close()

    #createGENEPage(gene_db_id, headers)
    



#Create Gene Data base within each page
#createGENEPage(res_dict['id'], headers, data)






token = 'secret_Q5cktwWfIrqQK6udE6LK5A6Nb0B5QwSvmgVSlJuuooz'

databaseId = 'ab5c7392d488469d9d1ba5bfc8b3f802'

headers = {
    "Authorization": "Bearer " + token, #
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}



# Load the QTL CSV file
csv_file = open("QTL_peaks_loco.tsv", 'r+')
csv_reader = csv.DictReader(csv_file, delimiter='\t')

host_page = "https://mckeowr1.github.io/gwas_results/EffectPlots/"


for i, row in enumerate(csv_reader):

    formatted_entry = {
        'ID': row['marker'],
        'CHROM': row['CHROM'],
        'Trait': row['trait'],
        'log10p': row['log10p'],
        'startPOS': row['startPOS'],
        'peakPOS': row['peakPOS'],
        'endPOS': row['endPOS'],
        'peak_id': row['peak_id'],
        'narrow_h2': row['narrow_h2'],
        'Status': 'Active',

        #Combine the trait and marker into a single string divide the peak position by 1000 and round to four digits
        'pxg': host_page + row['trait'] + '_' + "CHR" + row['CHROM'] + '_' + str(round(int(row['peakPOS'])/1000000, 2)) + 'MB_effect_loco.plot.png',
        #'ld' : host_page + row['trait'] + '_' + "CHR" + row['CHROM'] + '_' + str(round(int(row['peakPOS'])/1000000, 2)) + 'MB_LD.png',
        #'fine_mapping' : 
    }

createQTLPage(databaseId, headers, formatted_entry)
    # Create a new page in the database for each row in the CSV file

