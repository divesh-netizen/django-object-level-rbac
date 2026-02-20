# Django ReBAC PoC (hierarchical object-level permissions)

This PoC demonstrates hierarchical object-level permissions in Django using `django-guardian`.

## 1) Create project and install deps

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Database setup

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data
```

## 3) Run server

```bash
python manage.py runserver
```

## 4) Demo users

Created by `seed_demo_data` (password is `pass1234` for all):

- `org_admin` → ORG_ADMIN on Organization Alpha
- `store_manager` → STORE_MANAGER on Store Alpha Downtown
- `camera_viewer` → VIEWER on Store Alpha Downtown + direct access to one specific camera

## 5) Test hierarchy behavior

Use session auth (log in via `/admin/login/`) or create your own script/client.

Endpoints:

- `GET /api/stores/`
- `GET /api/cameras/`
- `GET /api/machines/`
- `GET /api/cameras/<id>/probe/` (returns 403 when denied)

Expected outcomes:

- `org_admin` sees all stores/cameras/machines under Org Alpha, but none under Org Beta.
- `store_manager` sees only Store Alpha Downtown and its child cameras/machines.
- `camera_viewer` sees camera(s) inherited from Store Alpha Downtown, plus explicitly assigned camera object access.

## Key files

- `core/models.py`: hierarchy (`Organization -> Store -> Camera/Machine`) and custom `User`
- `core/permissions.py`: central `has_object_access(user, obj, action)` resolver with parent walking
- `core/roles.py`: role templates (`ORG_ADMIN`, `STORE_MANAGER`, `VIEWER`) and assignment helper
- `core/views.py`: demo endpoints + denial example
- `core/management/commands/seed_demo_data.py`: fixture-like seed command
