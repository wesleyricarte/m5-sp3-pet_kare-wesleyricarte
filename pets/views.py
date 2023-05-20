from rest_framework.views import APIView, Request, Response, status
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from pets.serializers import PetSerializer
from pets.models import Pet
from groups.models import Group
from traits.models import Trait


class PetView(APIView, PageNumberPagination):
    def post(self, request: Request) -> Response:
        serializer = PetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        group_data = serializer.validated_data.pop("group", None)
        traits_data = serializer.validated_data.pop("traits", None)

        group = Group.objects.filter(
            scientific_name__iexact=group_data["scientific_name"]
        ).first()
        if not group:
            group = Group.objects.create(**group_data)

        new_pet: Pet = Pet.objects.create(**serializer.validated_data, group=group)

        for trait in traits_data:
            object = Trait.objects.filter(name__iexact=trait["name"]).first()
            if not object:
                object = Trait.objects.create(**trait)
            new_pet.traits.add(object)

        serializer_show = PetSerializer(instance=new_pet)

        return Response(serializer_show.data, status=status.HTTP_201_CREATED)

    def get(self, request: Request) -> Response:
        pets = Pet.objects.all()

        traits = request.query_params.get("trait", None)
        if traits:
            trait = Trait.objects.filter(name__iexact=traits).first()
            if trait:
                pets = Pet.objects.filter(traits=trait).all()

        pets_paged = self.paginate_queryset(pets, request)
        serializer = PetSerializer(instance=pets_paged, many=True)

        return self.get_paginated_response(serializer.data)


class PetDetailView(APIView):
    def get(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(instance=pet)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, pet_id: int) -> Response:
        pet: Pet = get_object_or_404(Pet, id=pet_id)
        serializer = PetSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        group_data: dict = serializer.validated_data.pop("group", None)
        traits_data: list = serializer.validated_data.pop("traits", None)

        if group_data:
            group_find = Group.objects.filter(scientific_name__iexact=group_data["scientific_name"])
            if group_find:
                object = group_find.first()
            else:
                object = Group.objects.create(scientific_name=group_data["scientific_name"])

            pet.group = object

        traits: list = []
        if traits_data:
            for trait in traits_data:
                trait_find = Trait.objects.filter(name__iexact=trait["name"])
                if trait_find:
                    object = trait_find.first()
                else:
                    object = Trait.objects.create(name=trait["name"])
                traits.append(object)
            pet.traits.set(traits)

        for key, value in serializer.validated_data.items():
            setattr(pet, key, value)

        pet.save()
        serializer = PetSerializer(pet)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pet_id: int) -> Response:
        pet = get_object_or_404(Pet, id=pet_id)
        pet.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
