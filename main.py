from selenium import webdriver
import time
import os
import requests
import csv
def t2d(gene_name):


    # Get the current directory of the executed Python script
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Construct the URL with the gene name
    url = f"https://t2d.hugeamp.org/gene.html?gene={gene_name}"

    # Configure the Selenium driver with ChromeOptions to set download directory
    chrome_options = webdriver.ChromeOptions()
    download_directory = os.path.join(current_directory, "downloaded_files")
    if not os.path.exists(download_directory):
        os.makedirs(download_directory)
    prefs = {"download.default_directory": download_directory}
    chrome_options.add_experimental_option("prefs", prefs)
    # Add any desired Chrome options here

    driver = webdriver.Chrome(options=chrome_options)

    # Navigate to the URL
    driver.get(url)
    time.sleep(5)  # Adjust the delay as needed

    explore_button = driver.find_element("xpath","//button[contains(text(), 'Explore Region')]")
    explore_button.click()

    time.sleep(5)  # Adjust the delay as needed

    download_button = driver.find_element("xpath", "//button[contains(text(), 'Download')]")
    download_button.click()
    time.sleep(5)

    json_option = driver.find_element("xpath", "//a[contains(text(), 'CSV')]")
    json_option.click()

    # Wait for the download to complete
    time.sleep(5)  # Adjust the delay as needed

    # Rename the downloaded file
    original_filename = "clumped-variants.csv"  # Adjust the filename as needed
    new_filename = f"{gene_name}.csv"
    original_file_path = os.path.join(download_directory, original_filename)
    new_file_path = os.path.join(download_directory, new_filename)

    os.rename(original_file_path, new_file_path)
    # Close the browser
    driver.quit()


def gwas_variant_search(table, gene):
    session = requests.Session()
    base_url = "https://www.ebi.ac.uk/gwas/"
    download_url = f"{base_url}api/v2/genes/{gene}/{table}/download"
    download_directory="downloaded_files\\"
    try:
        response = session.get(download_url)
        response.raise_for_status()

        filename = f"gwas{gene_name}.tsv"
        file_path = os.path.join(download_directory, filename)

        with open(file_path, "wb") as file:
            file.write(response.content)

        print(f"File '{filename}' downloaded to '{download_directory}' successfully")
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

id_phen={}
def extract_dbSNPs():
    # Open the CSV file for reading
    csv_file_path = f"downloaded_files/{gene_name}.csv"  # Replace with the path to your CSV file
    lead_dbSNPs = []

    with open(csv_file_path, "r", newline="") as csvfile:
        csv_reader = csv.DictReader(csvfile)

        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Extract the value of the 'leadSNP' column
            lead_snp = row["group"]
            phen= row[None][row[None].__len__()-1]
            lead_dbSNPs.append(lead_snp)
            id_phen[lead_snp]=phen

    return  lead_dbSNPs

if __name__ == '__main__':
    gene_name = input('Enter the gene name: ')
    #gene_name="Vps37b"
    gene_name = gene_name.upper()
    gene_name = gene_name.strip()
    t2d(gene_name)
    t2d_rsIds = extract_dbSNPs()

    table = "associations"  # Change this to "studies" or "traits" as needed
    gwas_variant_search(table, gene_name)



    gwas_rsIds = extract_rsId("downloaded_files/"+'gwas'+gene_name+".tsv" )
    for rs in gwas_rsIds:
        if t2d_rsIds.__contains__(rs):
            pheno=id_phen[rs]
            print(rs+"\t"+pheno)


