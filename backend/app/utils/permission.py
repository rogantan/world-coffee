from app.admin.enum.permission_mode import PermissionMode
from app.reports.service.report_service import report_service
from app.admin.service.user_permission_service import user_permission_service
from pprint import pprint


async def has_permission(user, report_title: str, mode: PermissionMode):
    report = await report_service.get_report(report_title)
    if not report:
        return False
    
    permission = await user_permission_service.get_permission(user_id=user.id, report_id=report.id)

    pprint(permission[0].mode)
    if permission:
        permission_mode = permission[0].mode.value
        pprint(permission_mode == "displayed")
        if (
            (mode.value == "editable"
            and permission_mode == mode.value) or
            (mode.value == "displayed"
            and permission_mode in ("displayed", "editable"))
        ):
            return True
    return False