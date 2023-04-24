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

def createGENEDb(pageId, headers):
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
            "type": "pdf",
            "pdf": {
            "type" : "external",
            "external": {
                "url": qtl_data['fine_ld']
            }
             
            }
        },
            {   "object": "block",
            "type": "pdf",
            "pdf": {
            "type" : "external",
            "external": {
                "url": qtl_data['bcsq_gene']
            }
             
            }
        },        
        {   "object": "block",
            "type": "image",
            "image": {
            "type" : "external",
            "external": {
                "url": qtl_data['pxg']
            }
             
            }
        },
        {   "object": "block",
            "type": "image",
            "image": {
            "type" : "external",
            "external": {
                "url": qtl_data['mediation']
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
    
  
    #return the page id so we can create something in it
    return(res_dict['id'])

def formatQTL(qtl_row, host_page, algorithm):
    #Format the QTL data into a dictionary
    #algorithm is either "inbred" or "loco"
    formatted_entry = {
    'ID': qtl_row['marker'],
    'CHROM': qtl_row['CHROM'],
    'Trait': qtl_row['trait'],
    'log10p': qtl_row['log10p'],
    'startPOS': qtl_row['startPOS'],
    'peakPOS': qtl_row['peakPOS'],
    'endPOS': qtl_row['endPOS'],
    'peak_id': qtl_row['peak_id'],
    'narrow_h2': qtl_row['narrow_h2'],
    'Status': 'Active',
    'Algorithim' : algorithm,

    #Combine the trait and marker into a single string divide the peak position by 1000 and round to four digits
    'pxg': host_page + "EffectPlots/" + qtl_row['trait'] + '_' + "CHR" + qtl_row['CHROM'] + '_' + str(round(int(qtl_row['peakPOS'])/1000000, 2)) + 'MB_effect_' + algorithm + 'plot.png',
    #'ld' : host_page + qtl_row['trait'] + '_' + "CHR" + qtl_row['CHROM'] + '_' + str(round(int(qtl_row['peakPOS'])/1000000, 2)) + 'MB_LD.png'
    #fine mapping LD plot - ex) CV_length_Monepantel_LY3348298_0_55.III.8220.1574164_finemap_plot_loco.pdf
    'fine_ld': host_page + qtl_row['trait'] + '.' + qtl_row['CHROM'] + '.' + qtl_row['startPOS'] + '.' + qtl_row['endPOS'] + "_finemap_plot_" + algorithm + ".pdf",
    
    #BCSQ GENE plots - ex) CV_length_Copper_chloride_V_15173542-16832320_gene_plot_bcsq_loco.pdf
    'bcsq_gene': host_page + qtl_row['trait'] + '_' + qtl_row['CHROM'] + '_' + qtl_row['startPOS'] + '-' + qtl_row['endPOS'] + "_gene_plot_bcsq_" + algorithm + ".pdf", 

    #Mediation - ex) length_Zoetis_7027187_emed_detailed_plot_loco.png
    'mediation': host_page + qtl_row['trait'] + "_emed_detailed_plot_" + algorithm + ".png"
    }
    return(formatted_entry)

def formatGENE(gene_row):
    formatted_entry = {
        'GENE_NAME': gene_row['GENE_NAME'],
        'CHROM': gene_row['CHROM'],
        'POS': gene_row['POS'],
        'VARIANT_IMPACT': gene_row['VARIANT_IMPACT'],
        'VARIANT_LD_WITH_PEAK_MARKER': gene_row['VARIANT_LD_WITH_PEAK_MARKER'],
        'VARIANT_LOG10p': gene_row['VARIANT_LOG10p'],
        'pct.divergent.ALT': gene_row['pct.divergent.ALT'],
        'pct.divergent.REF': gene_row['pct.divergent.REF'],
        'MAF_variant': gene_row['MAF_variant'],
        'Status': 'Active',

        #Could add URL to wormbase if we wanted
    }
    return(formatted_entry)


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

host_page = "https://mckeowr1.github.io/gwas_results/"


for i, qtl_row in enumerate(csv_reader):

    #Format the QTL data into a dictionary
    formatted_entry = formatQTL(qtl_row, host_page)
    
    QTL_PID = createQTLPage(databaseId, headers, formatted_entry)
    # Create a new page in the database for each row in the CSV file
#Create a gene database in the QTL page
    gene_db_id = createGENEDb(QTL_PID, headers)
    
    #Get the candidate gene data for the QTL
    candidate_gene_dir = "20230411candidate_genes"

    #Search the candidate gene_dir for the QTL ID
    print("Searching for candidate genes file for QTL: " + qtl_row['trait'] + "_" + qtl_row['CHROM'] + "_" + qtl_row['startPOS'] + "-" + qtl_row['endPOS'] + "_" + "loco_candidates.csv")
    for file in os.listdir(candidate_gene_dir):
        if file == (qtl_row['trait'] + "_" + qtl_row['CHROM'] + "_" + qtl_row['startPOS'] + "-" + qtl_row['endPOS'] + "_" + "loco_candidates.csv"):
            print("Found file: " + file)
            candidate_gene_file = open(candidate_gene_dir + "/" + file, 'r+')
            csv_reader = csv.DictReader(candidate_gene_file)
            for i, gene_row in enumerate(csv_reader):
                formatted_entry = formatGENE(gene_row)
                createGENEPage(gene_db_id, headers, formatted_entry)
            
            candidate_gene_file.close()

    #createGENEPage(gene_db_id, headers)
    
