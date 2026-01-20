"""
Community Resource Navigator - Demo Application
Convolve 4.0 - MAS Track Submission

This demo showcases:
1. Semantic Search - Finding resources based on meaning, not keywords
2. Memory - Tracking user interactions over time
3. Recommendations - Personalized suggestions based on history
4. Multimodal Data - Text + Structured information
"""

import sys
from setup_qdrant import setup_qdrant
from navigator import CommunityNavigator

def print_header(title):
    """Print formatted section header"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def run_demo():
    """Run interactive demo of the Community Navigator"""
    
    print_header("COMMUNITY RESOURCE NAVIGATOR")
    print("Powered by Qdrant Vector Search Engine")
    print("Convolve 4.0 - MAS Track Demo")
    print("\nInitializing system...")
    
    # Setup Qdrant and load data
    client, model = setup_qdrant()
    
    # Initialize navigator
    nav = CommunityNavigator(client=client, model=model)
    
    # Demo Scenarios - Simulating real user interactions
    scenarios = [
        {
            "query": "I lost my job and need help feeding my family",
            "category": None,
            "description": "Emergency food assistance need"
        },
        {
            "query": "Free medical checkup without insurance",
            "category": "Healthcare",
            "description": "Healthcare access for uninsured"
        },
        {
            "query": "My landlord is trying to evict me unfairly",
            "category": None,
            "description": "Legal assistance for housing dispute"
        },
        {
            "query": "Want to get my GED and learn English",
            "category": "Education",
            "description": "Adult education and ESL"
        },
        {
            "query": "Struggling with depression and anxiety",
            "category": None,
            "description": "Mental health support"
        }
    ]
    
    # Run through scenarios
    print_header("DEMONSTRATION: SEMANTIC SEARCH & MEMORY")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n\n{'─'*70}")
        print(f"SCENARIO {i}: {scenario['description']}")
        print(f"User Query: \"{scenario['query']}\"")
        print(f"{'─'*70}")
        
        # Search for resources
        results = nav.search_resources(
            query=scenario['query'],
            category_filter=scenario['category'],
            top_k=3
        )
        
        # Display results
        print(f"\n📋 Top {len(results)} Matching Resources:")
        for j, result in enumerate(results, 1):
            nav.display_result(result, rank=j)
        
        # Small pause for readability
        print("\n" + "─"*70)
    
    # Show memory capability
    print_header("MEMORY DEMONSTRATION: Search History Analysis")
    
    history = nav.get_user_history()
    print(f"\n📊 User Profile:")
    print(f"   Total searches: {history['profile']['search_count']}")
    print(f"   First interaction: {history['profile']['first_interaction']}")
    
    print(f"\n📝 Search History:")
    for i, entry in enumerate(history['memory'], 1):
        print(f"   {i}. [{entry['timestamp'][:19]}] \"{entry['query']}\"")
        print(f"      → Found: {entry['top_result']} ({entry['top_category']})")
    
    print(f"\n🎯 Pattern Analysis:")
    print(nav.analyze_user_patterns())
    
    # Show recommendations
    print_header("RECOMMENDATION DEMONSTRATION: Personalized Suggestions")
    
    recommendations = nav.get_recommendations(top_k=4)
    
    print("\n💡 Based on your search history, you might also be interested in:\n")
    for i, rec in enumerate(recommendations, 1):
        print(f"\n{i}. {rec.payload['name']}")
        print(f"   Category: {rec.payload['category']}")
        print(f"   Why recommended: Similar to your previous searches")
        print(f"   {rec.payload['description'][:100]}...")
        print(f"   📞 {rec.payload['contact']} | 📍 {rec.payload['location']}")
    
    # Demonstrate filtering
    print_header("ADVANCED SEARCH: Category Filtering")
    
    print("\n🔍 Searching specifically for Healthcare services...")
    healthcare_results = nav.search_resources(
        query="need medical help",
        category_filter="Healthcare",
        top_k=3
    )
    
    print(f"\n📋 Healthcare Resources:")
    for i, result in enumerate(healthcare_results, 1):
        print(f"\n{i}. {result.payload['name']}")
        print(f"   {result.payload['description'][:120]}...")
        print(f"   Score: {result.score:.3f}")
    
    # Export memory
    print_header("MEMORY PERSISTENCE")
    nav.export_memory('demo_memory_export.json')
    print("\n✅ User session data exported for future reference")
    
    # Final summary
    print_header("DEMONSTRATION COMPLETE")
    print("""
This demo showcased the three core capabilities required:

1. ✅ SEARCH: Semantic vector search using Qdrant
   - Natural language queries matched to resources by meaning
   - Category filtering for precise results
   - Cosine similarity scoring for relevance

2. ✅ MEMORY: Long-term interaction tracking
   - Every search stored with timestamp and context
   - User profile built from search patterns
   - Historical data persists across sessions

3. ✅ RECOMMENDATIONS: Personalized suggestions
   - Analyzes past queries to understand user needs
   - Suggests related resources not yet seen
   - Adapts to user patterns over time

4. ✅ MULTIMODAL DATA: Text + Structured information
   - Resource descriptions (text embeddings)
   - Metadata (category, location, hours, contact)
   - Combined for rich, contextual search

SOCIETAL IMPACT:
This system addresses real barriers to accessing community resources:
- Information fragmentation across multiple sources
- Language/literacy barriers requiring natural language search
- Time constraints requiring personalized recommendations
- Trust issues requiring evidence-based, traceable results

The system can scale to thousands of resources across multiple
communities, languages, and service types.
    """)
    
    print("\n" + "="*70)
    print("Thank you for reviewing this submission!")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please ensure all dependencies are installed:")
        print("pip install qdrant-client sentence-transformers pandas")