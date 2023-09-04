from exceptions import MissingRequiredValues, TheValueAlreadyExists
import util
from services.conn_db import DataBaseConn

def insert_research_form(
    scores: list[str],
    cities: list[str],
    neighborhoods: list[str],
    satisfaction_rate: int,
    obversation: str | None,
    criminix_id: str
):
    
    if scores is None:
        raise MissingRequiredValues(["scores"])
    elif cities is None:
        raise MissingRequiredValues(["cities"])
    elif neighborhoods is None:
        raise MissingRequiredValues(["neighborhoods"])
    elif satisfaction_rate is None:
        raise MissingRequiredValues(["satisfaction_rate"])
    else:
        list_of_scores = ', '.join([str(elem) for elem in scores])
        list_of_cities = ', '.join([str(elem) for elem in cities])
        list_of_neighborhoods = ', '.join([str(elem) for elem in neighborhoods])

        conn = DataBaseConn()

        query = """
            INSERT INTO tb_search_form (scores, cities, neighborhoods, satisfaction_rate, obversation, criminix_id, created_at)
            VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}')
        """.format(str(list_of_scores), str(list_of_cities), str(list_of_neighborhoods), int(satisfaction_rate), str(obversation), str(criminix_id), util.get_today_date())

        cursor = conn.db_connect()
        cursor.execute(query)
        conn.conn.commit()
        conn.db_disconnect()
       