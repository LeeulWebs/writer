-- Run this in your Supabase SQL Editor (Dashboard > SQL Editor > New Query)
-- This creates all tables needed for the Young Adults Novel Generator app

CREATE TABLE IF NOT EXISTS series (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    num_books INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS series_arcs (
    id BIGSERIAL PRIMARY KEY,
    series_id BIGINT NOT NULL REFERENCES series(id) ON DELETE CASCADE,
    overall_arc TEXT NOT NULL,
    character_arcs TEXT NOT NULL,
    themes TEXT NOT NULL,
    continuity_notes TEXT
);

CREATE TABLE IF NOT EXISTS novels (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    model TEXT NOT NULL,
    max_scene_length INTEGER NOT NULL,
    min_scene_length INTEGER NOT NULL,
    story_details TEXT,
    series_id BIGINT REFERENCES series(id) ON DELETE SET NULL,
    book_number INTEGER DEFAULT 1,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS chapter_outlines (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    outline TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS scenes (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    chapter_title TEXT NOT NULL,
    scene_content TEXT NOT NULL,
    scene_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS novel_formats (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    format_name TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS premises_and_endings (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    premises TEXT NOT NULL,
    chosen_premise TEXT NOT NULL,
    potential_endings TEXT NOT NULL,
    chosen_ending TEXT
);

CREATE TABLE IF NOT EXISTS novel_synopsis (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    synopsis TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS character_profiles (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    profiles TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS novel_plan (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    plan TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chapter_guide (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    guide TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS chapter_beats (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL UNIQUE REFERENCES novels(id) ON DELETE CASCADE,
    beats TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS cover_design_prompts (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    prompt TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS editing_suggestions (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    content_id TEXT NOT NULL,
    content_type TEXT NOT NULL,
    original_text TEXT NOT NULL,
    overall_assessment TEXT NOT NULL,
    strengths TEXT NOT NULL,
    weaknesses TEXT NOT NULL,
    suggestions TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS novel_keywords (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    keywords TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS novel_bisac (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    categories TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS novel_quotes (
    id BIGSERIAL PRIMARY KEY,
    novel_id BIGINT NOT NULL REFERENCES novels(id) ON DELETE CASCADE,
    quotes TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
