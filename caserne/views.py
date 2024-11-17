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
        new_lieu = form.cleaned_data["lieu"]
        ancien_lieu = soldat.lieu

        # Vérification des contraintes de disponibilité
        if new_lieu.id_equip in ("Douche", "Barre de tractions"):
            if new_lieu.disponibilite == "occupé":
                message = f"Le lieu {new_lieu.id_equip} est déjà occupé."
            else:
                # Mise à jour de l'ancien lieu
                if ancien_lieu:
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()

                # Mise à jour du nouveau lieu
                new_lieu.disponibilite = "occupé"
                new_lieu.save()

                # Enregistrer le changement de lieu
                form.save()
                return redirect("soldat_detail", id_character=soldat.id_character)
        else:
            # Gestion des lieux sans contraintes
            if ancien_lieu:
                ancien_lieu.disponibilite = "libre"
                ancien_lieu.save()

            form.save()
            return redirect("soldat_detail", id_character=soldat.id_character)

    return render(
        request,
        "caserne/soldat_detail.html",
        {"soldat": soldat, "form": form, "message": message},
    )
