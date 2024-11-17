from .models import Character
from .forms import MoveForm
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.
def soldat_list(request):
    soldats = Character.objects.all()
    return render(request, "caserne/soldat_list.html", {"soldats": soldats})


def soldat_detail(request, id_character, message=""):
    soldat = get_object_or_404(Character, id_character=id_character)
    form = MoveForm(request.POST or None, instance=soldat)

    if request.method == "POST" and form.is_valid():
        # Récupérer le nouveau lieu demandé
        new_lieu = form.cleaned_data["lieu"]
        ancien_lieu = soldat.lieu  # Récupérer l'ancien lieu

        if new_lieu.id_equip in ("Douche", "Barre de tractions"):
            # Vérifier si le lieu est disponible
            if new_lieu.disponibilite == "occupé":
                message = f"Le lieu {new_lieu.id_equip} est déjà occupé."
            else:
                # Libérer l'ancien lieu (si nécessaire)
                if ancien_lieu and ancien_lieu.id_equip in ("Douche", "Barre de tractions"):
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()

                # Occuper le nouveau lieu
                new_lieu.disponibilite = "occupé"
                new_lieu.save()

                # Enregistrer le changement pour le soldat
                form.save()
                return redirect("soldat_detail", id_character=soldat.id_character)

        else:
            # Pour les lieux "illimités" (piscine, dortoir)
            if ancien_lieu and ancien_lieu.id_equip in ("Douche", "Barre de tractions"):
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

            # Pas de modification de disponibilité pour piscine/dortoir
            form.save()
            return redirect("soldat_detail", id_character=soldat.id_character)

    return render(
        request,
        "caserne/soldat_detail.html",
        {"soldat": soldat, "form": form, "message": message},
    )
