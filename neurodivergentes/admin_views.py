from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import ParecerAvaliativo

@method_decorator(staff_member_required, name='dispatch')
class ParecerGraficosView(TemplateView):
    template_name = 'admin/neurodivergentes/pareceravaliativo/graficos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parecer_id = kwargs.get('parecer_id')
        context['parecer'] = get_object_or_404(ParecerAvaliativo, pk=parecer_id)
        return context
