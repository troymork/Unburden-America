# n8n Import Instructions

## Prerequisites
1. n8n instance running (local or cloud)
2. Agent API endpoints deployed and accessible
3. SMTP email configuration for notifications

## Setup Steps

### 1. Environment Variables
Import the environment variables from `templates/environment_variables.json`:
- Go to Settings > Environment Variables in n8n
- Add the variables with your actual URLs and configuration

### 2. Credentials
Set up the required credentials:
- **Agent API Bearer Token**: Your API authentication token
- **SMTP Email**: Your email service configuration

### 3. Import Workflows
Import workflows in this order:
1. `workflows/error_handling_workflow.json` (foundational error handling)
2. `workflows/main_campaign_workflow.json` (primary content pipeline)
3. `workflows/petition_workflow.json` (petition processing)
4. `workflows/analytics_workflow.json` (daily reporting)

### 4. Import Individual Nodes (Optional)
Individual agent nodes in `nodes/` can be imported for custom workflow building.

### 5. Activate Workflows
- Start with `error_handling_workflow` (always active)
- Activate `analytics_workflow` for daily reports
- Activate `petition_workflow` for live petition processing
- Activate `main_campaign_workflow` for content creation

## Testing
1. Test error handling workflow first
2. Run main campaign workflow with sample data
3. Verify webhook endpoints are accessible
4. Check email notifications are working

## Monitoring
- Monitor workflow execution logs
- Set up alerting for failed executions
- Review daily analytics reports
- Check SRE auto-healing actions
