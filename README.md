# AI Social Media Post Generator v2.0

Transform academic papers into engaging LinkedIn posts using advanced AI workflows powered by LangGraph and OpenAI, now with **Supervisor Pattern** for enhanced orchestration!

## ✨ What's New in v2.0

- 🧠 **Supervisor Pattern**: AI supervisor coordinates specialized agents for optimal workflow
- 🎯 **Intelligent Routing**: Dynamic decision-making based on content quality and context
- 📊 **Enhanced Monitoring**: Detailed insights, quality metrics, and workflow analytics
- 🔄 **Adaptive Workflow**: Self-optimizing process that adapts to content complexity
- 🛡️ **Better Error Handling**: Robust recovery mechanisms and fallback strategies

## Features

- 🚀 **AI-Powered Generation**: Uses LangGraph workflows with OpenAI GPT-4
- 📄 **Academic Paper Processing**: Input paper titles and get structured summaries
- 📱 **Social Media Optimization**: Generates LinkedIn-optimized posts
- ✅ **Quality Verification**: Built-in technical and style checking
- 🔄 **Auto-Revision**: Automatically improves posts until quality standards are met
- 🎨 **Modern UI**: Beautiful, responsive React frontend with Tailwind CSS
- 🧠 **Supervisor Pattern**: Intelligent workflow orchestration (NEW!)

## Architecture

- **Backend**: FastAPI with LangGraph workflows + Supervisor Pattern
- **Frontend**: Next.js 14 with TypeScript and Tailwind CSS
- **AI**: OpenAI GPT-4 with LangChain agents + AI Supervisor
- **Orchestration**: Intelligent workflow routing and quality optimization
- **Deployment**: Vercel (full-stack)

### Workflow Patterns

#### 🧠 Supervisor Pattern (Recommended)
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Supervisor  │───▶│  Research   │───▶│ Summarize   │
│   Agent     │    │   Agent     │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘
       │                                      │
       ▼                                      ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Quality    │◀───│   Verify    │◀───│    Post     │
│ Monitoring  │    │   Agent     │    │   Agent     │
└─────────────┘    └─────────────┘    └─────────────┘
```

**Benefits**: Intelligent routing • Enhanced error handling • Quality optimization • Workflow insights

#### ⚡ Linear Pattern (Legacy)
```
Research → Summarize → Post → Verify → Complete
```

**Benefits**: Simple flow • Predictable execution • Lower overhead

## Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.9+
- OpenAI API key

### Local Development

1. **Clone and install dependencies**:
   ```bash
   git clone <your-repo>
   cd ai-social-media-generator
   npm install
   pip install -r requirements.txt
   ```

2. **Start the backend**:
   ```bash
   python -m uvicorn api.main:app --reload --port 8000
   ```

3. **Start the frontend** (in a new terminal):
   ```bash
   npm run dev
   ```

4. **Open your browser** to `http://localhost:3000`

5. **Enter your OpenAI API key** directly in the web interface

### Quick Setup Script

Run the setup script for automatic installation:
```bash
chmod +x setup_local.sh
./setup_local.sh
```

### Testing the Supervisor Pattern

Test the new supervisor pattern vs. linear workflow:
```bash
python test_supervisor_pattern.py
```

This will demonstrate:
- Performance comparison between patterns
- Quality metrics and insights
- Supervisor decision-making capabilities

## Deployment on Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/ai-social-media-generator)

### Manual Deploy

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Deploy**:
   ```bash
   vercel
   ```

3. **Set environment variables in Vercel dashboard**:
   - `OPENAI_API_KEY`: Your OpenAI API key

### Configuration

The app is configured for Vercel with:
- Frontend: Next.js app automatically deployed
- Backend: Python FastAPI serverless functions
- Environment: Production environment variables

## API Endpoints

### POST `/api/generate-post`

Generate a social media post using supervisor or linear pattern.

**Request:**
```json
{
  "paper_title": "LoRA: Low-Rank Adaptation of Large Language Models",
  "openai_api_key": "your-api-key",
  "use_supervisor": true
}
```

**Response (Supervisor Pattern):**
```json
{
  "summary": "Generated summary...",
  "post": "LinkedIn post content...",
  "verify_result": "pass",
  "revision_count": 1,
  "tech_check": "pass",
  "style_check": "pass",
  "supervisor_insights": {
    "completed_steps": ["research", "summarize", "post", "verify"],
    "workflow_efficiency": 1.0,
    "completion_reason": "quality_achieved"
  },
  "workflow_pattern": "supervised",
  "quality_metrics": {
    "overall_quality": 0.9,
    "mention_compliance": true,
    "character_efficiency": 0.8
  }
}
```

### GET `/api/workflow-info`

Get information about available workflow patterns.

**Parameters:**
- `use_supervisor` (boolean): Pattern to get info about

**Response:**
```json
{
  "pattern": "supervisor",
  "description": "AI supervisor coordinates specialized agents for optimal workflow",
  "benefits": ["Intelligent routing", "Enhanced error handling", "Quality optimization"],
  "status": {
    "supervisor_enabled": true,
    "agent_count": 4,
    "capabilities": {
      "intelligent_routing": true,
      "error_recovery": true,
      "adaptive_workflow": true
    }
  }
}
```

### POST `/api/generate-post-legacy`

Generate a post using the original linear workflow (for comparison).

## Development

### Project Structure

```
├── api/                    # FastAPI backend
│   ├── main.py            # API entry point
│   └── services/          # Business logic
│       ├── post_generator.py
│       ├── graph_builder.py
│       ├── agents.py
│       ├── tools.py
│       └── models.py
├── app/                   # Next.js frontend
│   ├── page.tsx          # Main page
│   ├── layout.tsx        # Root layout
│   └── globals.css       # Global styles
├── vercel.json           # Vercel configuration
├── package.json          # Node dependencies
└── requirements.txt      # Python dependencies
```

### Key Components

- **LangGraph Workflow**: Multi-agent system with research, summarization, and verification
- **Quality Assurance**: Automated technical and style checking with revision loops
- **Modern UI**: Responsive design with loading states and error handling

## Customization

### Adding New Tools

Add tools in `api/services/tools.py`:

```python
@tool
def your_custom_tool(input: str) -> str:
    """Your tool description."""
    # Your implementation
    return result
```

### Modifying the Workflow

Edit the graph structure in `api/services/graph_builder.py`:

```python
# Add new nodes
graph.add_node("your_node", your_agent)
graph.add_edge("existing_node", "your_node")
```

### Styling

Modify `tailwind.config.js` and `app/globals.css` for custom styling.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the example workflows

## Roadmap

- [ ] Support for multiple paper formats (PDF, URL)
- [ ] Additional social media platforms (Twitter, Facebook)
- [ ] Advanced paper analysis with semantic search
- [ ] Custom prompt templates
- [ ] Analytics and post performance tracking 