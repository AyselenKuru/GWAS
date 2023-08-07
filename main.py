import requests
import json

def extract_dbSNPs(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    dbSNPs_list = []

    for entry in data.get('data', []):
        if 'dbSNP' in entry:
            if not dbSNPs_list.__contains__(entry["dbSNP"]):
                dbSNPs_list.append(entry['dbSNP'])


    return dbSNPs_list
def fetch_gene_variants(gene_name):
    url = 'https://bioindex.hugeamp.org/api/bio/query/gene-variants'
    params = {'q': gene_name}
    headers = {'accept': 'application/json'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()

        # Save the data as a JSON file
        file_name = f'{gene_name}_variants.json'
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        dbSNPs_list = extract_dbSNPs(file_name)

        print(f'Data saved successfully as {file_name}')
    else:
        print(f'Request failed with status code: {response.status_code}')
        print(response.text)
def extract_rsIds(json_data):
    rsIds_list = []

    if "_embedded" in json_data and "singleNucleotidePolymorphisms" in json_data["_embedded"]:
        snps_data = json_data["_embedded"]["singleNucleotidePolymorphisms"]

        for snp in snps_data:
            if "rsId" in snp:
                if not rsIds_list.__contains__(snp["rsId"]):
                 rsIds_list.append(snp["rsId"])

    return rsIds_list
def query_gwas_by_gene(gene_name):
    api_url = f"https://www.ebi.ac.uk/gwas/rest/api/singleNucleotidePolymorphisms/search/findByGene"
    params = {
        "geneName": gene_name
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes (e.g., 404, 500)

        snp_data = response.json()

        # Save the SNP data to a JSON file
        with open("GWAS.json", "w") as json_file:
            json.dump(snp_data, json_file, indent=4)


        print(f"GWAS data for gene {gene_name} retrieved and saved as GWAS.json")

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while retrieving data: {e}")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")

if __name__ == '__main__':
    gene_name = input('Enter the gene name: ')
   # gene_name="SLC30A8"
    fetch_gene_variants(gene_name)
    with open('GWAS.json', 'r') as f:
        json_data = json.load(f)
    list = extract_rsIds(json_data)
    file_name = f'{gene_name}_variants.json'
    dbSNPs_list = extract_dbSNPs(file_name)
    for rsID in list:
        if dbSNPs_list.__contains__(rsID):
            print(rsID)

