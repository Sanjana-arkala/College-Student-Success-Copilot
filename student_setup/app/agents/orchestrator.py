"""Ties the agents together: Planner -> MCP tools -> Analysis -> Policy -> Success -> Communication."""
from app.agents import planner
from app.agents.analysis import analyze_student
from app.agents.communication import draft_message
from app.agents.mcp_client import call_tool, mcp_session
from app.agents.policy import answer_policy
from app.agents.success import recommend
from app.audit.logger import audit


async def _analyze_one(session, student_id: str, trace: list):
    profile = await call_tool(session, "get_student", {"student_id": student_id}, trace)
    if "error" in profile:
        return None, profile["error"]  # AC-04: never invent a student
    att = await call_tool(session, "get_attendance", {"student_id": student_id}, trace)
    marks = await call_tool(session, "get_marks", {"student_id": student_id}, trace)
    prev = await call_tool(session, "get_previous_semester_results", {"student_id": student_id}, trace)
    asg = await call_tool(session, "get_assignments", {"student_id": student_id}, trace)
    profile.update({"previous_gpa": prev.get("previous_gpa", profile["previous_gpa"]),
                    "backlogs": prev.get("backlogs", profile["backlogs"])})
    return analyze_student(profile, att["attendance"], marks["marks"], asg["assignments"]), None


async def handle(message: str, user_role: str = "faculty") -> dict:
    trace: list[str] = ["Planner: classifying request"]
    plan = planner.make_plan(message)
    intent = plan.get("intent")
    audit("request", role=user_role, message=message, plan=plan)

    async with mcp_session() as session:
        if intent == "analyze_class":
            course, sem = plan.get("course") or "CSE", int(plan.get("semester") or 6)
            students = (await call_tool(session, "get_students", {"course": course, "semester": sem}, trace))["students"]
            results = []
            for s in students:
                analysis, _ = await _analyze_one(session, s["student_id"], trace)
                if analysis:
                    results.append(analysis)
            flagged = [r for r in results if r["needs_attention"]]
            trace.append("Academic Analysis Agent: applied configured rules")
            return {"intent": intent, "trace": trace,
                    "summary": f"{len(results)} students analyzed; {len(flagged)} need faculty attention.",
                    "flagged": flagged}

        if intent in {"student_report", "intervention_plan", "draft_message"}:
            sid = (plan.get("student_id") or "").upper()
            if not sid:
                return {"intent": intent, "trace": trace, "summary": "Please include a student ID (e.g. 2023CSE104)."}
            analysis, err = await _analyze_one(session, sid, trace)
            if err:
                return {"intent": intent, "trace": trace, "summary": f"{err}: {sid}"}
            if intent == "student_report":
                return {"intent": intent, "trace": trace, "analysis": analysis}
            if intent == "intervention_plan":
                pol = await call_tool(session, "search_college_policy", {"query": "academic support counseling remedial"}, trace)
                text = "\n".join(p["text"] for p in pol.get("passages", []))
                trace.append("Student Success Agent: recommendations (for faculty review)")
                return {"intent": intent, "trace": trace, "analysis": analysis, **recommend(analysis, text)}
            draft = draft_message(analysis)
            trace.append("Communication Agent: draft created, awaiting approval")
            return {"intent": intent, "trace": trace, "analysis": analysis, "draft": draft}

        result = await answer_policy(session, plan.get("query") or message, trace)
        trace.append("Policy Agent: answered from retrieved documents")
        return {"intent": "policy_question", "trace": trace, **result}
