import markdown
from django.conf import settings
from django.http import Http404
from django.shortcuts import render

from loader import load_modules
from validators import run_check


def _get_modules():
    return load_modules(settings.CONTENT_MODULES_DIR)


def index(request):
    modules = _get_modules()
    return render(request, "checker/index.html", {"modules": modules, "current_slug": None})


def module_detail(request, slug):
    modules = _get_modules()
    module = next((m for m in modules if m.slug == slug), None)
    if module is None:
        raise Http404(f"Module '{slug}' introuvable")

    content_html = markdown.markdown(module.content_md)

    results = None
    if request.method == "POST":
        results = [(check, run_check(check)) for check in module.checks]
    all_passed = results is not None and all(result.passed for _, result in results)

    position = modules.index(module)
    next_module = modules[position + 1] if position + 1 < len(modules) else None

    return render(
        request,
        "checker/module.html",
        {
            "modules": modules,
            "current_slug": slug,
            "module": module,
            "content_html": content_html,
            "results": results,
            "all_passed": all_passed,
            "next_module": next_module if all_passed else None,
        },
    )
