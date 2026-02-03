COMPOSE = docker-compose -f infrastructure/docker-compose.yml

.PHONY: start_db alembic_upgrade elt_run dbt_tests workflow


start_db:
		$(COMPOSE) up postgres -d

alembic_upgrade:
		alembic upgrade head

etl_run:
		$(COMPOSE) run --rm etl 

dbt_tests:
		$(COMPOSE) run --rm dbt 

workflow:
		make start_db
		make alembic_upgrade
		make etl_run
		make dbt_tests