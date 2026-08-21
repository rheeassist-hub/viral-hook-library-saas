# -*- coding: utf-8 -*-
"""
바이럴 훅 문구 추천 SaaS - FastAPI 백엔드
숏폼 영상 주제/카테고리를 입력받아 매칭되는 바이럴 훅 문구 5개를 추천한다.
"""

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from hooks_data import recommend_hooks, get_categories, get_total_hook_count

app = FastAPI(title="Viral Hook Library SaaS")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "categories": get_categories(),
            "total_count": get_total_hook_count(),
            "result": None,
            "query": "",
            "matched_category": None,
        },
    )


@app.post("/recommend", response_class=HTMLResponse)
def recommend(request: Request, category: str = Form(...)):
    hooks, matched_category = recommend_hooks(category, top_n=5)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "categories": get_categories(),
            "total_count": get_total_hook_count(),
            "result": hooks,
            "query": category,
            "matched_category": matched_category,
        },
    )


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
