from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
from sentence_transformers import SentenceTransformer
from datetime import datetime
import json
import os

class CommunityNavigator:
    """
    AI Agent for Community Resource Navigation
    Powered by Qdrant Vector Search
    
    Features:
    - Semantic search across resources
    - Long-term memory of user interactions
    - Personalized recommendations
    - Multi-criteria filtering
    """
    
    def __init__(self, client=None, model=None):
        """Initialize the navigator"""
        # Use provided client or create new one
        self.client = client if client else QdrantClient(":memory:")
        
        # Load embedding model
        self.model = model if model else SentenceTransformer('all-MiniLM-L6-v2')
        
        # Memory storage (simulates persistent user session)
        self.memory = []
        self.user_profile = {
            "frequent_categories": {},
            "search_count": 0,
            "first_interaction": datetime.now().isoformat()
        }
        
        print("✅ Community Navigator initialized")
    
    def search_resources(self, query, category_filter=None, top_k=5):
        """
        Search for relevant community resources using semantic similarity
        
        Args:
            query: Natural language search query
            category_filter: Optional category to filter by
            top_k: Number of results to return
            
        Returns:
            List of matching resources with relevance scores
        """
        print(f"\n🔍 Searching for: '{query}'")
        
        # Generate query embedding
        query_vector = self.model.encode(query).tolist()
        
        # Build filter if category specified
        search_filter = None
        if category_filter:
            search_filter = Filter(
                must=[
                    FieldCondition(
                        key="category",
                        match=MatchValue(value=category_filter)
                    )
                ]
            )
            print(f"   Filtering by category: {category_filter}")
        
        # Search in Qdrant - Using UPDATED API for v1.16+
        try:
            # New API (v1.16+)
            search_result = self.client.query_points(
                collection_name="community_resources",
                query=query_vector,
                limit=top_k,
                query_filter=search_filter,
                with_payload=True
            )
            results = search_result.points
        except AttributeError:
            # Fallback for older versions
            results = self.client.search(
                collection_name="community_resources",
                query_vector=query_vector,
                query_filter=search_filter,
                limit=top_k,
                with_payload=True
            )
        
        # Update memory
        self._add_to_memory(query, results, category_filter)
        
        print(f"   Found {len(results)} relevant resources")
        
        return results
    
    def _add_to_memory(self, query, results, category_filter=None):
        """
        Store search interaction in memory for personalization
        This demonstrates the MEMORY capability required by the challenge
        """
        memory_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "category_filter": category_filter,
            "num_results": len(results),
            "top_result": results[0].payload['name'] if results else None,
            "top_category": results[0].payload['category'] if results else None
        }
        
        self.memory.append(memory_entry)
        self.user_profile["search_count"] += 1
        
        # Track frequent categories
        if results:
            cat = results[0].payload['category']
            self.user_profile["frequent_categories"][cat] = \
                self.user_profile["frequent_categories"].get(cat, 0) + 1
    
    def get_recommendations(self, top_k=3):
        """
        Generate personalized recommendations based on search history
        This demonstrates the RECOMMENDATION capability
        
        Returns:
            List of recommended resources based on user patterns
        """
        if not self.memory:
            print("\n💡 No search history yet. Showing popular resources...")
            # Return general popular resources
            return self.search_resources("community services", top_k=top_k)
        
        print("\n💡 Generating personalized recommendations...")
        
        # Analyze past queries to understand user needs
        past_queries = [m['query'] for m in self.memory[-5:]]
        
        # Create a combined query from recent searches
        combined_query = " ".join(past_queries)
        print(f"   Based on your recent interests: {', '.join(past_queries[:3])}...")
        
        # Find related resources
        recommendations = self.search_resources(
            combined_query, 
            top_k=top_k * 2  # Get more to filter out already seen
        )
        
        # Filter out resources already seen
        seen_resources = set()
        for m in self.memory:
            if m['top_result']:
                seen_resources.add(m['top_result'])
        
        # Return unseen recommendations
        new_recommendations = [
            r for r in recommendations 
            if r.payload['name'] not in seen_resources
        ][:top_k]
        
        return new_recommendations
    
    def get_user_history(self):
        """
        Retrieve user's search history
        Demonstrates long-term memory capability
        """
        return {
            "memory": self.memory,
            "profile": self.user_profile
        }
    
    def analyze_user_patterns(self):
        """
        Analyze user search patterns for insights
        Shows how memory enables intelligent personalization
        """
        if not self.memory:
            return "No search history available yet."
        
        analysis = []
        analysis.append(f"Total searches: {len(self.memory)}")
        
        # Most frequent category
        if self.user_profile["frequent_categories"]:
            top_category = max(
                self.user_profile["frequent_categories"].items(),
                key=lambda x: x[1]
            )
            analysis.append(f"Most searched category: {top_category[0]} ({top_category[1]} times)")
        
        # Recent focus
        recent_categories = [m['top_category'] for m in self.memory[-3:] if m['top_category']]
        if recent_categories:
            analysis.append(f"Recent focus areas: {', '.join(set(recent_categories))}")
        
        return "\n".join(analysis)
    
    def export_memory(self, filepath='memory_export.json'):
        """
        Export user memory for persistence
        In production, this would save to a database
        """
        memory_data = {
            "history": self.memory,
            "profile": self.user_profile,
            "export_time": datetime.now().isoformat()
        }
        
        with open(filepath, 'w') as f:
            json.dump(memory_data, f, indent=2)
        
        print(f"✅ Memory exported to {filepath}")
    
    def display_result(self, result, rank=1):
        """Pretty print a search result"""
        payload = result.payload
        score = result.score
        
        print(f"\n{'='*60}")
        print(f"RANK #{rank} - Relevance Score: {score:.3f}")
        print(f"{'='*60}")
        print(f"📍 {payload['name']}")
        print(f"   Category: {payload['category']}")
        print(f"   {payload['description']}")
        print(f"   📞 Contact: {payload['contact']}")
        print(f"   📍 Location: {payload['location']}")
        print(f"   🕐 Hours: {payload['hours']}")
        print(f"   ⚡ Services: {payload['services']}")


# Quick test
if __name__ == "__main__":
    print("Testing Community Navigator...\n")
    
    # This would normally load from setup_qdrant.py
    # For testing purposes, we'll note that setup is required
    print("Note: Run setup_qdrant.py first to initialize the database")
    print("Then import this module in your demo script")