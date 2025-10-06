#!/bin/bash

# VHACK Docker Profile Manager
# Usage: ./scripts/run-scenario.sh [scenario] [mode]
# Scenarios: research, creative, sysadmin, finance, medical
# Modes: cli, web (default: web)

set -e

SCENARIO=${1:-""}
MODE=${2:-"web"}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_help() {
    echo -e "${BLUE}VHACK Docker Profile Manager${NC}"
    echo ""
    echo "Usage: $0 [scenario] [mode]"
    echo ""
    echo -e "${YELLOW}Available scenarios:${NC}"
    echo "  research  - Information Disclosure vulnerabilities"
    echo "  creative  - Jailbreaking and prompt injection"
    echo "  sysadmin  - Command injection vulnerabilities"
    echo "  finance   - PII exposure and financial data leaks"
    echo "  medical   - HIPAA violations and health data"
    echo ""
    echo -e "${YELLOW}Available modes:${NC}"
    echo "  cli       - Command line interface"
    echo "  web       - Web interface (default)"
    echo ""
    echo -e "${YELLOW}Examples:${NC}"
    echo "  $0 research web    # Research scenario web interface (port 5001)"
    echo "  $0 creative cli    # Creative scenario CLI"
    echo "  $0 finance         # Finance scenario web interface (default)"
    echo ""
    echo -e "${YELLOW}Port mappings (web mode):${NC}"
    echo "  research: 5001"
    echo "  creative: 5002"
    echo "  sysadmin: 5003"
    echo "  finance:  5004"
    echo "  medical:  5005"
}

if [[ "$SCENARIO" == "" || "$SCENARIO" == "help" || "$SCENARIO" == "-h" || "$SCENARIO" == "--help" ]]; then
    show_help
    exit 0
fi

# Validate scenario
case $SCENARIO in
    research|creative|sysadmin|finance|medical)
        ;;
    *)
        echo -e "${RED}Error: Invalid scenario '$SCENARIO'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

# Validate mode
case $MODE in
    cli|web)
        ;;
    *)
        echo -e "${RED}Error: Invalid mode '$MODE'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac

# Build profile name
if [[ "$MODE" == "web" ]]; then
    PROFILE="${SCENARIO}-web"
    case $SCENARIO in
        research) PORT=5001 ;;
        creative) PORT=5002 ;;
        sysadmin) PORT=5003 ;;
        finance) PORT=5004 ;;
        medical) PORT=5005 ;;
    esac
else
    PROFILE="$SCENARIO"
    PORT="N/A (CLI mode)"
fi

echo -e "${GREEN}Starting VHACK ${SCENARIO} scenario in ${MODE} mode...${NC}"
if [[ "$MODE" == "web" ]]; then
    echo -e "${BLUE}Web interface will be available at: http://localhost:${PORT}${NC}"
fi
echo ""

# Check if .env exists
if [[ ! -f .env ]]; then
    echo -e "${YELLOW}Warning: .env file not found. Creating from example...${NC}"
    if [[ -f .env.example ]]; then
        cp .env.example .env
        echo -e "${YELLOW}Please edit .env with your OpenRouter API key before continuing.${NC}"
        echo "Press Enter to continue..."
        read
    fi
fi

# Run the profile
echo -e "${BLUE}Running: docker compose --profile ${PROFILE} up --build${NC}"
docker compose --profile "$PROFILE" up --build