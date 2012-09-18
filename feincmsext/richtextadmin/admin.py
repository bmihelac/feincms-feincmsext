from django.contrib import admin
from django.conf import settings
from django.template.loader import render_to_string
from django.template import Context


class RichTextModelMixin(object):
    """
    Mixin that includes template and context for editing
    RichTextContent fields.
    """
    change_form_template = "admin/feincms/richtext/change_form.html"

    def get_richtext_context(self, extra_context):
        extra_context = extra_context or {}
        ctx = Context({
            'richtext_template_base': settings.FEINCMS_RICHTEXT_INIT_TEMPLATE
            })
        extra_context['init_richtext'] = render_to_string(
                "admin/feincms/richtext/init_richtext.html",
                settings.FEINCMS_RICHTEXT_INIT_CONTEXT,
                ctx
                )
        return extra_context

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = self.get_richtext_context(extra_context)
        return super(RichTextModelMixin, self).change_view(request, object_id,
            form_url, extra_context=extra_context)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = self.get_richtext_context(extra_context)
        return super(RichTextModelMixin, self).add_view(request,
            form_url, extra_context=extra_context)


class RichTextModelAdmin(RichTextModelMixin, admin.ModelAdmin):
    """
    ModelAdmin class that includes template and context for editing
    RichTextContent fields.
    """
    pass
