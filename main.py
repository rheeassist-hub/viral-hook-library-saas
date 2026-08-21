# -*- coding: utf-8 -*-
"""
바이럴 훅 문구 추천 SaaS - FastAPI 백엔드
숏폼 영상 주제/카테고리를 입력받아 매칭되는 바이럴 훅 문구 5개를 추천한다.
"""

import jinja2
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse

from hooks_data import recommend_hooks, get_categories, get_total_hook_count

app = FastAPI(title="Viral Hook Library SaaS")

# Vercel 서버리스 환경에서 FastAPI Jinja2Templates 내부 LRUCache가
# "unhashable type: 'dict'"로 깨지는 문제가 있어 캐시를 끈 순수 jinja2 Environment 사용.
import os

_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
_jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(_TEMPLATES_DIR),
    cache_size=0,
    autoescape=jinja2.select_autoescape(["html"]),
)


def render_template(name: str, **context) -> str:
    return _jinja_env.get_template(name).render(**context)


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return HTMLResponse(render_template(
        "index.html",
        request=request,
        categories=get_categories(),
        total_count=get_total_hook_count(),
        result=None,
        query="",
        matched_category=None,
    ))


@app.post("/recommend", response_class=HTMLResponse)
def recommend(request: Request, category: str = Form(...)):
    hooks, matched_category = recommend_hooks(category, top_n=5)
    return HTMLResponse(render_template(
        "index.html",
        request=request,
        categories=get_categories(),
        total_count=get_total_hook_count(),
        result=hooks,
        query=category,
        matched_category=matched_category,
    ))


@app.get("/api/recommend")
def api_recommend(category: str):
    """API 형태로도 사용 가능 (예: /api/recommend?category=뷰티)"""
    hooks, matched_category = recommend_hooks(category, top_n=5)
    return {
        "query": category,
        "matched_category": matched_category,
        "hooks": hooks,
        "count": len(hooks),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
