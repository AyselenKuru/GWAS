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
base_url = "https://www.ebi.ac.uk/gwas/"

def start_download_export(table, gene):
    session = requests.Session()

    download_url = f"{base_url}api/v2/genes/{gene}/{table}/download"

    try:
        response = session.get(download_url)
        response.raise_for_status()

        filename = response.headers.get("Content-Disposition").split("filename=")[-1]
        with open(filename, "wb") as file:
            file.write(response.content)

        print(f"File '{filename}' downloaded successfully")
    except requests.exceptions.RequestException as e:
        print("Error downloading file:", e)
def extract_rsId(data):
    rs_id_list = []

    with open(data, 'r') as tsv_file:
        next(tsv_file)  # Skip the first line (header)
        for line in tsv_file:
            parts = line.strip().split('\t')
            if len(parts) > 0:
                rs_id_part = parts[0]
                if(rs_id_part.__contains__("-")):
                    rs_id= rs_id_part.split('-')
                    rs_id_list.append(rs_id[0])


    unique_rs_ids = list(set(rs_id_list))
    return unique_rs_ids

    unique_rs_ids = list(set(rs_id_list))
    return unique_rs_ids

if __name__ == '__main__':
   # gene_name = input('Enter the gene name: ')
    gene_name="SLC30A8"
    fetch_gene_variants(gene_name)
    file_name = f'{gene_name}_variants.json'
    t2d_rsIds = extract_dbSNPs(file_name)
    table = "associations"  # Change this to "studies" or "traits" as needed
    start_download_export(table, gene_name)
    gwas_rsIds = extract_rsId(gene_name + "_associations_export.tsv")
    for rs in gwas_rsIds:
        if t2d_rsIds.__contains__(rs):
            print(rs)

