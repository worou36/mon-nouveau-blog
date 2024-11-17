from .models import Character
from .forms import MoveForm
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
def soldat_list(request):
    soldats = Character.objects.all()
    return render(request, "caserne/soldat_list.html", {"soldats": soldats})


def soldat_detail(request, id_character):
    # Récupérer le soldat et le formulaire
    soldat = get_object_or_404(Character, id_character=id_character)
    form = MoveForm(request.POST or None, instance=soldat)

    if request.method == "POST" and form.is_valid():
        # Récupérer l'ancien lieu
        if soldat.lieu:
            ancien_lieu = get_object_or_404(Equipement, id_equip=soldat.lieu.id_equip)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()

        # Sauvegarder les modifications du soldat
        form.save()

        # Récupérer le nouveau lieu
        nouveau_lieu = get_object_or_404(Equipement, id_equip=soldat.lieu.id_equip)
        nouveau_lieu.disponibilite = "occupé"
        nouveau_lieu.save()

        return redirect("soldat_detail", id_character=soldat.id_character)

    return render(
        request,
        "caserne/soldat_detail.html",
        {"soldat": soldat, "form": form},
    )
