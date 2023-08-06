import requests
import json

def extract_dbSNPs(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    dbSNPs_list = []

    for entry in data.get('data', []):
        if 'dbSNP' in entry:
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
        for dbSNP in dbSNPs_list:
            print(dbSNP)

        print(f'Data saved successfully as {file_name}')
    else:
        print(f'Request failed with status code: {response.status_code}')
        print(response.text)

if __name__ == '__main__':
    gene_name = input('Enter the gene name: ')
   # gene_name="HBS1L"
    fetch_gene_variants(gene_name)
