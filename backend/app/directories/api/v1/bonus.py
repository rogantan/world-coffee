from fastapi import APIRouter
from app.admin.dependens.auth import CurrentUserDep
from typing import List
from app.directories.service.bonus_service import bonus_service
from app.directories.schema.bonus_schema import BonusSchema, BonusEditSchema

router = APIRouter(prefix="/bonuses", tags=["Справочник. Премии"])

@router.get("", response_model=List[BonusEditSchema])
async def get_bonus(user: CurrentUserDep):
  return await bonus_service.get_bonuses()

@router.post("")
async def create_bonus(user: CurrentUserDep, bonus: BonusSchema):
  return await bonus_service.create_bonus(bonus)

@router.put("/{row_id}")
async def edit_bonus(user: CurrentUserDep, row_id: int, bonus: BonusSchema):
  return await bonus_service.edit_bonus(row_id, bonus)