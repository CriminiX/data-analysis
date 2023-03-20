import pytest
from airflow.models import DagBag

@pytest.fixture(params=["../airflow/dags"])
def dag_bag(request):
    return DagBag(dag_folder=request.param, include_examples=False)

def test_no_import_errors(dag_bag):
    assert not dag_bag.import_errors