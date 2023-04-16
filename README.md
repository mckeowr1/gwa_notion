

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

Each QTL has a phenotype ID and each GENE has a QTL and Phenotype ID. 


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

# Adding plots to pages - DEV** 

We would like some of the data to automatically uploaded to the pages, or at least linked to it.

To do this we first need to make sure the plots we want to display are hosted somewhere. Currently they are on my github URL ex) `https://mckeowr1.github.io/gwas_results/20221102_Thiabendazole_CV_combined_GWA_status.png`

Things we want to add plots to: 
- Phenotypes 
    - Trait distribution 
    - HTML Report 
    - Manhattan Plots
- QTL 
    -

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
