import argparse
import logging

from src.pdf_retriever import retrieve_all_season_pdfs
from src.pdf_summarizer import process_documents

FIA_URL = 'https://www.fia.com/documents/championships/fia-formula-one-world-championship-14/'

def main():
    parser = argparse.ArgumentParser(description='F1 FIA Document Parser')
    parser.add_argument('--force', action='store_true', help='Force re-download of PDFs')
    parser.add_argument('--season', type=str, required=False, help='Process documents for a given season')
    parser.add_argument('--gp', type=str, required=False, help='Process documents for a given GP')
    parser.add_argument('--event-notes', action='store_true', help='Process event notes for the given season and GP')
    parser.add_argument('--penalty-notes', action='store_true', help='Process penalties for the given season and GP NOT IMPLEMENTED')
    parser.add_argument('--verbosity', type=str, choices=['DEBUG', 'WARNING', 'DEFAULT'], default='DEFAULT', help='Set the verbosity level of the program')

    args = parser.parse_args()

    if args.verbosity == 'DEBUG':
        logging.basicConfig(level=logging.DEBUG)
    elif args.verbosity == 'WARNING':
        logging.basicConfig(level=logging.WARNING)
    else:
        logging.basicConfig(level=logging.INFO)

    print("========================================")
    print("=                                      =")
    print("=    Starting FIA F1 DOC Retrieval     =")
    print("=                                      =")
    print("========================================")
    print("Please wait while the program retrieves FIA PDFs...")

    if args.force:
        print("Force re-download enabled.")

    if args.season:
        print(f"Processing documents for season: {args.season}")

    if args.gp:
        print(f"Processing documents for GP: {args.gp}")
    
    if args.event_notes or args.penalty_notes:
        if args.event_notes:
            
            print(f"~~~~~ Processing the FIA Event Notes with LLM: {args.gp} ~~~~~")
            process_documents(args.season, args.gp, actions=['event_notes'], force=args.force)

        if args.penalty_notes:
            
            print(f"~~~~~ Processing the FIA Penalty Notes with LLM: {args.gp} ~~~~~")
            process_documents(args.season, args.gp, actions=['event_infringiments'], force=args.force)

    else:
        retrieve_all_season_pdfs(FIA_URL, force=args.force, season=args.season, gp=args.gp)

if __name__ == "__main__":
    main()