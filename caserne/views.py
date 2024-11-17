from .models import Character, Equipement
from .forms import MoveForm
from django.shortcuts import render, get_object_or_404, redirect


def soldat_list(request):
    soldats = Character.objects.all()
    return render(request, "caserne/soldat_list.html", {"soldats": soldats})


def soldat_detail(request, id_character):
    # Récupérer le soldat
    soldat = get_object_or_404(Character, id_character=id_character)

    # Instancier le formulaire lié au soldat
    form = MoveForm(request.POST or None, instance=soldat)

    if request.method == "POST" and form.is_valid():
        # Libérer l'ancien lieu si assigné
        if soldat.lieu:
            ancien_lieu = get_object_or_404(Equipement, id_equip=soldat.lieu.id_equip)
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()

        # Sauvegarder le formulaire pour mettre à jour le lieu du soldat
        form.save()

        # Marquer le nouveau lieu comme occupé
        nouveau_lieu = get_object_or_404(Equipement, id_equip=soldat.lieu.id_equip)
        nouveau_lieu.disponibilite = "occupé"
        nouveau_lieu.save()

        # Rediriger après les modifications
        return redirect("soldat_detail", id_character=id_character)

    # Rendu de la page
    return render(
        request,
        "caserne/soldat_detail.html",
        {"soldat": soldat, "form": form},
    )
