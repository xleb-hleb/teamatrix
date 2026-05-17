from django.contrib import admin, messages
from django.utils.html import format_html

from .models import (
    Component,
    DevSection,
    GitHubLink,
    ReadySolution,
    RobotAssemblyStep,
    RobotBodyPart,
    RobotBOMItem,
    RobotDrawing,
    RobotElectronics,
    RobotModel3D,
    RobotReference,
    Subsystem,
)

# ─────────────────────────────────────────────────────────────────────────────
# Универсальное действие «Дублировать»
# ─────────────────────────────────────────────────────────────────────────────

def _unique_value(model, field, value, suffix=" (копия)"):
    """Возвращает уникальное значение поля, добавляя суффикс/счётчик."""
    candidate = value + suffix
    n = 2
    while model._default_manager.filter(**{field: candidate}).exists():
        candidate = value + suffix + f" {n}"
        n += 1
    return candidate


@admin.action(description="Создать дубликат")
def duplicate_objects(modeladmin, request, queryset):
    created = 0
    for obj in queryset:
        obj.pk = None
        obj._state.adding = True

        # Уникальные строковые поля — добавляем суффикс
        model = obj.__class__
        for field_name in ("slug", "name", "title", "label"):
            field = next((f for f in model._meta.fields if f.name == field_name), None)
            if field and getattr(field, "unique", False):
                original = getattr(obj, field_name)
                setattr(obj, field_name, _unique_value(model, field_name, original))

        obj.save()
        created += 1

    messages.success(request, f"Создано дубликатов: {created}.")


# Специальная версия для RobotBodyPart — копирует и все дочерние записи
@admin.action(description="Создать дубликат (с вложенными данными)")
def duplicate_body_part(modeladmin, request, queryset):
    RELATED = [
        ("electronics",    RobotElectronics,   "body_part"),
        ("bom_items",      RobotBOMItem,        "body_part"),
        ("drawings",       RobotDrawing,        "body_part"),
        ("references",     RobotReference,      "body_part"),
        ("assembly_steps", RobotAssemblyStep,   "body_part"),
    ]

    created = 0
    for original in queryset:
        # Снимаем дочерние объекты до обнуления PK
        children = {
            attr: list(getattr(original, attr).all())
            for attr, _, _ in RELATED
        }

        original.pk = None
        original._state.adding = True

        # key уникален — добавляем суффикс к label, key оставляем для ручной правки
        original.label = _unique_value(
            RobotBodyPart, "label", original.label
        )
        # key — очищаем, чтобы администратор мог задать вручную
        original.key = ""
        original.save()

        # Копируем дочерние записи
        for attr, ChildModel, fk_field in RELATED:
            for child in children[attr]:
                child.pk = None
                child._state.adding = True
                setattr(child, fk_field, original)
                child.save()

        created += 1

    messages.success(
        request,
        f"Создано дубликатов: {created}. "
        "Не забудьте задать уникальный ключ (key) для каждой копии."
    )


# ─────────────────────────────────────────────────────────────────────────────
# Inline-классы
# ─────────────────────────────────────────────────────────────────────────────

class ComponentInline(admin.TabularInline):
    model = Component
    extra = 1


class RobotElectronicsInline(admin.TabularInline):
    model = RobotElectronics
    extra = 1
    fields = ("order", "name", "purpose", "description")


class RobotBOMItemInline(admin.TabularInline):
    model = RobotBOMItem
    extra = 1
    fields = ("order", "name", "quantity", "acquisition", "material", "note")


class RobotDrawingInline(admin.TabularInline):
    model = RobotDrawing
    extra = 1
    fields = ("order", "label", "url", "source")


class RobotReferenceInline(admin.TabularInline):
    model = RobotReference
    extra = 1
    fields = ("order", "label", "url")


class RobotAssemblyStepInline(admin.TabularInline):
    model = RobotAssemblyStep
    extra = 1
    fields = ("order", "title", "description")


# ─────────────────────────────────────────────────────────────────────────────
# Регистрация ModelAdmin
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(Subsystem)
class SubsystemAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ComponentInline]
    actions = [duplicate_objects]


@admin.register(ReadySolution)
class ReadySolutionAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    actions = [duplicate_objects]


@admin.register(DevSection)
class DevSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    prepopulated_fields = {"slug": ("title",)}
    actions = [duplicate_objects]


@admin.register(GitHubLink)
class GitHubLinkAdmin(admin.ModelAdmin):
    list_display = ("title", "link_type", "url")
    list_filter = ("link_type",)
    actions = [duplicate_objects]


@admin.register(RobotModel3D)
class RobotModel3DAdmin(admin.ModelAdmin):
    list_display  = ("__str__", "updated_at")
    readonly_fields = ("updated_at", "fbx_preview", "annotate_link")
    fieldsets = (
        (None, {
            "fields": ("fbx_file", "updated_at", "fbx_preview", "annotate_link"),
        }),
        ("Начальное положение в сцене", {
            "fields": (("init_pos_x", "init_pos_y", "init_pos_z"), "init_rot_y", "init_scale"),
            "description": (
                "Смещение и поворот модели применяются после авто-центрирования. "
                "Модель нормализована к ~100 единицам сцены. "
                "Поворот Y в градусах (положительный — по часовой стрелке сверху). "
                "Масштаб: 1.0 = без изменений, 2.0 = вдвое крупнее."
            ),
        }),
    )

    def fbx_preview(self, obj):
        if obj.fbx_file:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.fbx_file.url,
                obj.fbx_file.name,
            )
        return "—"
    fbx_preview.short_description = "Текущий файл"

    def has_add_permission(self, request):
        return not RobotModel3D.objects.exists()

    def annotate_link(self, obj):
        return format_html(
            '<a class="button" href="{}" target="_blank">&#128393; Открыть инструмент разметки</a>',
            '/development/admin-tools/annotate/',
        )
    annotate_link.short_description = "Разметка частей тела"


@admin.register(RobotBodyPart)
class RobotBodyPartAdmin(admin.ModelAdmin):
    list_display = ("label", "key", "progress_display", "subsystem")
    list_editable = ("subsystem",)
    list_filter = ("subsystem",)
    fields = ("key", "label", "color", "progress", "subsystem", "description", "controllers", "mesh_names")
    inlines = [
        RobotElectronicsInline,
        RobotBOMItemInline,
        RobotDrawingInline,
        RobotReferenceInline,
        RobotAssemblyStepInline,
    ]
    actions = [duplicate_body_part]

    def progress_display(self, obj):
        if obj.progress == 0:
            color = "#dc3545"
        elif obj.progress < 60:
            color = "#ffc107"
        else:
            color = "#198754"
        return format_html(
            '<div style="display:flex;align-items:center;gap:8px;">'
            '<div style="width:100px;background:#e9ecef;border-radius:4px;overflow:hidden;">'
            '<div style="width:{}px;background:{};height:14px;border-radius:4px;"></div>'
            '</div>'
            '<span style="font-size:12px;color:#555;">{}&nbsp;%</span>'
            '</div>',
            obj.progress,
            color,
            obj.progress,
        )
    progress_display.short_description = "Прогресс"
