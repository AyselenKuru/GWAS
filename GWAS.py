import requests
import json

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

# Usage example
if __name__ == "__main__":
    gene_name = "SLC30A8"
    query_gwas_by_gene(gene_name)
