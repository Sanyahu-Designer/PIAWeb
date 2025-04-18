from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.urls import reverse
from ..models import PDI, PDIMetaHabilidade, MetaHabilidade
import json

def get_metas_habilidades_context(pdi_id):
    """
    Obtém o contexto para o card de Metas/Habilidades
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    todas_metas = MetaHabilidade.objects.filter(ativo=True).order_by('nome')
    metas_existentes = PDIMetaHabilidade.objects.filter(pdi=pdi).select_related('meta_habilidade')
    
    return {
        'pdi': pdi,
        'todas_metas': todas_metas,
        'metas_existentes': metas_existentes,
        'progresso_choices': PDIMetaHabilidade.PROGRESSO_CHOICES,
    }

@require_POST
def adicionar_meta_habilidade(request, pdi_id):
    """
    Adiciona uma nova Meta/Habilidade ao PDI
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    meta_id = request.POST.get('meta_habilidade')
    progresso = request.POST.get('progresso', 0)
    
    # Verificar se a meta já existe para este PDI
    if PDIMetaHabilidade.objects.filter(pdi=pdi, meta_habilidade_id=meta_id).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Esta Meta/Habilidade já está associada a este PDI'
        })
    
    # Criar nova meta/habilidade
    meta_habilidade = get_object_or_404(MetaHabilidade, id=meta_id)
    nova_meta = PDIMetaHabilidade.objects.create(
        pdi=pdi,
        meta_habilidade=meta_habilidade,
        progresso=progresso
    )
    
    return JsonResponse({
        'status': 'success',
        'id': nova_meta.id,
        'nome': nova_meta.meta_habilidade.nome,
        'progresso': nova_meta.progresso
    })

@require_POST
def excluir_meta_habilidade(request, pdi_id, meta_id):
    """
    Exclui uma Meta/Habilidade do PDI
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    meta = get_object_or_404(PDIMetaHabilidade, id=meta_id, pdi=pdi)
    
    meta.delete()
    
    return JsonResponse({
        'status': 'success'
    })

@require_POST
def atualizar_meta_habilidade(request, pdi_id, meta_id):
    """
    Atualiza o progresso de uma Meta/Habilidade
    """
    pdi = get_object_or_404(PDI, id=pdi_id)
    meta = get_object_or_404(PDIMetaHabilidade, id=meta_id, pdi=pdi)
    
    progresso = request.POST.get('progresso', meta.progresso)
    meta.progresso = progresso
    meta.save()
    
    return JsonResponse({
        'status': 'success',
        'progresso': meta.progresso
    })
