# convolve-mas-community-navigator
AI-powered community resource navigator using Qdrant vector search - Convolve 4.0 MAS Track submission
# Community Resource Navigator

**Convolve 4.0 - MAS Track Submission**  
Powered by Qdrant Vector Search Engine


**BY TEAM: FIRST ORDER**
## 🎯 Project Overview

An AI-powered system that helps underserved communities discover relevant social services using semantic search, long-term memory, and personalized recommendations.

### Problem Solved
40% of eligible families don't access available community resources due to information fragmentation and discovery barriers. This system uses vector search to match people with services based on intent, not keywords.

### Key Features
- 🔍 **Semantic Search**: "I'm hungry" → finds food banks, meal centers, nutrition programs
- 🧠 **Memory**: Tracks search history to understand user needs over time
- 💡 **Recommendations**: Suggests related resources based on patterns
- 📊 **Multimodal**: Text descriptions + structured metadata (hours, location, contact)

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8 or higher
```

### Installation

1. **Clone/Download this project**
```bash
cd convolve-mas-submission
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the demo**
```bash
# Initialize Qdrant database with sample data
python setup_qdrant.py

# Run interactive demonstration
python demo_app.py
```

## 📁 Project Structure

```
convolve-mas-submission/
├── README.md                      # This file
├── PROJECT_DOCUMENTATION.md       # Full 10-page documentation
├── requirements.txt               # Python dependencies
├── setup_qdrant.py               # Database initialization
├── navigator.py                   # Core agent logic
├── demo_app.py                   # Interactive demo
└── data/
    └── community_resources.csv    # Sample dataset (auto-generated)
```

## 💻 Usage Examples

### Example 1: Basic Search
```python
from navigator import CommunityNavigator

nav = CommunityNavigator()
results = nav.search_resources("I need medical help but no insurance")

for result in results:
    print(result.payload['name'])
    print(f"Score: {result.score}")
```

### Example 2: Search with Filtering
```python
# Find only healthcare resources
results = nav.search_resources(
    query="free health services",
    category_filter="Healthcare",
    top_k=3
)
```

### Example 3: Get Recommendations
```python
# After several searches, get personalized suggestions
recommendations = nav.get_recommendations(top_k=5)
```

### Example 4: View Search History
```python
history = nav.get_user_history()
print(f"Total searches: {history['profile']['search_count']}")
```

## 🎬 Demo Output Preview

The demo runs through realistic scenarios:

```
SCENARIO 1: Emergency food assistance need
User Query: "I lost my job and need help feeding my family"

📋 Top 3 Matching Resources:

RANK #1 - Relevance Score: 0.847
📍 Daily Bread Food Bank
   Category: Food Assistance
   Emergency food supplies, weekly groceries for low-income households...
   📞 Contact: 555-0200
   📍 Location: 456 Oak Ave, West Side
   🕐 Hours: Tue-Sat 8AM-4PM
```

## 🔧 Technical Implementation

### Architecture
```
User Query → Embedding Model → Qdrant Vector Search → Ranked Results
                                         ↓
                                    Memory Storage
                                         ↓
                              Recommendation Engine
```

### Key Technologies
- **Qdrant**: Vector database for semantic search
- **SentenceTransformers**: Text embedding (all-MiniLM-L6-v2)
- **Python**: Core implementation
- **Pandas**: Data processing

### How It Works

1. **Setup Phase**:
   - Load 25 community resources
   - Generate 384-dimensional embeddings
   - Store in Qdrant with metadata

2. **Search Phase**:
   - User query → embedding vector
   - Qdrant finds similar vectors (cosine similarity)
   - Returns top-K matches with scores

3. **Memory Phase**:
   - Every search stored with timestamp
   - User profile built from patterns
   - Enables personalization

4. **Recommendation Phase**:
   - Analyzes past searches
   - Finds related resources not yet seen
   - Ranks by relevance

## 📊 System Capabilities

### ✅ SEARCH
- Semantic matching beyond keywords
- Category filtering
- Relevance scoring
- Sub-100ms response time

### ✅ MEMORY
- Long-term interaction tracking
- Pattern recognition
- User profiling
- Session persistence

### ✅ RECOMMENDATIONS
- History-based suggestions
- Avoids repetition
- Context-aware
- Adapts over time

### ✅ MULTIMODAL DATA
- Text (descriptions, services)
- Structured (category, hours, location)
- Extensible (images, geo-coordinates)

## 🎯 Evaluation Criteria

| Criterion | Implementation |
|-----------|---------------|
| Qdrant Usage | ✅ Core infrastructure, not just storage |
| Retrieval Quality | ✅ Semantic search with 0.8+ relevance scores |
| Memory Design | ✅ Persistent history with pattern analysis |
| Societal Impact | ✅ Addresses real barrier to social services |
| Documentation | ✅ Complete 10-page technical report |
| Creativity | ✅ Novel application to underserved communities |

## 🌟 Societal Impact

**Problem**: Information barriers prevent 40% of eligible families from accessing social services

**Solution**: Vector search enables natural language discovery
- "I'm struggling financially" → finds food banks, utility assistance, job training
- Remembers user needs across sessions
- Recommends related resources proactively

**Target Users**: 
- Low-income families
- Non-native English speakers
- Elderly individuals
- People in crisis situations

**Measurable Outcomes**:
- Reduce resource discovery time from hours to seconds
- Increase service utilization through easier access
- Provide personalized support through memory

## 🔒 Ethical Considerations

### Privacy
- No personally identifiable information stored
- Search history kept local by default
- Exportable for user control

### Bias Mitigation
- Diverse resource representation
- Regular coverage audits
- Community-driven updates

### Safety
- Not a replacement for emergency services (911)
- Provides information, not medical/legal advice
- Transparent about data sources

## 📈 Future Enhancements

### Near-term
- Multi-language support (Spanish, Chinese, Arabic)
- SMS interface for non-smartphone users
- Real-time resource updates

### Long-term
- Geographic radius filtering
- Eligibility pre-screening
- Appointment booking integration
- Impact analytics

## 🧪 Testing

Run included test scenarios:
```bash
python demo_app.py
```

Scenarios include:
1. Emergency food assistance
2. Healthcare for uninsured
3. Legal help for housing
4. Adult education (GED/ESL)
5. Mental health support

## 📝 Documentation

Full technical documentation available in:
- `PROJECT_DOCUMENTATION.md` - Complete 10-page report
- Code comments - Inline explanations
- This README - Quick reference

## 🤝 Contributing

This is a hackathon submission. For questions or collaboration:
- Review the documentation
- Examine the code
- Run the demo
- Provide feedback

## 📄 License

This project was developed for Convolve 4.0 educational purposes.

## 🙏 Acknowledgments

- **Qdrant** for vector search technology
- **Convolve 4.0** organizers for the challenge
- **Community organizations** whose work inspired this solution

## 📞 Support

For technical issues:
1. Check requirements are installed: `pip install -r requirements.txt`
2. Verify Python version: `python --version` (3.8+)
3. Review error messages in console output

## ✅ Submission Checklist

- [x] Reproducible code with clear instructions
- [x] Working demo demonstrating all capabilities
- [x] Comprehensive documentation (10 pages)
- [x] Qdrant integration (search + memory + recommendations)
- [x] Multimodal data handling
- [x] Societal impact clearly defined
- [x] Ethical considerations addressed
- [x] Evidence-based outputs with traceability

---

**Built with ❤️ for Convolve 4.0**  

*Making community resources accessible through AI*
