"""
memory.py - Session memory and activity tracking for Carbon Coach.
Supports in-memory tracking with SQLite persistence for multi-turn conversational memory.
"""

import sqlite3
import datetime
from typing import List, Dict, Any, Optional
import os

DB_PATH = os.environ.get("CARBON_COACH_DB", "carbon_coach.db")


class CarbonMemory:
    """Manages conversational session logs and aggregate calculations."""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initializes tables if they do not exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    emissions_kg REAL NOT NULL,
                    details_json TEXT,
                    campus_group TEXT DEFAULT 'Hostel Cauvery',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS campus_groups (
                    name TEXT PRIMARY KEY,
                    category TEXT NOT NULL,
                    residents INTEGER NOT NULL,
                    total_emissions_kg REAL NOT NULL,
                    badge TEXT
                )
            """)
            conn.commit()
            self._seed_campus_leaderboard(cursor, conn)

    def _seed_campus_leaderboard(self, cursor, conn):
        """Seeds initial campus leaderboard data if empty."""
        cursor.execute("SELECT COUNT(*) FROM campus_groups")
        count = cursor.fetchone()[0]
        if count == 0:
            from carbon_coach.emission_factors import INITIAL_CAMPUS_LEADERBOARD
            for item in INITIAL_CAMPUS_LEADERBOARD:
                cursor.execute("""
                    INSERT INTO campus_groups (name, category, residents, total_emissions_kg, badge)
                    VALUES (?, ?, ?, ?, ?)
                """, (item["name"], item["category"], item["residents"], item["total_emissions_kg"], item["badge"]))
            conn.commit()

    def log_activity(
        self,
        category: str,
        description: str,
        emissions_kg: float,
        session_id: str = "default_user",
        campus_group: str = "Hostel Cauvery",
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Logs an activity into session memory and updates campus group score."""
        import json
        details_str = json.dumps(details or {})
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO activities (session_id, category, description, emissions_kg, details_json, campus_group, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, category, description, round(emissions_kg, 4), details_str, campus_group, now))
            activity_id = cursor.lastrowid

            # Update campus group totals
            cursor.execute("""
                UPDATE campus_groups
                SET total_emissions_kg = total_emissions_kg + ?
                WHERE name = ?
            """, (round(emissions_kg, 4), campus_group))
            conn.commit()

        return {
            "status": "success",
            "activity_id": activity_id,
            "session_id": session_id,
            "category": category,
            "description": description,
            "emissions_kg": round(emissions_kg, 4),
            "campus_group": campus_group,
            "timestamp": now,
        }

    def get_activities(self, session_id: str = "default_user", period: str = "all") -> List[Dict[str, Any]]:
        """Retrieves activities logged for a given session and time period."""
        query = "SELECT id, category, description, emissions_kg, details_json, campus_group, timestamp FROM activities WHERE session_id = ?"
        params: List[Any] = [session_id]

        now = datetime.datetime.now()
        if period.lower() in ("today", "daily"):
            start_date = now.strftime("%Y-%m-%d 00:00:00")
            query += " AND timestamp >= ?"
            params.append(start_date)
        elif period.lower() in ("week", "weekly", "7days"):
            start_date = (now - datetime.timedelta(days=7)).strftime("%Y-%m-%d 00:00:00")
            query += " AND timestamp >= ?"
            params.append(start_date)
        elif period.lower() in ("month", "monthly"):
            start_date = (now - datetime.timedelta(days=30)).strftime("%Y-%m-%d 00:00:00")
            query += " AND timestamp >= ?"
            params.append(start_date)

        query += " ORDER BY id DESC"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

        results = []
        for r in rows:
            results.append({
                "id": r[0],
                "category": r[1],
                "description": r[2],
                "emissions_kg": r[3],
                "details": r[4],
                "campus_group": r[5],
                "timestamp": r[6]
            })
        return results

    def get_summary(self, session_id: str = "default_user", period: str = "all") -> Dict[str, Any]:
        """Calculates total emissions, category breakdowns, and activity count."""
        activities = self.get_activities(session_id, period)

        total_emissions = sum(a["emissions_kg"] for a in activities)
        by_category: Dict[str, float] = {}

        for a in activities:
            cat = a["category"].lower()
            by_category[cat] = round(by_category.get(cat, 0.0) + a["emissions_kg"], 4)

        # Percentages
        percentages = {}
        if total_emissions > 0:
            for cat, val in by_category.items():
                percentages[cat] = round((val / total_emissions) * 100, 1)

        highest_category = max(by_category.items(), key=lambda x: x[1])[0] if by_category else "none"

        return {
            "session_id": session_id,
            "period": period,
            "activity_count": len(activities),
            "total_emissions_kg": round(total_emissions, 4),
            "by_category_kg": by_category,
            "percentages": percentages,
            "highest_category": highest_category,
            "recent_activities": activities[:5]  # most recent 5
        }

    def get_campus_leaderboard(self) -> List[Dict[str, Any]]:
        """Returns ranked campus hostels and departments by per capita emissions (lowest first)."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT name, category, residents, total_emissions_kg, badge
                FROM campus_groups
                ORDER BY (total_emissions_kg / residents) ASC
            """)
            rows = cursor.fetchall()

        leaderboard = []
        for idx, r in enumerate(rows, start=1):
            per_capita = round(r[3] / r[2], 2)
            leaderboard.append({
                "rank": idx,
                "name": r[0],
                "category": r[1],
                "residents": r[2],
                "total_emissions_kg": round(r[3], 1),
                "per_capita_kg": per_capita,
                "badge": r[4] or "🌱 Eco Supporter"
            })
        return leaderboard

    def add_chat_message(self, session_id: str, role: str, content: str):
        """Records a user or assistant message to maintain conversational context."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO chat_messages (session_id, role, content, timestamp)
                VALUES (?, ?, ?, ?)
            """, (session_id, role, content, now))
            conn.commit()

    def get_chat_history(self, session_id: str = "default_user", limit: int = 10) -> List[Dict[str, str]]:
        """Retrieves the recent conversation turns for context in follow-up queries."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT role, content FROM chat_messages
                WHERE session_id = ?
                ORDER BY id DESC LIMIT ?
            """, (session_id, limit))
            rows = cursor.fetchall()
        # Return in chronological order
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

    def clear_session(self, session_id: str = "default_user"):
        """Clears activity logs and chat history for a given session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM activities WHERE session_id = ?", (session_id,))
            cursor.execute("DELETE FROM chat_messages WHERE session_id = ?", (session_id,))
            conn.commit()


# Global singleton instance for easy import across tools
memory_store = CarbonMemory()
