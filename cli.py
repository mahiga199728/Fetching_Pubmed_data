from fetch_papers import fetch_pubmed, save_to_csv
import argparse
import logging

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", help="Search query for PubMed.")
    parser.add_argument("-f", "--file", help="Filename to save results.", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    args = parser.parse_args()
    
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
        logging.debug(f"Debug mode enabled. Query: {args.query}")
    
    papers = fetch_pubmed(args.query)
    if papers:
        if args.file:
            save_to_csv(papers, args.file)
        else:
            for paper in papers:
                print(paper)
    else:
        print("No results found.")

if __name__ == "__main__":
    main()
