# NBA Data Analytics Platform

## Overview
This project provides a comprehensive platform for collecting, analyzing, and visualizing NBA statistics. It features automated data collection, validation, and analysis tools.

## Features
- Automated NBA data collection
- Data validation and verification
- Statistical analysis tools
- RESTful API for data access
- Web-based visualization dashboard

## Project Structure
```
.
├── src/
│   ├── api/           # REST API implementation
│   ├── frontend/      # Web interface
│   ├── data_processing/  # Data processing scripts
│   └── utils/         # Utility functions
├── docs/
│   ├── api/          # API documentation
│   └── user_guide/   # User documentation
└── tests/
    ├── unit/        # Unit tests
    └── integration/ # Integration tests
```

## Setup
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Data Collection
The NBA data collector runs automatically every 10 minutes and performs:
- Player statistics collection
- Team data updates
- Game results processing

### Data Validation
Run the validation script to check data integrity:
```bash
python src/data_processing/data_validation.py
```

## Development
- Python 3.7+
- Uses nba_api for data collection
- FastAPI for REST endpoints
- React for frontend (planned)

## Contributing
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License
MIT License

## How We Work

We use a structured, agent-driven workflow to ensure quality, speed, and clarity:

- **Rules & Agents:** See `AGENTS.md` for our top-level rules, agent routing, and decision-making system.
- **Workplans:** Every feature or bugfix starts with a workplan in `docs/Plans/` (see `WorkplanTemplate.md`).
- **Documentation:** All requirements, architecture, UX/UI, and roadmap docs are in the project root or `docs/`.
- **CI/CD:** All PRs require a workplan and passing tests. Our CI checks for both.

**Key Docs:**
- Product: `PRODUCT_REQUIREMENTS.md`
- Architecture: `ARCHITECTURE.md`
- UX/UI: `UX_UI_PLAN.md`
- Roadmap: `PROJECT_OVERVIEW.md`
- Personas: `elite_persona_stack.md`
- Rules/Agents: `AGENTS.md`
- Workplans: `docs/Plans/`

**New to the project?**
- Start by reading `AGENTS.md` and `PRODUCT_REQUIREMENTS.md`.
- Use the workplan template for any new work.
- Ask questions early and often! 