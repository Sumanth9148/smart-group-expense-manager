from uuid import uuid4
from unittest.mock import Mock
from app.services.settlement_service import SettlementService
from app.domain.domain_services.settlement_calculator import SettlementCalculator
from app.domain.entities.group import Group


def test_get_balances():
    group_id = uuid4()
    group = Group(group_id, "Trip")

    group_repo = Mock()
    group_repo.get_by_id.return_value = group

    calculator = SettlementCalculator()
    service = SettlementService(group_repo, calculator)

    balances = service.get_balances(group_id)

    assert isinstance(balances, dict)
