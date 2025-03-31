from vector_store import VectorStoreManager
import argparse
from typing import List, Dict
import json

def format_result(result: Dict) -> str:
    """Format a single search result for display."""
    output = "-" * 80 + "\n"
    output += f"URL: {result['metadata'].get('url', 'N/A')}\n"
    output += f"Title: {result['metadata'].get('title', 'N/A')}\n"
    
    # Format score with proper handling of None values
    score = result['score']
    if score is not None:
        output += f"Similarity Score: {score:.4f}\n"
    else:
        output += "Similarity Score: N/A\n"
    
    output += "\nContent Preview:\n"
    # Get first 200 characters of content
    preview = result['content'][:200] + "..." if len(result['content']) > 200 else result['content']
    output += preview + "\n"
    return output

def main():
    parser = argparse.ArgumentParser(description='Query your crawled web pages')
    parser.add_argument('query', type=str, help='The search query')
    parser.add_argument('--k', type=int, default=5, help='Number of results to return (default: 5)')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    args = parser.parse_args()

    # Initialize vector store
    vector_store = VectorStoreManager()
    
    # Search for similar documents
    results = vector_store.search_similar(args.query, k=args.k)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if not results:
            print("No results found.")
            return
            
        print(f"\nFound {len(results)} results for query: '{args.query}'\n")
        for result in results:
            print(format_result(result))

if __name__ == "__main__":
    main() 