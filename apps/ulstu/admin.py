from django.contrib import admin

from .models import Application, PrivacyPolicy, RoadmapStage, UlstuMember, UlstuTeam


@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    fields = ("content", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        # Разрешаем только одну запись
        return not PrivacyPolicy.objects.exists()


@admin.register(RoadmapStage)
class RoadmapStageAdmin(admin.ModelAdmin):
    list_display = ("title", "period", "is_completed", "order")
    list_filter = ("is_completed",)


class UlstuMemberInline(admin.TabularInline):
    model = UlstuMember
    extra = 1


@admin.register(UlstuTeam)
class UlstuTeamAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    inlines = [UlstuMemberInline]


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "specialty", "created_at", "is_processed")
    list_filter = ("is_processed",)
    actions = ["mark_processed"]

    def mark_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_processed.short_description = "Отметить как обработанные"
