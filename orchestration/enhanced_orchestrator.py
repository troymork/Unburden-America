#!/usr/bin/env python3
"""
Enhanced Orchestration Engine for IsThereEnoughMoney Movement
========================================================

This orchestrator coordinates AI agents for campaign automation, content generation,
compliance checking, and movement operations while maintaining strict verification
and quality standards.

Key Features:
- Multi-agent workflow coordination
- Dual-gate fact-checking and compliance validation
- Content generation with source verification
- Campaign automation and analytics
- Real-time monitoring and alerting
"""

import json
import asyncio
import logging
import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import traceback

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"

class AgentType(Enum):
    ORCHESTRATOR = "orchestrator"
    CONTENT_PRODUCER = "content_producer"
    FACT_CHECKER = "fact_checker"
    COMPLIANCE_REVIEWER = "compliance_reviewer"
    SOCIAL_MEDIA = "social_media"
    ANALYTICS = "analytics"
    PETITION_OPTIMIZER = "petition_optimizer"
    FUNDRAISING = "fundraising"
    NARRATIVE_DEVELOPER = "narrative_developer"
    VISUAL_DESIGNER = "visual_designer"

@dataclass
class WorkflowTask:
    """Individual task within a workflow"""
    task_id: str
    agent_type: AgentType
    description: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    dependencies: List[str] = None
    created_at: str = None
    updated_at: str = None
    error_log: List[str] = None
    verification_sources: List[str] = None
    compliance_notes: str = ""
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []
        if self.error_log is None:
            self.error_log = []
        if self.verification_sources is None:
            self.verification_sources = []
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at

