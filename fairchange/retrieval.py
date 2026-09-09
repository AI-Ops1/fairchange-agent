"""Read-only Strands retrieval tools over one engagement fixture."""

from __future__ import annotations

from typing import Any

from strands import tool

from .domain import Engagement


def build_retrieval_tools(engagement: Engagement) -> list[Any]:
    @tool
    def get_scope(clause_ids: list[str] | None = None) -> dict[str, Any]:
        """Retrieve signed scope clauses. Pass clause IDs to narrow the result."""
        clauses = engagement.scope.clauses
        if clause_ids:
            clauses = tuple(item for item in clauses if item.id in clause_ids)
        return {
            "scope_version": engagement.scope.version,
            "source_id": engagement.scope.source_id,
            "clauses": [{"id": item.id, "text": item.text} for item in clauses],
        }

    @tool
    def search_correspondence(query: str) -> dict[str, Any]:
        """Search project correspondence by case-insensitive terms."""
        terms = [part.lower() for part in query.split() if part.strip()]
        matches = [
            item
            for item in engagement.correspondence
            if all(term in item.text.lower() for term in terms)
        ]
        return {
            "matches": [
                {"id": item.id, "sent_at": item.sent_at, "text": item.text}
                for item in matches
            ]
        }

    @tool
    def get_tasks(work_id: str | None = None) -> dict[str, Any]:
        """Retrieve existing delivery tasks, optionally filtered by work ID."""
        tasks = engagement.tasks
        if work_id:
            tasks = tuple(item for item in tasks if item.work_id == work_id)
        return {
            "tasks": [
                {
                    "id": item.id,
                    "work_id": item.work_id,
                    "status": item.status,
                    "scope_clause": item.scope_clause,
                }
                for item in tasks
            ]
        }

    return [get_scope, search_correspondence, get_tasks]
