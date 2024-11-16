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

    if request.method == "POST":
        if form.is_valid():
            # Récupérer le nouveau lieu depuis le formulaire
            new_lieu = form.cleaned_data["lieu"]

            if new_lieu.id_equip in ("Douche", "Barre_tractions"):
                # Vérifier si le lieu est déjà occupé
                if new_lieu.disponibilite == "occupé":
                    message = f"Le lieu {new_lieu.id_equip} est déjà occupé."
                else:
                    # Mise à jour si disponible
                    ancien_lieu = soldat.lieu
                    if ancien_lieu:
                        ancien_lieu.disponibilite = "libre"
                        ancien_lieu.save()

                    new_lieu.disponibilite = "occupé"
                    new_lieu.save()
                    form.save()
                    return redirect("soldat_detail", id_character=soldat.id_character)

            else:
                # Pour les lieux sans contraintes (piscine, dortoir, etc.)
                ancien_lieu = soldat.lieu
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
