from django import template
from teacher.models import StudyMaterial
import os

register = template.Library()

@register.simple_tag
def display_study_material_name(material_id):
    try:
        study_material = StudyMaterial.objects.get(id=material_id)
        file_name = os.path.basename(study_material.file.name)
        return file_name
    except StudyMaterial.DoesNotExist:
        return "Study material not found"
