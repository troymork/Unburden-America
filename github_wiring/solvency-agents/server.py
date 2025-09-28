from fastapi import FastAPI
from pydantic import BaseModel
import os

ROLE = os.getenv("ROLE","planner")

app = FastAPI(title=f"Solvency Agent — {ROLE}")

class GenericIn(BaseModel):
    text: str | None = None

@app.get("/health")
def health():
    return {"ok": True, "role": ROLE}

@app.post("/plan")
def plan(payload: GenericIn):
    if ROLE != "planner":
        return {"error":"wrong role","role":ROLE}
    return {"okr":{"objective":"Auto objective","key_results":[{"kr":"KR1","target":"1000"}]}}

@app.post("/bundle")
def bundle(payload: GenericIn):
    if ROLE != "producer":
        return {"error":"wrong role","role":ROLE}
    return {"bundle_type":"Explainer","assets":[{"name":"script.md","format":"md","content":"Intro… body… CTA"}]}

@app.post("/render")
def render(payload: GenericIn):
    if ROLE != "design":
        return {"error":"wrong role","role":ROLE}
    return {"pages":[{"template":"slide","elements":[{"type":"heading","text":"Lift the Burden… Fund the Future"}]}]}

@app.post("/schedule")
def schedule(payload: GenericIn):
    if ROLE != "social":
        return {"error":"wrong role","role":ROLE}
    return {"schedule":[{"platform":"x","datetime":"2025-10-01T10:00","copy":"Two economies… one fix.","assets":["/assets/graphic.png"]}]}

@app.post("/rollup")
def rollup(payload: GenericIn):
    if ROLE != "analytics":
        return {"error":"wrong role","role":ROLE}
    return {"okr_progress":[{"objective":"Awareness","kr":"Views","value":1234,"target":100000,"percent":1.23}]}

@app.post("/mint")
def mint(payload: GenericIn):
    if ROLE != "cert":
        return {"error":"wrong role","role":ROLE}
    return {"id":"ITEM-00000001","url":"https://example.org/ITEM-00000001.svg"}