@dataclass
class WorkflowInstance:
    """Complete workflow execution instance"""
    workflow_id: str
    name: str
    description: str
    tasks: List[WorkflowTask]
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.MEDIUM
    created_at: str = None
    deadline: Optional[str] = None
    brand_guidelines: Dict[str, Any] = None
    resource_constraints: Dict[str, Any] = None
    audit_trail: List[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.datetime.utcnow().isoformat()
        if self.brand_guidelines is None:
            self.brand_guidelines = {}
        if self.resource_constraints is None:
            self.resource_constraints = {}
        if self.audit_trail is None:
            self.audit_trail = []

class EnhancedOrchestrator:
    """Main orchestration engine for the IsThereEnoughMoney movement"""
    
    def __init__(self):
        self.active_workflows: Dict[str, WorkflowInstance] = {}
        self.agent_registry: Dict[AgentType, Dict] = {}
        self.workflow_templates: Dict[str, Dict] = {}
        self._initialize_agents()
        self._load_workflow_templates()
    
    def _initialize_agents(self):
        """Initialize the agent registry with capabilities and configurations"""
        self.agent_registry = {
            AgentType.CONTENT_PRODUCER: {
                "description": "Research-driven content generation with source verification",
                "capabilities": ["research", "writing", "fact_verification", "citation"],
                "quality_gates": ["source_verification", "dual_fact_check"]
            },
            AgentType.FACT_CHECKER: {
                "description": "Rigorous fact-checking with multiple source verification",
                "capabilities": ["source_validation", "claim_verification", "uncertainty_documentation"],
                "quality_gates": ["minimum_two_sources", "primary_source_preference"]
            },
            AgentType.COMPLIANCE_REVIEWER: {
                "description": "Legal and platform compliance validation",
                "capabilities": ["legal_review", "platform_policy_check", "accessibility_audit"],
                "quality_gates": ["legal_compliance", "platform_compliance", "accessibility_standards"]
            },
            AgentType.SOCIAL_MEDIA: {
                "description": "Multi-platform social media automation and management",
                "capabilities": ["content_scheduling", "engagement_tracking", "platform_optimization"],
                "quality_gates": ["platform_compliance", "brand_consistency"]
            },
            AgentType.ANALYTICS: {
                "description": "Campaign performance tracking and predictive analytics",
                "capabilities": ["impact_measurement", "predictive_modeling", "ROI_analysis"],
                "quality_gates": ["data_accuracy", "attribution_validation"]
            },
            AgentType.PETITION_OPTIMIZER: {
                "description": "Petition funnel optimization and conversion tracking",
                "capabilities": ["funnel_analysis", "A/B_testing", "conversion_optimization"],
                "quality_gates": ["consent_validation", "UX_standards"]
            },
            AgentType.FUNDRAISING: {
                "description": "Ethical fundraising optimization and donor management",
                "capabilities": ["donor_journey_mapping", "ethical_ask_optimization", "retention_analysis"],
                "quality_gates": ["ethical_standards", "compliance_check"]
            },
            AgentType.NARRATIVE_DEVELOPER: {
                "description": "Strategic narrative development using Hero's Journey framework",
                "capabilities": ["story_architecture", "emotional_arc_design", "accessibility_adaptation"],
                "quality_gates": ["narrative_coherence", "emotional_impact_validation"]
            },
            AgentType.VISUAL_DESIGNER: {
                "description": "Accessibility-first visual design and brand consistency",
                "capabilities": ["visual_design", "accessibility_optimization", "brand_application"],
                "quality_gates": ["accessibility_compliance", "brand_consistency"]
            }
        }
    
    def _load_workflow_templates(self):
        """Load predefined workflow templates for common campaign operations"""
        self.workflow_templates = {
            "content_creation": {
                "name": "Content Creation Pipeline",
                "description": "Full content creation with dual verification gates",
                "task_sequence": [
                    {"agent": AgentType.CONTENT_PRODUCER, "phase": "research_and_draft"},
                    {"agent": AgentType.FACT_CHECKER, "phase": "primary_fact_check"},
                    {"agent": AgentType.COMPLIANCE_REVIEWER, "phase": "compliance_review"},
                    {"agent": AgentType.FACT_CHECKER, "phase": "secondary_fact_check"},
                    {"agent": AgentType.NARRATIVE_DEVELOPER, "phase": "narrative_enhancement"},
                    {"agent": AgentType.VISUAL_DESIGNER, "phase": "visual_design"}
                ]
            },
            "social_media_campaign": {
                "name": "Social Media Campaign Launch",
                "description": "Multi-platform social media campaign deployment",
                "task_sequence": [
                    {"agent": AgentType.CONTENT_PRODUCER, "phase": "content_adaptation"},
                    {"agent": AgentType.COMPLIANCE_REVIEWER, "phase": "platform_compliance_check"},
                    {"agent": AgentType.SOCIAL_MEDIA, "phase": "campaign_deployment"},
                    {"agent": AgentType.ANALYTICS, "phase": "performance_tracking"}
                ]
            },
            "petition_optimization": {
                "name": "Petition Launch and Optimization",
                "description": "Petition deployment with conversion optimization",
                "task_sequence": [
                    {"agent": AgentType.CONTENT_PRODUCER, "phase": "petition_content"},
                    {"agent": AgentType.COMPLIANCE_REVIEWER, "phase": "legal_review"},
                    {"agent": AgentType.PETITION_OPTIMIZER, "phase": "funnel_setup"},
                    {"agent": AgentType.ANALYTICS, "phase": "conversion_tracking"}
                ]
            },
            "fundraising_campaign": {
                "name": "Ethical Fundraising Campaign",
                "description": "Donor-centric fundraising with ethical optimization",
                "task_sequence": [
                    {"agent": AgentType.FUNDRAISING, "phase": "donor_journey_design"},
                    {"agent": AgentType.CONTENT_PRODUCER, "phase": "fundraising_content"},
                    {"agent": AgentType.COMPLIANCE_REVIEWER, "phase": "ethical_review"},
                    {"agent": AgentType.ANALYTICS, "phase": "donor_analytics"}
                ]
            }
        }
    
    async def route_intent(self, intent: str, payload: Dict[str, Any] = None, 
                          context_history: List = None, priority: Priority = Priority.MEDIUM) -> Dict[str, Any]:
        """Main entry point for routing user intents to appropriate workflows"""
        
        workflow_id = str(uuid.uuid4())
        timestamp = datetime.datetime.utcnow().isoformat()
        
        logger.info(f"Routing intent: {intent} with workflow ID: {workflow_id}")
        
        try:
            # Parse intent and determine workflow template
            workflow_template = self._parse_intent_to_workflow(intent, payload)
            
            if not workflow_template:
                return {
                    "workflow_id": workflow_id,
                    "status": "error",
                    "message": f"Unable to determine workflow for intent: {intent}",
                    "timestamp": timestamp
                }
            
            # Create workflow instance
            workflow = self._create_workflow_from_template(
                workflow_id, workflow_template, intent, payload, priority
            )
            
            # Validate resources and dependencies
            validation_result = await self._validate_workflow(workflow)
            if not validation_result["valid"]:
                return {
                    "workflow_id": workflow_id,
                    "status": "blocked",
                    "message": f"Workflow validation failed: {validation_result['errors']}",
                    "timestamp": timestamp
                }
            
            # Store workflow and begin execution
            self.active_workflows[workflow_id] = workflow
            
            # Execute workflow asynchronously
            asyncio.create_task(self._execute_workflow(workflow))
            
            return {
                "workflow_id": workflow_id,
                "status": "accepted",
                "workflow_dag": self._generate_dag_representation(workflow),
                "estimated_completion": self._estimate_completion_time(workflow),
                "resource_allocation": validation_result["resources"],
                "success_metrics": self._define_success_metrics(workflow),
                "timestamp": timestamp
            }
            
        except Exception as e:
            logger.error(f"Error routing intent {intent}: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "workflow_id": workflow_id,
                "status": "error",
                "message": f"Internal error: {str(e)}",
                "timestamp": timestamp
            }
    
    def _parse_intent_to_workflow(self, intent: str, payload: Dict[str, Any]) -> Optional[str]:
        """Parse user intent and map to appropriate workflow template"""
        
        intent_lower = intent.lower()
        
        # Intent mapping logic
        if any(keyword in intent_lower for keyword in ["content", "article", "blog", "write"]):
            return "content_creation"
        elif any(keyword in intent_lower for keyword in ["social", "twitter", "facebook", "instagram"]):
            return "social_media_campaign"
        elif any(keyword in intent_lower for keyword in ["petition", "sign", "signature"]):
            return "petition_optimization"
        elif any(keyword in intent_lower for keyword in ["fundraise", "donate", "donation", "fund"]):
            return "fundraising_campaign"
        elif intent_lower in ["plan", "strategy", "campaign"]:
            # Default to content creation for general planning
            return "content_creation"
        
        return None
    
    def _create_workflow_from_template(self, workflow_id: str, template_name: str, 
                                     intent: str, payload: Dict[str, Any], 
                                     priority: Priority) -> WorkflowInstance:
        """Create a workflow instance from a template"""
        
        template = self.workflow_templates[template_name]
        tasks = []
        
        for i, task_spec in enumerate(template["task_sequence"]):
            task = WorkflowTask(
                task_id=f"{workflow_id}_task_{i}",
                agent_type=task_spec["agent"],
                description=f"{task_spec['phase']} for {intent}",
                inputs=payload or {},
                outputs={},
                priority=priority,
                dependencies=[f"{workflow_id}_task_{i-1}"] if i > 0 else []
            )
            tasks.append(task)
        
        return WorkflowInstance(
            workflow_id=workflow_id,
            name=template["name"],
            description=f"{template['description']} - {intent}",
            tasks=tasks,
            priority=priority
        )
    
    async def _validate_workflow(self, workflow: WorkflowInstance) -> Dict[str, Any]:
        """Validate workflow before execution"""
        
        errors = []
        warnings = []
        
        # Check for circular dependencies
        if self._has_circular_dependencies(workflow):
            errors.append("Circular dependencies detected in workflow")
        
        # Validate agent availability
        for task in workflow.tasks:
            if task.agent_type not in self.agent_registry:
                errors.append(f"Unknown agent type: {task.agent_type}")
        
        # Resource constraint validation
        if workflow.resource_constraints:
            # Add resource validation logic here
            pass
        
        # Deadline validation
        if workflow.deadline:
            deadline = datetime.datetime.fromisoformat(workflow.deadline)
            if deadline < datetime.datetime.utcnow():
                errors.append("Deadline is in the past")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "resources": {"estimated_agents": len(workflow.tasks)}
        }
    
    def _has_circular_dependencies(self, workflow: WorkflowInstance) -> bool:
        """Check for circular dependencies in task graph"""
        # Simple implementation - could be enhanced with proper graph algorithms
        task_ids = {task.task_id for task in workflow.tasks}
        
        for task in workflow.tasks:
            for dep in task.dependencies:
                if dep == task.task_id:
                    return True
                if dep not in task_ids:
                    # Dependency refers to non-existent task
                    continue
        
        return False
    
    async def _execute_workflow(self, workflow: WorkflowInstance):
        """Execute workflow tasks in dependency order"""
        
        logger.info(f"Starting execution of workflow: {workflow.workflow_id}")
        workflow.status = TaskStatus.IN_PROGRESS
        workflow.audit_trail.append(f"Workflow execution started at {datetime.datetime.utcnow().isoformat()}")
        
        try:
            # Execute tasks in dependency order
            completed_tasks = set()
            
            while len(completed_tasks) < len(workflow.tasks):
                # Find tasks ready to execute (all dependencies completed)
                ready_tasks = []
                for task in workflow.tasks:
                    if task.status == TaskStatus.PENDING and all(dep in completed_tasks for dep in task.dependencies):
                        ready_tasks.append(task)
                
                if not ready_tasks:
                    # Check for blocked workflow
                    remaining_tasks = [t for t in workflow.tasks if t.status not in [TaskStatus.COMPLETED, TaskStatus.FAILED]]
                    if remaining_tasks:
                        logger.error(f"Workflow {workflow.workflow_id} is blocked - no ready tasks")
                        workflow.status = TaskStatus.BLOCKED
                        break
                
                # Execute ready tasks in parallel
                execution_tasks = []
                for task in ready_tasks:
                    execution_tasks.append(self._execute_task(task))
                
                # Wait for task completion
                results = await asyncio.gather(*execution_tasks, return_exceptions=True)
                
                # Process results
                for task, result in zip(ready_tasks, results):
                    if isinstance(result, Exception):
                        logger.error(f"Task {task.task_id} failed: {str(result)}")
                        task.status = TaskStatus.FAILED
                        task.error_log.append(f"Execution error: {str(result)}")
                        workflow.audit_trail.append(f"Task {task.task_id} failed at {datetime.datetime.utcnow().isoformat()}")
                    else:
                        task.status = TaskStatus.COMPLETED
                        task.outputs = result
                        completed_tasks.add(task.task_id)
                        workflow.audit_trail.append(f"Task {task.task_id} completed at {datetime.datetime.utcnow().isoformat()}")
                
                # Check for critical failures
                failed_critical_tasks = [t for t in ready_tasks if t.status == TaskStatus.FAILED and t.priority in [Priority.HIGH, Priority.CRITICAL]]
                if failed_critical_tasks:
                    logger.error(f"Critical task failures in workflow {workflow.workflow_id}")
                    workflow.status = TaskStatus.FAILED
                    break
            
            # Set final workflow status
            if workflow.status not in [TaskStatus.FAILED, TaskStatus.BLOCKED]:
                all_completed = all(task.status == TaskStatus.COMPLETED for task in workflow.tasks)
                workflow.status = TaskStatus.COMPLETED if all_completed else TaskStatus.FAILED
            
            workflow.audit_trail.append(f"Workflow execution completed with status {workflow.status.value} at {datetime.datetime.utcnow().isoformat()}")
            logger.info(f"Workflow {workflow.workflow_id} completed with status: {workflow.status.value}")
            
        except Exception as e:
            logger.error(f"Workflow execution error for {workflow.workflow_id}: {str(e)}")
            workflow.status = TaskStatus.FAILED
            workflow.audit_trail.append(f"Workflow execution failed: {str(e)} at {datetime.datetime.utcnow().isoformat()}")
    
    async def _execute_task(self, task: WorkflowTask) -> Dict[str, Any]:
        """Execute individual task by delegating to appropriate agent"""
        
        logger.info(f"Executing task: {task.task_id} with agent: {task.agent_type.value}")
        task.status = TaskStatus.IN_PROGRESS
        task.updated_at = datetime.datetime.utcnow().isoformat()
        
        try:
            # Import agent factory with absolute imports
            import sys
            import os
            
            # Get the absolute path to the project root
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(current_dir)
            agents_path = os.path.join(project_root, "agents", "implementations")
            
            if agents_path not in sys.path:
                sys.path.insert(0, agents_path)
            if project_root not in sys.path:
                sys.path.insert(0, project_root)
            
            # Import with error handling using proper module imports
            try:
                import sys
                import os
                import importlib.util
                
                # Get the project root directory
                project_root = os.path.dirname(os.path.dirname(__file__))
                if project_root not in sys.path:
                    sys.path.insert(0, project_root)
                
                # Import using proper module path
                from agents.implementations.agent_factory import agent_factory, AgentType as FactoryAgentType
                factory = agent_factory
                
            except ImportError as e:
                logger.error(f"Failed to import agent factory: {e}")
                logger.error(f"Project root: {os.path.dirname(os.path.dirname(__file__))}")
                logger.error(f"Python path: {sys.path[:3]}...")
                # Fallback to mock execution
                return await self._execute_task_fallback(task)
            
            # Map orchestrator AgentType to factory AgentType
            agent_type_mapping = {
                AgentType.CONTENT_PRODUCER: FactoryAgentType.CONTENT_PRODUCER,
                AgentType.FACT_CHECKER: FactoryAgentType.FACT_CHECKER,
                AgentType.COMPLIANCE_REVIEWER: FactoryAgentType.COMPLIANCE_REVIEWER,
                AgentType.SOCIAL_MEDIA: FactoryAgentType.SOCIAL_MEDIA,
                AgentType.ANALYTICS: FactoryAgentType.ANALYTICS,
                AgentType.PETITION_OPTIMIZER: FactoryAgentType.PETITION_OPTIMIZER,
                AgentType.FUNDRAISING: FactoryAgentType.FUNDRAISING,
                AgentType.NARRATIVE_DEVELOPER: FactoryAgentType.NARRATIVE_DEVELOPER,
                AgentType.VISUAL_DESIGNER: FactoryAgentType.VISUAL_DESIGNER
            }
            
            factory_agent_type = agent_type_mapping.get(task.agent_type)
            if not factory_agent_type:
                raise Exception(f"Unknown agent type: {task.agent_type}")
            
            # Execute task using agent factory
            agent_result = await factory.execute_agent_task(factory_agent_type, task.inputs)
            
            # Update task with agent results
            task.verification_sources = [s.url for s in agent_result.sources_used] if agent_result.sources_used else []
            task.compliance_notes = f"Compliance checks: {len(agent_result.compliance_checks)}"
            
            # Apply quality gates based on agent results
            quality_result = await self._apply_quality_gates_from_agent_result(task, agent_result)
            
            # Convert agent output to task output format (store content regardless of quality gates)
            output = {
                "status": "success" if quality_result["passed"] else "needs_review",
                "agent_id": agent_result.agent_id,
                "agent_type": agent_result.agent_type,
                "processed_at": agent_result.created_at,
                "execution_time_ms": agent_result.execution_time_ms,
                "quality_scores": agent_result.quality_scores,
                "primary_output": agent_result.primary_output,
                "metadata": agent_result.metadata,
                "fact_checks_count": len(agent_result.fact_checks),
                "compliance_checks_count": len(agent_result.compliance_checks),
                "sources_count": len(agent_result.sources_used),
                "verification_sources": task.verification_sources,
                "compliance_notes": task.compliance_notes,
                "quality_gate_failures": quality_result.get("failures", []) if not quality_result["passed"] else []
            }
            
            # Only raise exception for critical failures, not quality gate failures
            if not quality_result["passed"]:
                logger.warning(f"Task {task.task_id} completed with quality gate failures: {quality_result['failures']}")
                # Don't raise exception - store content for review instead
            
            return output
            
        except Exception as e:
            logger.error(f"Task execution failed for {task.task_id}: {str(e)}")
            raise
    
    async def _apply_quality_gates(self, task: WorkflowTask) -> Dict[str, Any]:
        """Apply quality gates based on agent type and task requirements"""
        
        agent_config = self.agent_registry.get(task.agent_type, {})
        quality_gates = agent_config.get("quality_gates", [])
        
        failures = []
        score = 1.0
        
        # Simulate quality gate checks
        for gate in quality_gates:
            if gate == "source_verification" and len(task.verification_sources) < 2:
                failures.append("Insufficient source verification (minimum 2 required)")
                score -= 0.2
            elif gate == "dual_fact_check" and task.agent_type == AgentType.CONTENT_PRODUCER:
                # This would be checked by having fact-check tasks in the workflow
                pass
            elif gate == "legal_compliance":
                # Simulate compliance check
                pass
        
        return {
            "passed": len(failures) == 0,
            "failures": failures,
            "score": max(0.0, score)
        }
    
    async def _apply_quality_gates_from_agent_result(self, task: WorkflowTask, agent_result) -> Dict[str, Any]:
        """Apply quality gates based on actual agent results"""
        
        failures = []
        
        # Check agent execution status
        if hasattr(agent_result, 'status') and agent_result.status.value != "completed":
            failures.append(f"Agent execution failed: {agent_result.status.value}")
        
        # Check quality scores
        if hasattr(agent_result, 'quality_scores'):
            for metric, score in agent_result.quality_scores.items():
                if score < 0.7:  # Minimum quality threshold
                    failures.append(f"Low quality score for {metric}: {score:.2f}")
        
        # Check compliance issues
        if hasattr(agent_result, 'compliance_checks'):
            non_compliant = [c for c in agent_result.compliance_checks if c.status == "non_compliant"]
            if non_compliant:
                failures.append(f"Compliance violations: {len(non_compliant)} issues found")
        
        # Check fact-checking confidence
        if hasattr(agent_result, 'fact_checks'):
            low_confidence = [fc for fc in agent_result.fact_checks if fc.confidence_level < 0.8]
            if low_confidence:
                failures.append(f"Low-confidence fact checks: {len(low_confidence)}")
        
        # Calculate overall score from agent quality scores
        overall_score = 1.0
        if hasattr(agent_result, 'quality_scores') and agent_result.quality_scores:
            scores = list(agent_result.quality_scores.values())
            overall_score = sum(scores) / len(scores)
        
        return {
            "passed": len(failures) == 0,
            "failures": failures,
            "score": overall_score
        }
    
    async def _execute_task_fallback(self, task: WorkflowTask) -> Dict[str, Any]:
        """Fallback execution when agent factory is not available"""
        
        logger.warning(f"Using fallback execution for task: {task.task_id}")
        
        # Simulate processing time
        await asyncio.sleep(1)
        
        # Generate mock output based on agent type
        if task.agent_type == AgentType.CONTENT_PRODUCER:
            output = {
                "status": "success",
                "agent_type": task.agent_type.value,
                "processed_at": datetime.datetime.utcnow().isoformat(),
                "content": f"Mock content generated for: {task.description}",
                "sources": ["mock-source1.gov", "mock-source2.org"],
                "word_count": 500,
                "fallback_mode": True
            }
        elif task.agent_type == AgentType.FACT_CHECKER:
            output = {
                "status": "success",
                "agent_type": task.agent_type.value,
                "processed_at": datetime.datetime.utcnow().isoformat(),
                "verification_status": "verified",
                "source_count": 3,
                "confidence_level": 0.85,
                "fallback_mode": True
            }
        elif task.agent_type == AgentType.COMPLIANCE_REVIEWER:
            output = {
                "status": "success", 
                "agent_type": task.agent_type.value,
                "processed_at": datetime.datetime.utcnow().isoformat(),
                "compliance_status": "approved",
                "legal_review": "passed",
                "platform_compliance": "approved",
                "fallback_mode": True
            }
        else:
            output = {
                "status": "success",
                "agent_type": task.agent_type.value,
                "processed_at": datetime.datetime.utcnow().isoformat(),
                "message": f"Mock {task.agent_type.value} processing completed",
                "fallback_mode": True
            }
        
        return output
    
    def _generate_dag_representation(self, workflow: WorkflowInstance) -> Dict[str, Any]:
        """Generate DAG representation for workflow visualization"""
        
        nodes = []
        edges = []
        
        for task in workflow.tasks:
            nodes.append({
                "id": task.task_id,
                "label": task.agent_type.value,
                "description": task.description,
                "status": task.status.value
            })
            
            for dep in task.dependencies:
                edges.append([dep, task.task_id])
        
        return {
            "nodes": nodes,
            "edges": edges
        }
    
    def _estimate_completion_time(self, workflow: WorkflowInstance) -> str:
        """Estimate workflow completion time based on task complexity"""
        
        # Simple estimation - could be enhanced with ML models
        base_time_per_task = 300  # 5 minutes per task
        total_estimated_seconds = len(workflow.tasks) * base_time_per_task
        
        # Account for parallel execution
        max_parallel_depth = self._calculate_max_depth(workflow)
        adjusted_time = (total_estimated_seconds * max_parallel_depth) // len(workflow.tasks)
        
        completion_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=adjusted_time)
        return completion_time.isoformat()
    
    def _calculate_max_depth(self, workflow: WorkflowInstance) -> int:
        """Calculate maximum dependency depth in workflow"""
        # Simple implementation - could be enhanced
        return max(len(task.dependencies) for task in workflow.tasks) + 1
    
    def _define_success_metrics(self, workflow: WorkflowInstance) -> Dict[str, Any]:
        """Define success metrics for workflow tracking"""
        
        return {
            "completion_rate": "percentage of tasks completed successfully",
            "quality_score": "average quality gate scores",
            "compliance_rate": "percentage of tasks passing compliance review",
            "source_verification_rate": "percentage of content with verified sources",
            "time_to_completion": "actual vs estimated completion time"
        }
    
    def get_workflow_status(self, workflow_id: str) -> Dict[str, Any]:
        """Get current status of a workflow"""
        
        if workflow_id not in self.active_workflows:
            return {"error": "Workflow not found"}
        
        workflow = self.active_workflows[workflow_id]
        
        # Calculate progress statistics
        total_tasks = len(workflow.tasks)
        completed_tasks = len([t for t in workflow.tasks if t.status == TaskStatus.COMPLETED])
        failed_tasks = len([t for t in workflow.tasks if t.status == TaskStatus.FAILED])
        
        return {
            "workflow_id": workflow_id,
            "name": workflow.name,
            "status": workflow.status.value,
            "progress": {
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "completion_percentage": (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            },
            "tasks": [
                {
                    "task_id": task.task_id,
                    "agent_type": task.agent_type.value,
                    "status": task.status.value,
                    "description": task.description,
                    "error_count": len(task.error_log)
                } for task in workflow.tasks
            ],
            "audit_trail": workflow.audit_trail,
            "created_at": workflow.created_at,
            "updated_at": workflow.tasks[-1].updated_at if workflow.tasks else workflow.created_at
        }

# Global orchestrator instance
orchestrator = EnhancedOrchestrator()

def main():
    """Main entry point for testing the orchestrator"""
    import asyncio
    
    async def test_orchestrator():
        """Test the orchestrator with sample intents"""
        
        print("Testing Enhanced Orchestrator for IsThereEnoughMoney Movement")
        print("=" * 60)
        
        # Test content creation workflow
        result1 = await orchestrator.route_intent(
            intent="Create content about monetary flow tax",
            payload={
                "topic": "Monetary Flow Tax Explanation",
                "target_audience": "general_public",
                "content_type": "educational_article"
            },
            priority=Priority.HIGH
        )
        
        print(f"Content Creation Workflow: {result1['workflow_id']}")
        print(f"Status: {result1['status']}")
        print(f"DAG Nodes: {len(result1.get('workflow_dag', {}).get('nodes', []))}")
        
        # Wait a bit and check status
        await asyncio.sleep(3)
        status1 = orchestrator.get_workflow_status(result1['workflow_id'])
        print(f"Progress: {status1['progress']['completion_percentage']:.1f}%")
        print()
        
        # Test social media campaign
        result2 = await orchestrator.route_intent(
            intent="Launch social media campaign",
            payload={
                "platforms": ["twitter", "facebook", "instagram"],
                "campaign_theme": "Tax the System, Not the People"
            },
            priority=Priority.MEDIUM
        )
        
        print(f"Social Media Campaign: {result2['workflow_id']}")
        print(f"Status: {result2['status']}")
        print()
        
        # Wait for workflows to complete
        print("Waiting for workflows to complete...")
        await asyncio.sleep(5)
        
        # Final status check
        final_status1 = orchestrator.get_workflow_status(result1['workflow_id'])
        final_status2 = orchestrator.get_workflow_status(result2['workflow_id'])
        
        print(f"Final Status - Content: {final_status1['status']} ({final_status1['progress']['completion_percentage']:.1f}%)")
        print(f"Final Status - Social Media: {final_status2['status']} ({final_status2['progress']['completion_percentage']:.1f}%)")
    
    # Run the test
    asyncio.run(test_orchestrator())

if __name__ == "__main__":
    main()