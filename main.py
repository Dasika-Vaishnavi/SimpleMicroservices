from __future__ import annotations
import os
import socket
from datetime import datetime
from typing import Dict, List
from uuid import UUID
from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional
from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health

# --- NEW IMPORTS ---
from models.organization import OrganizationCreate, OrganizationRead, OrganizationUpdate
from models.project import ProjectCreate, ProjectRead, ProjectUpdate

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}

# --- NEW DATABASES ---
organizations: Dict[UUID, OrganizationRead] = {}
projects: Dict[UUID, ProjectRead] = {}

app = FastAPI(
    title="Person/Address API",
    description="Demo FastAPI app using Pydantic v2 models for Person and Address",
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Address endpoints
# -----------------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())
    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]
    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())
    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]
    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# Organization endpoints (NEW)
# -----------------------------------------------------------------------------
@app.post("/organizations", response_model=OrganizationRead, status_code=201)
def create_organization(org: OrganizationCreate):
    if org.id in organizations:
        raise HTTPException(status_code=400, detail="Organization with this ID already exists")
    organizations[org.id] = OrganizationRead(**org.model_dump())
    return organizations[org.id]

@app.get("/organizations", response_model=List[OrganizationRead])
def list_organizations(name: Optional[str] = Query(None, description="Organization name to filter")):
    results = list(organizations.values())
    if name is not None:
        results = [o for o in results if o.name == name]
    return results

@app.get("/organizations/{org_id}", response_model=OrganizationRead)
def get_organization(org_id: UUID):
    if org_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organizations[org_id]

@app.patch("/organizations/{org_id}", response_model=OrganizationRead)
def update_organization(org_id: UUID, update: OrganizationUpdate):
    if org_id not in organizations:
        raise HTTPException(status_code=404, detail="Organization not found")
    stored = organizations[org_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    organizations[org_id] = OrganizationRead(**stored)
    return organizations[org_id]

# -----------------------------------------------------------------------------
# Project endpoints (NEW)
# -----------------------------------------------------------------------------
@app.post("/projects", response_model=ProjectRead, status_code=201)
def create_project(project: ProjectCreate):
    if project.id in projects:
        raise HTTPException(status_code=400, detail="Project with this ID already exists")
    projects[project.id] = ProjectRead(**project.model_dump())
    return projects[project.id]

@app.get("/projects", response_model=List[ProjectRead])
def list_projects(title: Optional[str] = Query(None, description="Project title to filter")):
    results = list(projects.values())
    if title is not None:
        results = [p for p in results if p.title == title]
    return results

@app.get("/projects/{project_id}", response_model=ProjectRead)
def get_project(project_id: UUID):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects[project_id]

@app.patch("/projects/{project_id}", response_model=ProjectRead)
def update_project(project_id: UUID, update: ProjectUpdate):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    stored = projects[project_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    projects[project_id] = ProjectRead(**stored)
    return projects[project_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
