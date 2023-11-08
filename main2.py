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
    time.sleep(8)  # Adjust the delay as needed
    explore_button = driver.find_element("xpath", "//button[contains(text(), ' Explore ± 50 kb ')]")
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

id_phen_gwas={}
def extract_rsId(data):
    #GWAS
    rs_id_list = []

    with open(data, 'r') as tsv_file:
        next(tsv_file)  # Skip the first line (header)
        for line in tsv_file:
            parts = line.strip().split('\t')
            if len(parts) > 0:
                rs_id_part = parts[0]
                pval=parts[1]
                trait=parts[8]
                rs_id=""
                tup=(trait,pval)
                if(rs_id_part.__contains__("-")):
                    rs_idl= rs_id_part.split('-')
                    rs_id=rs_idl[0]
                    rs_id_list.append(rs_id)
                else:
                    rs_id_list.append(rs_id_part)
            if id_phen_gwas.__contains__(rs_id):
                id_phen_gwas.get(rs_id).append(tup)
            else:
                insert=[]
                insert.append(tup)
                id_phen_gwas[rs_id]=insert


    unique_rs_ids = list(set(rs_id_list))
    return unique_rs_ids

id_phen={}
id_phen_t2d={}
def extract_dbSNPs():
    # T2D
    csv_file_path = f"downloaded_files/{gene_name}.csv"  # Replace with the path to your CSV file
    lead_dbSNPs = []

    with open(csv_file_path, "r", newline="") as file:
        next(file)

        for row in file:
            splitted = row.split(",")
            lead_snp = splitted[splitted.__len__()-6].strip('"')
            phen= splitted[splitted.__len__()-2].strip('"')
            pval=splitted[splitted.__len__()-19].strip('"')
            tup=(phen,pval)
            lead_dbSNPs.append(lead_snp)
            if id_phen_t2d.__contains__(lead_snp):
               id_phen_t2d.get(lead_snp).append(tup)

            else:
                insert = []
                insert.append(tup)
                id_phen_t2d[lead_snp] =insert


    return  list(set(lead_dbSNPs))


if __name__ == '__main__':
    gene_name = input('Enter the gene name: ')
    #gene_name="gpx1"
    gene_name= gene_name.upper()
    gene_name=gene_name.strip()
    #gene_name = "SLC30A8"
    t2d(gene_name)
    t2d_rsIds = extract_dbSNPs()

    table = "associations"  # Change this to "studies" or "traits" as needed
    gwas_variant_search(table, gene_name)



    gwas_rsIds = extract_rsId("downloaded_files/"+'gwas'+gene_name+".tsv" )
    print("GWAS RESULTS\n")
    for id in id_phen_gwas:
        inserted=id_phen_gwas.get(id)
        for elem in inserted:
            print(id+"\t"+elem[0]+"\t"+elem[1])
    print("\n\n")
    print("T2D Knowledge Portal Results\n")
    for id in id_phen_t2d:
        inserted = id_phen_t2d.get(id)
        for elem in inserted:
            print(id + "\t" + elem[0] + "\t" + elem[1])
    print("\n\n")
    print("COMMON VARIANTS\n")
    for rs in gwas_rsIds:
        if t2d_rsIds.__contains__(rs):
            pheno=id_phen_t2d[rs]
            print(rs)



file=f"results{gene_name}.txt"
with open(f"results{gene_name}.txt", "w") as file:
    file.write("GWAS RESULTS\n")
    for id in id_phen_gwas:
        inserted = id_phen_gwas.get(id)
        for elem in inserted:
            file.write(id + "\t" + elem[0] + "\t" + elem[1] + "\n")

    file.write("\n\n")
    file.write("T2D Knowledge Portal Results\n")
    for id in id_phen_t2d:
        inserted = id_phen_t2d.get(id)
        for elem in inserted:
            file.write(id + "\t" + elem[0] + "\t" + elem[1] + "\n")

    file.write("\n\n")
    file.write("COMMON VARIANTS\n")
    for rs in gwas_rsIds:
        if rs in t2d_rsIds:
            pheno = id_phen_t2d[rs]
            file.write(rs +"\n")

print("Data has been written to results.txt.")


