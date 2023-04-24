

# Env
Simply clone the repo locally and install the dependencies, preferably in a virtualenv:
Dev env location
```
## Package Plan ##

  environment location: /Users/ryanmckeown/anaconda3/envs/notion_upload
```

```shell
conda create -n notion_upload
conda activate notion_upload
codna install pip
cd gwa_notion
python3 -m venv venv
pip install --upgrade pip
pip install -r requirements.txt
```

# GWAS Data Directory Structure

1. Our GWAS results are stored on quest in `/projects/b1059/analysis/2021_GWA_analysis/data/20230330_Analysis_NemaScan`. This directory contains several sub-directories: 
    - Reports (contains HTML reports of mappings)
    - Phenotypes (trait files)
    - LOCO ()
        - Plots
            - ManhattanPlots
            - LDPlots
            - EffectPlots #P x G splits for each QTL
                - CV_length_Mancozeb_CHRV_17.66MB_effect_loco.plot.png
                - <trait>_CHR<chrom>_<peak_id>MB_effect_<algorithm>.plot.png
        - Mediation 
        - Mapping
            - Raw
                - Raw mapping resuls
            - Processed
                - QTL_peaks_loco.tsv *
                - processed_<trait>_AGGREGATE_mapping_loco.tsv
                - <trait>_AGGREGATE_qtl_region_loco.tsv
                - <trait>_LD_between_QTL_regions_loco.tsv
                - 
        - Fine_Mappings
            - Plots 
                - <trait>_<peak_start>.<peak_end>_finemap_plot_loco.pdf
                - <trait>_<peak_start>.<peak_end>_gene_plot_bcsq_loco.pdf

            - Data 
                - <trait>_<peak_start>.<peak_end>.LD_loco.tsv
                - <trait>_<peak_start>.<peak_end>.ROI_Genotype_Matrix_loco.tsv
                - <trait>_<peak_start>.<peak_end>_bcsq_genes_loco.tsv
                - <trait>_<peak_start>.<peak_end>.finemap_inbred.loco.fastGWA
        - Divergent_and_haplotype
    - INBRED
        - Plots
        - Mediation 
        - Fine_Mappings
        - Divergent_and_haplotype
    - Genotype_matrix 


# Notion Database
We currently have 3 data types in the database 

- Phenotype
    - QTL 
        - Gene Summary

Each Drug condition has a page with two traits for the drug response
    - Length 
    - C.V length
Every identified QTL from the GWAS is stored in the 2021 QTL database.

Each QTL page in the database has a table with the candidate genes for that QTL

# Running upload script
```{python}
python qt_page_dict.py
```
NEED TO:
- ADD COMMAND LINE ARGS FOR (CANDIDATE GENE DIR, LOCO_PEAKS.TSV, INBRED_PEAKS.TSV)
- PLACE FOR HOST DB INFORMATION (BEST PRACTICE?)

# Uploading QTL data 

To populate our QTL database, we will use `QTL_peaks_<algorithm>.tsv`files. 

```
CHROM	marker	log10p	trait	startPOS	peakPOS	endPOS	peak_id	narrow_h2
V	V:18040094	4.328322779723392	CV_length_Thiabendazole	17659349	18040094	18674756	1	0.013061552280705586
III	III:2878048	4.236260624118633	CV_length_Levamisole	2763660	2878048	2976570	1	0.1761694279292411
```

We use our function in `add_QTL.py` to read-in the peaks file and build a dictionary for each row in the file and uses the information to create a page within a notion database 

```
for i, row in enumerate(csv_reader):

    formatted_entry = {
        'ID':      {'type': 'title',        'value': row['marker']},
        'Phenotype':     {'type': 'multi_select', 'value': [row['trait']]},
        'log10p':      {'type': 'text',        'value': row['log10p']},
        'startPOS':      {'type': 'text',        'value': row['startPOS']},
        'peakPOS':      {'type': 'text',        'value': row['peakPOS']},
        'endPOS':      {'type': 'text',        'value': row['endPOS']},
        'peak_id':      {'type': 'text',        'value': row['peak_id']},
        'narrow_h2':      {'type': 'text',        'value': row['narrow_h2']},
    }
    
    notion.create_page(formatted_entry)
```

# Uploading Gene Data 

Our gene database is populated from a gene summary tsv script that produces the 10 genes with the most significant variants from finemapping. 

After generating our QTL page, we populate the page with candidate gene data base. 

First we retrieve the ID of the QTL page we just created as we will need to that to specify where we want to build the candidate gene table. 

```{python}
    #Save return of funtion - page ID as a variable
    QTL_PID = createQTLPage(databaseId, headers, formatted_entry)

    #Create a child database of specified format in the QTL page
    gene_db_id = createGENEDb(QTL_PID, headers)
```
The loop will then search for the QTL ID in the candidate gene files and pull the gene files that match into the script where they get formated and pasted into the candidate gene database - THIS SHOULD BE ITS OWN FUNCTION

```{python}
print("Searching for candidate genes file for QTL: " + row['trait'] + "_" + row['CHROM'] + "_" + row['startPOS'] + "-" + row['endPOS'] + "_" + "loco_candidates.csv")
    for file in os.listdir(candidate_gene_dir):
        if file == (row['trait'] + "_" + row['CHROM'] + "_" + row['startPOS'] + "-" + row['endPOS'] + "_" + "loco_candidates.csv"):
            print("Found file: " + file)
            candidate_gene_file = open(candidate_gene_dir + "/" + file, 'r+')
            csv_reader = csv.DictReader(candidate_gene_file)
            for i, gene_row in enumerate(csv_reader):

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
                createGENEPage(gene_db_id, headers, formatted_entry)
            
            candidate_gene_file.close()
```


