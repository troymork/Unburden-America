# Unburden America n8n Integration Pack

This pack contains ready-to-import n8n workflows and nodes for the complete Unburden America agent system.

## 📋 Contents

### 🔄 Workflows
- **`main_campaign_workflow.json`** - Complete content creation pipeline with verification gates
- **`petition_workflow.json`** - Petition signature processing and certificate generation  
- **`error_handling_workflow.json`** - Automated error detection, healing, and escalation
- **`analytics_workflow.json`** - Daily analytics generation and strategy updates

### 🔌 Individual Agent Nodes
- Campaign Strategy Planner
- Content Production  
- Policy Fact-Check
- Compliance & Legal
- Narrative Development
- Visual Design
- Social Media Deployment
- And more...

### 📋 Templates
- Environment variable configuration
- Credential setup guides
- Import instructions

## 🚀 Quick Start

1. **Import Environment Variables**
   ```bash
   # Set these in your n8n instance
   AGENT_BASE_URL=https://your-agent-api.unburden-america.com
   WEBHOOK_BASE_URL=https://your-n8n-instance.com
   NOTIFICATION_EMAIL=alerts@unburden-america.com
   ```

2. **Import Workflows**
   - Import `error_handling_workflow.json` first
   - Then import other workflows as needed
   - Configure credentials (Bearer auth + SMTP)

3. **Activate & Test**
   - Start with error handling workflow
   - Test main campaign workflow with sample data
   - Verify webhook endpoints

## 🔍 Verification Gates

All workflows include multi-hop verification:
- **Policy Fact-Check Gate** - Validates claims against Tier A/B sources
- **Compliance Gate** - Ensures legal and platform compliance  
- **Safety Review** - Human-tone and safety validation
- **SRE Auto-Healing** - Automatic error detection and recovery

## 🎯 Key Features

- ✅ **Idempotent Operations** - Safe to re-run workflows
- 🔄 **Auto-Retry Logic** - Exponential backoff with jitter
- 📊 **Built-in Analytics** - KPI tracking and attribution
- 🚨 **Error Handling** - SRE-grade auto-healing and alerting
- 🔒 **Compliance** - Legal review gates and audit trails
- 📧 **Notifications** - Email alerts for key events

## 📖 Documentation

See `templates/import_instructions.md` for detailed setup steps.

Agent documentation: `../agents/00_shared_policies.md`
