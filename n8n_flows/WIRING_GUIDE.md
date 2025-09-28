# Wiring Guide — replace placeholders in n8n
After deploying Cloud Run… capture each service URL and set them in your n8n HTTP Request nodes:

- Planner → https://<planner-url>/plan
- Producer → https://<producer-url>/bundle
- Design → https://<design-url>/render
- Compliance → https://<compliance-url>/check
- Web → https://<web-url>/commit  (use your existing web-agent if present… or GitHub Action)
- Social → https://<social-url>/schedule
- Analytics → https://<analytics-url>/rollup
- Cert → https://<cert-url>/mint

The new flows added:
- 11_onboarding_auto.json
- 12_morning_digest.json
- 13_compliance_gate.json
- 14_publish_pipeline.json
- 15_fundraising_funnel.json
- 16_cloud_run_healthcheck.json
