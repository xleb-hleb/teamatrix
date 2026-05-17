import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from .models import DevSection, GitHubLink, ReadySolution, RobotBodyPart, RobotModel3D, Subsystem


class DevelopmentIndexView(TemplateView):
    template_name = "development/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["subsystems"] = Subsystem.objects.prefetch_related("components").all()
        ctx["ready_solutions"] = ReadySolution.objects.all()
        ctx["dev_sections"] = DevSection.objects.all()
        ctx["github_models"] = GitHubLink.objects.filter(link_type=GitHubLink.TYPE_MODELS)
        ctx["github_software"] = GitHubLink.objects.filter(link_type=GitHubLink.TYPE_SOFTWARE)

        robot_parts = list(
            RobotBodyPart.objects.select_related("subsystem").prefetch_related(
                "electronics", "bom_items", "drawings", "references", "assembly_steps"
            ).all()
        )
        ctx["robot_parts"] = robot_parts

        parts_data = {}
        mesh_map = {}
        for part in robot_parts:
            ann = None
            if part.annotation_x is not None:
                ann = {"x": part.annotation_x, "y": part.annotation_y, "z": part.annotation_z}
            parts_data[part.key] = {
                "label":       part.label,
                "progress":    part.progress,
                "color":       part.color or "",
                "description": part.description,
                "url":         "#part-" + part.key,
                "annotation":  ann,
            }
            for name in (part.mesh_names or "").split(","):
                name = name.strip()
                if name:
                    mesh_map[name] = part.key

        ctx["robot_parts_json"]    = json.dumps(parts_data, ensure_ascii=False)
        ctx["robot_mesh_map_json"] = json.dumps(mesh_map, ensure_ascii=False)
        robot_model = RobotModel3D.objects.first()
        ctx["robot_model"] = robot_model
        if robot_model:
            ctx["robot_init_json"] = json.dumps({
                "pos_x": robot_model.init_pos_x,
                "pos_y": robot_model.init_pos_y,
                "pos_z": robot_model.init_pos_z,
                "rot_y": robot_model.init_rot_y,
                "scale": robot_model.init_scale,
            })
        return ctx


class SubsystemDetailView(TemplateView):
    template_name = "development/subsystem_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        subsystem = get_object_or_404(Subsystem, slug=self.kwargs["slug"])
        ctx["subsystem"] = subsystem
        ctx["components"] = subsystem.components.all()
        ctx["all_subsystems"] = Subsystem.objects.all()
        return ctx


class RobotBodyPartDetailView(TemplateView):
    template_name = "development/robot_part_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        part = get_object_or_404(
            RobotBodyPart.objects.prefetch_related(
                "electronics", "bom_items", "drawings", "references", "assembly_steps"
            ),
            key=self.kwargs["key"],
        )
        ctx["part"] = part
        ctx["all_parts"] = RobotBodyPart.objects.all()
        return ctx


# ──────────────────────────────────────────────────────────────────────────────
# Admin annotation tool
# ──────────────────────────────────────────────────────────────────────────────

@staff_member_required
def admin_annotate_view(request):
    """Page for placing annotation anchors on the 3D model."""
    robot_model = RobotModel3D.objects.first()
    parts = list(RobotBodyPart.objects.order_by("key"))

    parts_json = json.dumps([
        {
            "key":   p.key,
            "label": p.label,
            "color": p.color or "#0ea5e9",
            "annotation": {
                "x": p.annotation_x,
                "y": p.annotation_y,
                "z": p.annotation_z,
            } if p.annotation_x is not None else None,
        }
        for p in parts
    ], ensure_ascii=False)

    mesh_map = {}
    for part in parts:
        for name in (part.mesh_names or "").split(","):
            name = name.strip()
            if name:
                mesh_map[name] = part.key

    return render(request, "development/admin_annotate.html", {
        "robot_model":    robot_model,
        "parts":          parts,
        "parts_json":     parts_json,
        "mesh_map_json":  json.dumps(mesh_map, ensure_ascii=False),
        "title":          "Разметка 3D-модели",
    })


@staff_member_required
@require_POST
def admin_annotate_save(request):
    """AJAX endpoint: save annotation coords for one body part."""
    try:
        data = json.loads(request.body)
        key  = data["key"]
        x, y, z = float(data["x"]), float(data["y"]), float(data["z"])
    except (KeyError, ValueError, json.JSONDecodeError) as e:
        return JsonResponse({"ok": False, "error": str(e)}, status=400)

    updated = RobotBodyPart.objects.filter(key=key).update(
        annotation_x=x, annotation_y=y, annotation_z=z
    )
    if not updated:
        return JsonResponse({"ok": False, "error": "Part not found"}, status=404)
    return JsonResponse({"ok": True})
