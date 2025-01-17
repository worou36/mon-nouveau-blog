from .models import Character, Equipement
from .forms import MoveForm
from django.shortcuts import render, get_object_or_404, redirect


def soldat_list(request):
    soldats = Character.objects.all()
    return render(request, "caserne/soldat_list.html", {"soldats": soldats})


def soldat_detail(request, id_character):
    # Récupérer le soldat et l'ancien lieu
    soldat = get_object_or_404(Character, id_character=id_character)
    ancien_lieu = get_object_or_404(Equipement, id_equip=soldat.lieu.id_equip)

    form = MoveForm(request.POST or None, instance=soldat)
    message = ""

    if request.method == "POST" and form.is_valid():
        # Récupérer le nouveau lieu depuis le formulaire
        nouveau_lieu = form.cleaned_data["lieu"]

        # Vérifier si le nouveau lieu est déjà occupé
        if nouveau_lieu.disponibilite == "occupé":
            message = f"Le lieu {nouveau_lieu.id_equip} est déjà occupé."
        else:
            # Libérer l'ancien lieu si assigné
            if soldat.lieu:

                # Marquer l'ancien lieu comme libre
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()  # Sauvegarder l'ancien lieu

            # Sauvegarder le formulaire pour mettre à jour le lieu du soldat
            form.save()

            # Marquer le nouveau lieu comme occupé
            nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()  

            # Rediriger après les modifications
            return redirect("soldat_detail", id_character=soldat.id_character)

    # Rendu de la page
    return render(
        request,
        "caserne/soldat_detail.html",
        {"soldat": soldat, "form": form, "message": message},
    )
