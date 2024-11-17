from .models import Character, Equipement
from .forms import MoveForm
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
def soldat_list(request):
    soldats = Character.objects.all()
    return render(request, "caserne/soldat_list.html", {"soldats": soldats})


def soldat_detail(request, id_character):
    character = get_object_or_404(Character, id_character=id_character)
    form = MoveForm()
    if form.is_valid():
        ancien_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        ancien_lieu.disponibilite = "libre"
        ancien_lieu.save()
        form.save()
        nouveau_lieu = get_object_or_404(Equipement, id_equip=character.lieu.id_equip)
        nouveau_lieu.disponibilite = "occupé"
        nouveau_lieu.save()
        return redirect("soldat_detail", id_character=id_character)
    else:
        form = MoveForm()
        return render(
            request,
            "caserne/soldat_detail.html",
            {"soldat": character, "lieu": character.lieu, "form": form},
        )
