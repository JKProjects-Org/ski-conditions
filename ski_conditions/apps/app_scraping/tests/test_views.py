import pytest
from django.urls import reverse

from .factories import ResortFactory


@pytest.mark.django_db()
def test_index_view(client):
    resort = ResortFactory()
    response = client.get(reverse('conditions:index'))
    assert response.status_code == 200
    assert list(response.context['resort_list']) == [resort]
