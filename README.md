# FinAgent Orchestrator

A sophisticated multi-agent financial orchestration system that leverages LangGraph workflows and Model Context Protocol (MCP) to provide intelligent loan approval and risk assessment services.

## 🏗️ Architecture Overview

FinAgent Orchestrator is built on a modern, modular architecture that combines:

- **LangGraph Workflow Engine**: Orchestrates complex multi-agent decision flows
- **MCP (Model Context Protocol)**: Provides standardized tool interfaces for external systems
- **Specialized AI Agents**: Domain-specific agents for decision-making, fraud detection, and risk assessment
- **FastAPI Backend**: High-performance REST API server
- **React Frontend**: Responsive user interface

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│              User Interface & Interaction Layer              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend (main.py)                  │
│                    HTTP Request Handler                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              LangGraph Workflow (workflow.py)                │
│                  Multi-Agent Orchestration                   │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Decision  │  │   Fraud    │  │    Risk    │            │
│  │   Agent    │  │   Agent    │  │   Agent    │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              MCP Client (client.py)                          │
│          Protocol Communication & Tool Execution             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            MCP Server (server.py + tools.py)                 │
│         Tool Registry & External System Integration          │
│  • Credit Score Lookup   • Fraud Blacklist Check            │
│  • Macro Context Retrieval                                   │
└─────────────────────────────────────────────────────────────┘
```

## 📋 Features

### Core Capabilities

- **🔍 Multi-Agent Decision Making**: Coordinated workflow across specialized agents
- **🛡️ Fraud Detection**: Real-time blacklist checking and risk scoring
- **📊 Risk Assessment**: Comprehensive credit evaluation with macro-economic context
- **🔗 MCP Integration**: Standardized protocol for tool invocation and external system access
- **🚀 Async Processing**: High-performance asynchronous request handling
- **🎯 Stateful Workflows**: LangGraph-powered state management throughout decision process

### Agent Responsibilities

#### Decision Agent
- Orchestrates the overall loan approval workflow
- Coordinates between fraud and risk agents
- Makes final approval/rejection decisions
- Synthesizes multi-agent insights

#### Fraud Agent
- Checks applicants against compliance blacklists
- Validates customer information
- Flags suspicious patterns
- Provides fraud risk scores

#### Risk Agent
- Evaluates credit worthiness
- Analyzes default history
- Assesses macro-economic factors
- Calculates risk-adjusted loan terms

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- npm or yarn

### Installation

#### Backend Setup

```bash
# Clone the repository
git clone https://github.com/emmacyu/FinAgent_Orchestrator.git

# Create virtual environment
python -m venv venv_finagent
source venv_finagent/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd FinAgent_Orchestrator/backend
pip install -r requirements.txt

# Edit .env to add API keys
```

#### Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

### Running the Application

#### Start the Backend

```bash
cd backend
python main.py
```

The API server will start at `http://localhost:8000`

#### Start the Frontend

```bash
cd frontend
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📁 Project Structure

```
FinAgent_Orchestrator/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── agents/
│   │   ├── decision_agent.py   # Main orchestration agent
│   │   ├── fraud_agent.py      # Fraud detection agent
│   │   └── risk_agent.py       # Risk assessment agent
│   ├── graph/
│   │   └── workflow.py         # LangGraph workflow definition
│   ├── mcp/
│   │   ├── server.py           # MCP tool server
│   │   ├── client.py           # MCP client implementation
│   │   └── tools.py            # External tool integrations
│   └── requirements.txt        # Python dependencies
│
└── frontend/
    ├── src/
    │   ├── App.tsx             # Main React component
    │   ├── main.tsx            # Application entry point
    │   └── components/         # React components
    ├── package.json            # Node dependencies
    └── vite.config.ts          # Vite configuration
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# MCP Server Configuration
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=3000

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

### MCP Tools Configuration

The MCP server exposes three main tools:

1. **get_client_credit_context**: Retrieves credit scores and history
2. **check_fraud_blacklist**: Validates against known fraud entities
3. **get_macro_context**: Fetches real-time economic indicators

