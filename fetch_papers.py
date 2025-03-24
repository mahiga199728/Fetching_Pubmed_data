from Bio import Entrez
import pandas as pd

from Bio import Entrez
import pandas as pd

# Set your email to use the PubMed API
Entrez.email = "your_email@example.com"

def fetch_pubmed(query: str, max_results: int = 10) -> list:
    """
    Fetch PubMed papers based on the query and include additional details.
    """
    try:
        # Search for papers
        handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()
        
        # Fetch paper details
        ids = record["IdList"]
        handle = Entrez.efetch(db="pubmed", id=ids, rettype="xml")
        papers = Entrez.read(handle)
        handle.close()
        
        results = []
        for paper in papers["PubmedArticle"]:
            # Extract basic information
            pubmed_id = paper["MedlineCitation"]["PMID"]
            title = paper["MedlineCitation"]["Article"]["ArticleTitle"]
            
            # Extract publication date
            pub_date = paper["MedlineCitation"].get("DateCompleted", {})
            publication_date = f"{pub_date.get('Year', 'Unknown')}-{pub_date.get('Month', 'Unknown')}-{pub_date.get('Day', 'Unknown')}"
            
            # Extract authors and affiliations
            authors = paper["MedlineCitation"]["Article"].get("AuthorList", [])
            non_academic_authors = []
            company_affiliations = []
            corresponding_author_email = ""

            for author in authors:
                # Extract affiliation details
                affiliation = ""
                if "AffiliationInfo" in author:
                    affiliation = author["AffiliationInfo"][0].get("Affiliation", "")
                    if "pharma" in affiliation.lower() or "biotech" in affiliation.lower():
                        non_academic_authors.append(author["LastName"])
                        company_affiliations.append(affiliation)
                
                # Extract corresponding author email (if available)
                if "CorrespondingAuthor" in author:
                    corresponding_author_email = author.get("CorrespondingAuthor", {}).get("Email", "")
            
            results.append({
                "PubmedID": pubmed_id,
                "Title": title,
                "PublicationDate": publication_date,
                "NonAcademicAuthors": ", ".join(non_academic_authors),
                "CompanyAffiliations": ", ".join(company_affiliations),
                "CorrespondingAuthorEmail": corresponding_author_email,
            })
        return results
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []


def save_to_csv(data, filename):
    """
    Save the data to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
    
    
    
import argparse
import sys

# Simulate command-line arguments for notebook execution
#sys.argv = ["fetch_papers.py", "cancer treatment", "--file", "results.csv"]
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", help="Filename to save results.", default="output.csv")
    args = parser.parse_args()
    
    # Pass the query dynamically to fetch_pubmed function
    papers = fetch_pubmed(args.query)
    if papers:
        save_to_csv(papers, args.file)
    else:
        print("No results found.")

print(f"Query received: {args.query}")

