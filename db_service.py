import json
import os
from supabase import create_client, Client


class NovelDatabaseService:
    """
    Service for managing novel data in a Supabase (PostgreSQL) database.
    Handles CRUD operations for novels, chapter outlines, scenes, formats, and series.
    """
    _client: Client = None

    @classmethod
    def _get_client(cls) -> Client:
        if cls._client is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_SERVICE_KEY")
            if not url or not key:
                raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY environment variables are required")
            cls._client = create_client(url, key)
        return cls._client

    # ── Novels ────────────────────────────────────────────────────────────────

    @classmethod
    def list_novels(cls):
        """List all saved novels"""
        try:
            db = cls._get_client()
            resp = db.table("novels").select("id, title, created_at").order("created_at", desc=True).execute()
            return resp.data or []
        except Exception as e:
            print(f"Database error listing novels: {e}")
            return []

    @classmethod
    def create_novel(cls, title, model, max_scene_length, min_scene_length, series_id=None, book_number=None):
        """
        Create a new novel entry.

        Returns:
            int: The ID of the created novel
        """
        try:
            db = cls._get_client()
            payload = {
                "title": title,
                "model": model,
                "max_scene_length": max_scene_length,
                "min_scene_length": min_scene_length,
            }
            if series_id:
                payload["series_id"] = series_id
            if book_number:
                payload["book_number"] = book_number

            resp = db.table("novels").insert(payload).execute()
            return resp.data[0]["id"]
        except Exception as e:
            print(f"Database error creating novel: {e}")
            return None

    @classmethod
    def get_novel(cls, novel_id):
        """Get a novel by ID"""
        try:
            db = cls._get_client()
            resp = db.table("novels").select("*").eq("id", novel_id).execute()
            if resp.data:
                novel = resp.data[0]
                if novel.get("story_details"):
                    try:
                        novel["story_details"] = json.loads(novel["story_details"])
                    except (json.JSONDecodeError, TypeError):
                        pass
                return novel
            return None
        except Exception as e:
            print(f"Database error getting novel: {e}")
            return None

    @classmethod
    def delete_novel(cls, novel_id):
        """Delete a novel and all related data"""
        try:
            db = cls._get_client()
            db.table("novels").delete().eq("id", novel_id).execute()
            return True
        except Exception as e:
            print(f"Database error deleting novel: {e}")
            return False

    @classmethod
    def save_story_details(cls, novel_id, story_details):
        """Save or update story details for a novel"""
        try:
            db = cls._get_client()
            db.table("novels").update({"story_details": json.dumps(story_details)}).eq("id", novel_id).execute()
            return True
        except Exception as e:
            print(f"Database error saving story details: {e}")
            return False

    # ── Series ────────────────────────────────────────────────────────────────

    @classmethod
    def create_series(cls, title, description=None, num_books=1):
        """
        Create a new series.

        Returns:
            int: The ID of the created series
        """
        try:
            db = cls._get_client()
            payload = {"title": title, "num_books": num_books}
            if description:
                payload["description"] = description
            resp = db.table("series").insert(payload).execute()
            return resp.data[0]["id"]
        except Exception as e:
            print(f"Database error creating series: {e}")
            return None

    @classmethod
    def get_series(cls, series_id):
        """Get a series by ID"""
        try:
            db = cls._get_client()
            resp = db.table("series").select("*").eq("id", series_id).execute()
            return resp.data[0] if resp.data else None
        except Exception as e:
            print(f"Database error getting series: {e}")
            return None

    @classmethod
    def list_series(cls):
        """List all series"""
        try:
            db = cls._get_client()
            resp = db.table("series").select("id, title, num_books, created_at").order("created_at", desc=True).execute()
            return resp.data or []
        except Exception as e:
            print(f"Database error listing series: {e}")
            return []

    @classmethod
    def delete_series(cls, series_id):
        """Delete a series"""
        try:
            db = cls._get_client()
            db.table("series").delete().eq("id", series_id).execute()
            return True
        except Exception as e:
            print(f"Database error deleting series: {e}")
            return False

    @classmethod
    def get_series_novels(cls, series_id):
        """Get all novels in a series ordered by book number"""
        try:
            db = cls._get_client()
            resp = (
                db.table("novels")
                .select("id, title, book_number, created_at")
                .eq("series_id", series_id)
                .order("book_number")
                .execute()
            )
            return resp.data or []
        except Exception as e:
            print(f"Database error getting series novels: {e}")
            return []

    # ── Series Arcs ───────────────────────────────────────────────────────────

    @classmethod
    def save_series_arcs(cls, series_id, overall_arc, character_arcs, themes, continuity_notes=None):
        """Save series arcs and continuity information"""
        try:
            db = cls._get_client()
            existing = db.table("series_arcs").select("id").eq("series_id", series_id).execute()
            payload = {
                "series_id": series_id,
                "overall_arc": overall_arc,
                "character_arcs": json.dumps(character_arcs),
                "themes": json.dumps(themes),
                "continuity_notes": continuity_notes,
            }
            if existing.data:
                db.table("series_arcs").update(payload).eq("series_id", series_id).execute()
            else:
                db.table("series_arcs").insert(payload).execute()
            return True
        except Exception as e:
            print(f"Database error saving series arcs: {e}")
            return False

    @classmethod
    def get_series_arcs(cls, series_id):
        """Get series arcs and continuity information"""
        try:
            db = cls._get_client()
            resp = db.table("series_arcs").select("*").eq("series_id", series_id).execute()
            if resp.data:
                arc = resp.data[0]
                arc["character_arcs"] = json.loads(arc["character_arcs"])
                arc["themes"] = json.loads(arc["themes"])
                return arc
            return None
        except Exception as e:
            print(f"Database error getting series arcs: {e}")
            return None

    # ── Chapter Outlines ──────────────────────────────────────────────────────

    @classmethod
    def save_chapter_outline(cls, novel_id, chapter_outline):
        """Save chapter outline for a novel"""
        try:
            db = cls._get_client()
            db.table("chapter_outlines").delete().eq("novel_id", novel_id).execute()
            db.table("chapter_outlines").insert({"novel_id": novel_id, "outline": json.dumps(chapter_outline)}).execute()
            return True
        except Exception as e:
            print(f"Database error saving chapter outline: {e}")
            return False

    @classmethod
    def get_chapter_outline(cls, novel_id):
        """Get chapter outline for a novel"""
        try:
            db = cls._get_client()
            resp = db.table("chapter_outlines").select("outline").eq("novel_id", novel_id).execute()
            if resp.data:
                return json.loads(resp.data[0]["outline"])
            return None
        except Exception as e:
            print(f"Database error getting chapter outline: {e}")
            return None

    # ── Scenes ────────────────────────────────────────────────────────────────

    @classmethod
    def save_scenes(cls, novel_id, all_scenes):
        """Save all scenes for a novel"""
        try:
            db = cls._get_client()
            db.table("scenes").delete().eq("novel_id", novel_id).execute()
            rows = []
            for chapter_title, scenes in all_scenes.items():
                for scene_order, scene_content in enumerate(scenes):
                    rows.append({
                        "novel_id": novel_id,
                        "chapter_title": chapter_title,
                        "scene_content": scene_content,
                        "scene_order": scene_order,
                    })
            if rows:
                db.table("scenes").insert(rows).execute()
            return True
        except Exception as e:
            print(f"Database error saving scenes: {e}")
            return False

    @classmethod
    def get_all_scenes(cls, novel_id):
        """Get all scenes for a novel"""
        try:
            db = cls._get_client()
            resp = (
                db.table("scenes")
                .select("chapter_title, scene_content, scene_order")
                .eq("novel_id", novel_id)
                .order("chapter_title")
                .order("scene_order")
                .execute()
            )
            if not resp.data:
                return None
            all_scenes = {}
            for row in resp.data:
                ch = row["chapter_title"]
                if ch not in all_scenes:
                    all_scenes[ch] = []
                all_scenes[ch].append(row["scene_content"])
            return all_scenes
        except Exception as e:
            print(f"Database error getting scenes: {e}")
            return None

    # ── Novel Formats ─────────────────────────────────────────────────────────

    @classmethod
    def save_novel_formats(cls, novel_id, novel_formats):
        """Save formatted novel content"""
        try:
            db = cls._get_client()
            db.table("novel_formats").delete().eq("novel_id", novel_id).execute()
            rows = [{"novel_id": novel_id, "format_name": k, "content": v} for k, v in novel_formats.items()]
            if rows:
                db.table("novel_formats").insert(rows).execute()
            return True
        except Exception as e:
            print(f"Database error saving novel formats: {e}")
            return False

    @classmethod
    def get_novel_formats(cls, novel_id):
        """Get formatted novel content"""
        try:
            db = cls._get_client()
            resp = db.table("novel_formats").select("format_name, content").eq("novel_id", novel_id).execute()
            if not resp.data:
                return None
            return {row["format_name"]: row["content"] for row in resp.data}
        except Exception as e:
            print(f"Database error getting novel formats: {e}")
            return None

    # ── Premises & Endings ────────────────────────────────────────────────────

    @classmethod
    def save_premises_and_endings(cls, novel_id, data):
        """Save premises and endings data"""
        try:
            db = cls._get_client()
            db.table("premises_and_endings").delete().eq("novel_id", novel_id).execute()
            db.table("premises_and_endings").insert({
                "novel_id": novel_id,
                "premises": json.dumps(data.get("premises", [])),
                "chosen_premise": data.get("chosen_premise", ""),
                "potential_endings": json.dumps(data.get("potential_endings", [])),
                "chosen_ending": data.get("chosen_ending", ""),
            }).execute()
            return True
        except Exception as e:
            print(f"Database error saving premises and endings: {e}")
            return False

    @classmethod
    def get_premises_and_endings(cls, novel_id):
        """Get premises and endings data for a novel"""
        try:
            db = cls._get_client()
            resp = (
                db.table("premises_and_endings")
                .select("premises, chosen_premise, potential_endings, chosen_ending")
                .eq("novel_id", novel_id)
                .execute()
            )
            if resp.data:
                row = resp.data[0]
                result = {
                    "premises": json.loads(row["premises"]),
                    "chosen_premise": row["chosen_premise"],
                    "potential_endings": json.loads(row["potential_endings"]),
                }
                if row.get("chosen_ending"):
                    result["chosen_ending"] = row["chosen_ending"]
                return result
            return None
        except Exception as e:
            print(f"Database error getting premises and endings: {e}")
            return None

    # ── Synopsis ──────────────────────────────────────────────────────────────

    @classmethod
    def save_novel_synopsis(cls, novel_id, synopsis):
        """Save a novel synopsis"""
        try:
            db = cls._get_client()
            db.table("novel_synopsis").delete().eq("novel_id", novel_id).execute()
            db.table("novel_synopsis").insert({"novel_id": novel_id, "synopsis": synopsis}).execute()
            return True
        except Exception as e:
            print(f"Database error saving novel synopsis: {e}")
            return False

    @classmethod
    def get_novel_synopsis(cls, novel_id):
        """Get a novel synopsis"""
        try:
            db = cls._get_client()
            resp = db.table("novel_synopsis").select("synopsis").eq("novel_id", novel_id).execute()
            return resp.data[0]["synopsis"] if resp.data else None
        except Exception as e:
            print(f"Database error getting novel synopsis: {e}")
            return None

    # ── Character Profiles ────────────────────────────────────────────────────

    @classmethod
    def save_character_profiles(cls, novel_id, profiles):
        """Save character profiles"""
        try:
            db = cls._get_client()
            db.table("character_profiles").delete().eq("novel_id", novel_id).execute()
            db.table("character_profiles").insert({"novel_id": novel_id, "profiles": profiles}).execute()
            return True
        except Exception as e:
            print(f"Database error saving character profiles: {e}")
            return False

    @classmethod
    def get_character_profiles(cls, novel_id):
        """Get character profiles"""
        try:
            db = cls._get_client()
            resp = db.table("character_profiles").select("profiles").eq("novel_id", novel_id).execute()
            return resp.data[0]["profiles"] if resp.data else None
        except Exception as e:
            print(f"Database error getting character profiles: {e}")
            return None

    # ── Novel Plan ────────────────────────────────────────────────────────────

    @classmethod
    def save_novel_plan(cls, novel_id, plan):
        """Save novel plan"""
        try:
            db = cls._get_client()
            db.table("novel_plan").delete().eq("novel_id", novel_id).execute()
            db.table("novel_plan").insert({"novel_id": novel_id, "plan": plan}).execute()
            return True
        except Exception as e:
            print(f"Database error saving novel plan: {e}")
            return False

    @classmethod
    def get_novel_plan(cls, novel_id):
        """Get novel plan"""
        try:
            db = cls._get_client()
            resp = db.table("novel_plan").select("plan").eq("novel_id", novel_id).execute()
            return resp.data[0]["plan"] if resp.data else None
        except Exception as e:
            print(f"Database error getting novel plan: {e}")
            return None

    # ── Chapter Guide ─────────────────────────────────────────────────────────

    @classmethod
    def save_chapter_guide(cls, novel_id, guide):
        """Save detailed chapter guide"""
        try:
            if not novel_id:
                print("Error: save_chapter_guide - novel_id is required")
                return False
            if not guide or not isinstance(guide, dict):
                print(f"Error: save_chapter_guide - guide must be a dictionary, got {type(guide)}")
                return False

            try:
                guide_json = json.dumps(guide)
            except (TypeError, ValueError) as e:
                print(f"Error serializing chapter guide: {e}")
                guide_json = json.dumps({})

            db = cls._get_client()
            db.table("chapter_guide").delete().eq("novel_id", novel_id).execute()
            db.table("chapter_guide").insert({"novel_id": novel_id, "guide": guide_json}).execute()
            return True
        except Exception as e:
            print(f"Database error saving chapter guide: {e}")
            return False

    @classmethod
    def get_chapter_guide(cls, novel_id):
        """Get detailed chapter guide"""
        try:
            if not novel_id:
                return {}
            db = cls._get_client()
            resp = db.table("chapter_guide").select("guide").eq("novel_id", novel_id).execute()
            if resp.data:
                try:
                    return json.loads(resp.data[0]["guide"])
                except (json.JSONDecodeError, TypeError):
                    return {}
            return {}
        except Exception as e:
            print(f"Database error getting chapter guide: {e}")
            return {}

    # ── Chapter Beats ─────────────────────────────────────────────────────────

    @classmethod
    def save_chapter_beats(cls, novel_id, beats):
        """Save chapter action beats"""
        try:
            db = cls._get_client()
            beats_json = json.dumps(beats)
            existing = db.table("chapter_beats").select("id").eq("novel_id", novel_id).execute()
            if existing.data:
                db.table("chapter_beats").update({"beats": beats_json}).eq("novel_id", novel_id).execute()
            else:
                db.table("chapter_beats").insert({"novel_id": novel_id, "beats": beats_json}).execute()
            return True
        except Exception as e:
            print(f"Database error saving chapter beats: {e}")
            return False

    @classmethod
    def get_chapter_beats(cls, novel_id):
        """Get chapter action beats"""
        try:
            db = cls._get_client()
            resp = db.table("chapter_beats").select("beats").eq("novel_id", novel_id).execute()
            if resp.data and resp.data[0].get("beats"):
                return json.loads(resp.data[0]["beats"])
            return {}
        except Exception as e:
            print(f"Database error getting chapter beats: {e}")
            return {}

    # ── Cover Design Prompts ──────────────────────────────────────────────────

    @classmethod
    def save_cover_design_prompt(cls, novel_id, prompt):
        """Save a cover design prompt for a novel"""
        try:
            db = cls._get_client()
            db.table("cover_design_prompts").delete().eq("novel_id", novel_id).execute()
            db.table("cover_design_prompts").insert({"novel_id": novel_id, "prompt": prompt}).execute()
            return True
        except Exception as e:
            print(f"Database error saving cover design prompt: {e}")
            return False

    @classmethod
    def get_cover_design_prompt(cls, novel_id):
        """Get the cover design prompt for a novel"""
        try:
            db = cls._get_client()
            resp = (
                db.table("cover_design_prompts")
                .select("prompt")
                .eq("novel_id", novel_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return resp.data[0]["prompt"] if resp.data else None
        except Exception as e:
            print(f"Database error getting cover design prompt: {e}")
            return None

    # ── Editing Suggestions ───────────────────────────────────────────────────

    @classmethod
    def save_editing_suggestion(cls, novel_id, content_id, content_type, original_text, editing_suggestions):
        """Save AI-generated editing suggestions for content"""
        try:
            db = cls._get_client()
            resp = db.table("editing_suggestions").insert({
                "novel_id": novel_id,
                "content_id": content_id,
                "content_type": content_type,
                "original_text": original_text,
                "overall_assessment": editing_suggestions.get("overall_assessment", ""),
                "strengths": json.dumps(editing_suggestions.get("strengths", [])),
                "weaknesses": json.dumps(editing_suggestions.get("weaknesses", [])),
                "suggestions": json.dumps(editing_suggestions.get("suggestions", [])),
            }).execute()
            return resp.data[0]["id"] if resp.data else None
        except Exception as e:
            print(f"Database error saving editing suggestion: {e}")
            return None

    @classmethod
    def get_editing_suggestions(cls, novel_id, content_id=None, content_type=None):
        """Get editing suggestions for a novel"""
        try:
            db = cls._get_client()
            query = db.table("editing_suggestions").select("*").eq("novel_id", novel_id)
            if content_id:
                query = query.eq("content_id", content_id)
            if content_type:
                query = query.eq("content_type", content_type)
            query = query.order("created_at", desc=True)
            resp = query.execute()

            suggestions = []
            for row in (resp.data or []):
                row["strengths"] = json.loads(row["strengths"])
                row["weaknesses"] = json.loads(row["weaknesses"])
                row["suggestions"] = json.loads(row["suggestions"])
                suggestions.append(row)
            return suggestions
        except Exception as e:
            print(f"Database error getting editing suggestions: {e}")
            return []

    # ── Keywords ──────────────────────────────────────────────────────────────

    @classmethod
    def save_novel_keywords(cls, novel_id, keywords):
        """Save searchable keywords for a novel"""
        try:
            db = cls._get_client()
            db.table("novel_keywords").delete().eq("novel_id", novel_id).execute()
            db.table("novel_keywords").insert({"novel_id": novel_id, "keywords": json.dumps(keywords)}).execute()
            return True
        except Exception as e:
            print(f"Database error saving novel keywords: {e}")
            return False

    @classmethod
    def get_novel_keywords(cls, novel_id):
        """Get searchable keywords for a novel"""
        try:
            db = cls._get_client()
            resp = (
                db.table("novel_keywords")
                .select("keywords")
                .eq("novel_id", novel_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return json.loads(resp.data[0]["keywords"]) if resp.data else []
        except Exception as e:
            print(f"Database error getting novel keywords: {e}")
            return []

    # ── BISAC Categories ──────────────────────────────────────────────────────

    @classmethod
    def save_novel_bisac(cls, novel_id, categories):
        """Save BISAC subject categories for a novel"""
        try:
            db = cls._get_client()
            db.table("novel_bisac").delete().eq("novel_id", novel_id).execute()
            db.table("novel_bisac").insert({"novel_id": novel_id, "categories": json.dumps(categories)}).execute()
            return True
        except Exception as e:
            print(f"Database error saving novel BISAC categories: {e}")
            return False

    @classmethod
    def get_novel_bisac(cls, novel_id):
        """Get BISAC subject categories for a novel"""
        try:
            db = cls._get_client()
            resp = (
                db.table("novel_bisac")
                .select("categories")
                .eq("novel_id", novel_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return json.loads(resp.data[0]["categories"]) if resp.data else []
        except Exception as e:
            print(f"Database error getting novel BISAC categories: {e}")
            return []

    # ── Quotes ────────────────────────────────────────────────────────────────

    @classmethod
    def save_novel_quotes(cls, novel_id, quotes):
        """Save novel quotes for marketing and promotion"""
        try:
            db = cls._get_client()
            db.table("novel_quotes").delete().eq("novel_id", novel_id).execute()
            db.table("novel_quotes").insert({"novel_id": novel_id, "quotes": json.dumps(quotes)}).execute()
            return True
        except Exception as e:
            print(f"Database error saving novel quotes: {e}")
            return False

    @classmethod
    def get_novel_quotes(cls, novel_id):
        """Get novel quotes for marketing and promotion"""
        try:
            db = cls._get_client()
            resp = (
                db.table("novel_quotes")
                .select("quotes")
                .eq("novel_id", novel_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            return json.loads(resp.data[0]["quotes"]) if resp.data else []
        except Exception as e:
            print(f"Database error getting novel quotes: {e}")
            return []