## 🔄 Workflow Process

### Loan Application Flow

```
1. User submits loan application
        ↓
2. Decision Agent receives request
        ↓
3. Parallel execution:
   ├─→ Fraud Agent checks blacklist
   └─→ Risk Agent assesses creditworthiness
        ↓
4. Decision Agent synthesizes results
        ↓
5. Final decision returned to user
   (Approved/Rejected with reasoning)
```

### State Management

The workflow maintains a structured state object:

```python
{
    "client_id": "C001",
    "client_name": "Example Corp",
    "loan_amount": 50000,
    "fraud_check": {
        "passed": True,
        "details": "..."
    },
    "risk_assessment": {
        "credit_score": 750,
        "default_history": "Clean",
        "recommendation": "..."
    },
    "decision": "Approved",
    "reasoning": "..."
}
```

## 🛠️ API Reference

### Endpoints

#### POST /api/loan-application

Submit a loan application for processing.

**Request Body:**
```json
{
  "client_id": "C001",
  "client_name": "Example Corp",
  "loan_amount": 50000,
  "purpose": "Business expansion"
}
```

**Response:**
```json
{
  "decision": "Approved",
  "reasoning": "Strong credit profile with no fraud indicators",
  "credit_score": 750,
  "approved_amount": 50000,
  "interest_rate": 5.5,
  "terms": "36 months"
}
```

#### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "mcp_server": "connected",
  "timestamp": "2024-03-28T10:00:00Z"
}
```

## 🧪 Testing

### Unit Tests

```bash
cd backend
pytest tests/
```

### Integration Tests

```bash
pytest tests/integration/
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📊 MCP Tool Details

### Tool: get_client_credit_context

**Purpose**: Retrieves internal credit data for a given client

**Input**:
- `client_id` (string): Unique client identifier

**Output**:
```json
{
  "score": 750,
  "history": "Clean",
  "limit": 50000
}
```

### Tool: check_fraud_blacklist

**Purpose**: Checks if an entity is on the compliance blacklist

**Input**:
- `name` (string): Entity name to check

**Output**:
- `boolean`: True if blacklisted, False otherwise

### Tool: get_macro_context

**Purpose**: Fetches real-time macroeconomic data

**Input**:
- `country` (string, default="Canada"): Target country

**Output**:
- `string`: Current economic indicators and interest rates

## 🔐 Security Considerations

- All API endpoints should be protected with authentication in production
- Sensitive customer data must be encrypted at rest and in transit
- MCP tool access should be restricted to authorized agents only
- Regular security audits of blacklist and credit data sources
- Rate limiting on API endpoints to prevent abuse

## 🚢 Deployment

### Docker Deployment

```bash
# Build images
docker-compose build

# Start services
docker-compose up -d
```

### Production Considerations

- Use environment-specific configuration files
- Implement proper logging and monitoring
- Set up health checks and auto-scaling
- Configure SSL/TLS certificates
- Implement database persistence for audit trails

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Backend: Follow PEP 8 guidelines
- Frontend: Use ESLint and Prettier configurations
- Write descriptive commit messages
- Include unit tests for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **LangGraph**: For the powerful workflow orchestration framework
- **FastMCP**: For the streamlined MCP server implementation
- **OpenAI**: For the language model capabilities
- **FastAPI**: For the high-performance web framework

## 📧 Contact

For questions or support, please open an issue on GitHub or contact the maintainers.

## 🗺️ Roadmap

### Upcoming Features

- [ ] Machine learning-based fraud detection
- [ ] Real-time dashboard for loan processing metrics
- [ ] Multi-language support
- [ ] Integration with additional external data sources
- [ ] Advanced analytics and reporting
- [ ] Mobile application
- [ ] Webhook support for third-party integrations

### Version History

- **v1.0.0** (Current): Initial release with core functionality
  - Multi-agent workflow
  - MCP integration
  - Basic fraud and risk assessment
  - React frontend

## 📚 Additional Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

---

**Built with ❤️ using LangGraph, FastMCP, and modern AI technologies**
