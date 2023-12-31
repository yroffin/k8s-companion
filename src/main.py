from utils.security import SecurityService
from utils.orm import OrmService
from utils.logger import LoggerService

# Load pages
from pages.main import MainPage
from pages.graph import GraphPage
from pages.namespaces import NamespacesPage
from pages.workloads import WorkloadsPage
from pages.services import ServicesPage
from pages.apiresources import ApiResourcesPage
from nicegui import app

import logging

def startup():
    LoggerService().startup()
    logging.info("Main")
    OrmService().startup()
    SecurityService().startup()

if __name__ in {"__main__", "__mp_main__"}:
    startup()
