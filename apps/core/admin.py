from django.contrib import admin

from .models import News, RobotLoaderConfig, TeamMember


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["title", "is_published", "created_at"]
    list_filter = ["is_published", "created_at"]
    search_fields = ["title", "summary"]
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ["is_published"]


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ["full_name", "position", "order"]
    list_editable = ["order"]
    search_fields = ["full_name", "position"]


@admin.register(RobotLoaderConfig)
class RobotLoaderConfigAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Позиция глаза", {
            "fields": ["eye_x", "eye_y"],
            "description": (
                "Смещение центра кольца от проецированного центра модели в пикселях. "
                "X: вправо +, влево −.  Y: вверх +, вниз −. "
                "При X=0, Y=0 кольцо появляется точно по центру модели."
            ),
        }),
        ("Внешний вид", {
            "fields": ["eye_size", "eye_intensity"],
            "description": (
                "eye_size — радиус кольца в пикселях (например 25 ≈ небольшое кольцо). "
                "eye_intensity — множитель яркости градиента: 0 = не видно, 1 = норма, 2 = максимум."
            ),
        }),
        ("Тайминг", {
            "fields": ["eye_start_t"],
            "description": (
                "Прогресс поворота (0–1), при котором глаз начинает загораться. "
                "0.72 = глаз появляется на последних ~28% поворота."
            ),
        }),
    ]

    def has_add_permission(self, request):
        return not RobotLoaderConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

