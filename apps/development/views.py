import json

from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from .models import DevSection, GitHubLink, ReadySolution, RobotBodyPart, Subsystem


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
        for part in robot_parts:
            parts_data[part.key] = {
                "label": part.label,
                "progress": part.progress,
                "description": part.description,
                "url": "#part-" + part.key,
            }
        ctx["robot_parts_json"] = json.dumps(parts_data, ensure_ascii=False)
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