# Adding plots to pages - DEV** 

We would like some of the data to automatically uploaded to the pages, or at least linked to it.

To do this we first need to make sure the plots we want to display are hosted somewhere. Currently they are on my github URL ex) `https://mckeowr1.github.io/gwas_results/20221102_Thiabendazole_CV_combined_GWA_status.png`

Things we want to add plots to: 
- Phenotypes 
    - Trait distribution 
    - HTML Report 
    - Manhattan Plots
- QTL 
    - PxG Split 
    - Fine mapping 
    - LD fine mapping
    - Mediation
    - Candidate genes DB



### Data strucutre for uploading to notion database 


```{bash}
curl 'https://api.notion.com/v1/pages' \
  -H 'Authorization: Bearer '"$NOTION_API_KEY"'' \
  -H "Content-Type: application/json" \
  -H "Notion-Version: 2022-06-28" \
  --data '{
	"parent": { "database_id": "d9824bdc84454327be8b5b47500af6ce" },
  "icon": {
  	"emoji": "🥬"
  },
	"cover": {
		"external": {
			"url": "https://upload.wikimedia.org/wikipedia/commons/6/62/Tuscankale.jpg"
		}
	},
	"properties": {
		"Name": {
			"title": [
				{
					"text": {
						"content": "Tuscan Kale"
					}
				}
			]
		},
		"Description": {
			"rich_text": [
				{
					"text": {
						"content": "A dark green leafy vegetable"
					}
				}
			]
		},
		"Food group": {
			"select": {
				"name": "Vegetable"
			}
		},
		"Price": { "number": 2.5 }
	},
	"children": [
		{
			"object": "block",
			"type": "heading_2",
			"heading_2": {
				"rich_text": [{ "type": "text", "text": { "content": "Lacinato kale" } }]
			}
		},
		{
			"object": "block",
			"type": "paragraph",
			"paragraph": {
				"rich_text": [
					{
						"type": "text",
						"text": {
							"content": "Lacinato kale is a variety of kale with a long tradition in Italian cuisine, especially that of Tuscany. It is also known as Tuscan kale, Italian kale, dinosaur kale, kale, flat back kale, palm tree kale, or black Tuscan palm.",
							"link": { "url": "https://en.wikipedia.org/wiki/Lacinato_kale" }
						}
					}
				]
			}
		}
	]
}'

```


## Requirements

To run the script, you will need the following things:

1. A CSV file exported from Paperpile containing the list of papers and their metadata. [data.csv](data.csv) is an example of an exported CSV. For now, this needs to be manually downloaded and moved to this folder since Paperpile does not provide any API for exporting data.

2. A configuration file to map categories, journals and conferences to their acronyms. [config.yaml](config.yaml) is an example of a configuration file containing major AI and NLP conferences and journals.

3. A database id for the Notion database you want to sync to. To retrieve the database id, follow the directions provided [here](https://developers.notion.com/docs/working-with-databases). The current structure for the database must contain at least the following columns:

    - `Item type`  ( `select` ): Corresponds to the `Item type` field in the Paperpile export (e.g. `Conference Paper`, `Journal Article`, etc.).

    - `Title`  ( `title` ): The title of the paper.

    - `Status` ( `select` ): Set to `Done` when the paper was read, empty otherwise. Can take other values. Managed by using a "Read" and a "To Read" folder inside Papepile.

    - `Authors` ( `multi_select` ): The paper's authors. Corresponds to the `Authors` field in the Paperpile export, with only lastnames and first letter of firstnames.

    - `Venues` ( `multi_select` ): The venues in which the paper was published. Based on the config sections for mapping names to acronyms. Multiselect to specify e.g. conference + arXiv.

    - `Date` ( `date` ): The date the paper was published.

    - `Link` ( `url` ): Link to the paper. If multiple links are available, arXiv links are preferred.

    - `Categories` ( `multi_select` ): The categories the paper belongs to. Define the macro-fields to which the paper belongs. These are extracted from the labels that were assigned to the paper on Paperpile.

    - `Methods` ( `multi_select` ): The methods and aspects investigated in the paper. Can be whatever, from architectures (e.g. CNN, Transformer) to sub-topics. On Paperpile, these correspond to labels having the following format: `category_shortname - method_name` (e.g. Probing tasks for interpretability research could be `INT - Probing`). Refer to the CSV file for an example.

4. A Notion API key. To retrieve the API key, follow the directions provided in the [Notion API Getting Started](https://developers.notion.com/docs/getting-started). You will also need to add permission for the integration on the database from the previous point.

## Usage

Once everything is in place, simply run the script as:

```shell
python update_notion_db.py \
    --input data.csv \
    --config config.yaml \
    --database <YOUR_DB_ID> \
    --token <YOUR_NOTION_API_KEY>
```

The experimental script to auto-download a folder from Paperpile can be run as:

```shell
python download_paperpile_dir.py \
    --username <YOUR_GOOGLE_USERNAME> \
    --password <YOUR_GOOGLE_PASSWORD> \
    --folder_id <YOUR_FOLDER_ID> # e.g. pp-folder-2cb1833f-582f-0000-ad59-567be5718692
```

This will download the folder content in CSV format in the default download location.

Example output, adding a new paper to the database:

![Console output](img/output.png)

Example resulting database on Notion:

![Notion result](img/notion_result.png)
